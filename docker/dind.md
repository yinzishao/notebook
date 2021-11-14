# docker compose
- [docker compose](https://hub.docker.com/r/tmaier/docker-compose/)
- [Run docker-compose build in .gitlab-ci.yml](https://stackoverflow.com/a/52734017)

```bash
image: tmaier/docker-compose:latest

services:
  - docker:dind

before_script:
  - docker info
  - docker-compose --version

build image:
  stage: build
  script:
    - docker-compose build
```

gitlab使用docker compose的教程


```bash

ARG DOCKER_VERSION=latest
FROM docker:${DOCKER_VERSION}

ARG COMPOSE_VERSION=1.26.2
ARG DOCKER_VERSION

RUN apk add --no-cache py3-pip python3
RUN apk add --no-cache --virtual build-dependencies python3-dev libffi-dev openssl-dev gcc libc-dev make \
  && pip3 install "docker-compose${COMPOSE_VERSION:+==}${COMPOSE_VERSION}" \
  && apk del build-dependencies

LABEL \
  org.opencontainers.image.authors="Tobias Maier <tobias.maier@baucloud.com>" \
  org.opencontainers.image.description="This docker image installs docker-compose on top of the docker image." \
  org.opencontainers.image.licenses="MIT" \
  org.opencontainers.image.source="https://github.com/tmaier/docker-compose" \
  org.opencontainers.image.title="Docker Compose on docker base image" \
  org.opencontainers.image.vendor="BauCloud GmbH" \
  org.opencontainers.image.version="${DOCKER_VERSION} with docker-compose ${COMPOSE_VERSION}"

```

> 构建自己的compose镜像： `docker build -t my-compose -f Dockerfile.compose .`

---
# 本地compose镜像的使用
```bash

version: '3'
services:
  sut:
    image: my-compose
    environment:
      DOCKER_TLS_CERTDIR: ""
    command: docker pull wurstmeister/zookeeper
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
```
> 本地挂载docker.sock可以跟本机一样操作docker。

---

- [dind](https://github.com/jpetazzo/dind)

```
docker run --name=dind --rm --privileged -d docker:18.09-dind
docker exec -it dind  /bin/sh
```
本地跑起来docker in docker 。进去容器里面发现是一个独立的docker 服务。

表现为：docker ps 没有任何东西.docker pull busybox 会重新拉取。`ls /var/lib/docker/overlay2/` 为空

---

- [making-docker-in-docker-builds-faster-with-docker-layer-caching](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#making-docker-in-docker-builds-faster-with-docker-layer-caching)

这个链接介绍了如何在gitlab上运行。

---

Q: 如何在本地通过docker把结合docker-compose和docker-dind跑起来？
- [docker-image](https://www.caktusgroup.com/blog/2020/02/25/docker-image/)

```bash
version: '3'
services:
  docker:
    image: docker:18.09-dind
    privileged: true
  sut:
    image: my-compose
    environment:
      DOCKER_TLS_CERTDIR: ""
      DOCKER_DRIVER: overlay2
    command:
      - /bin/sh
      - -c
      - |
        docker image ls
        docker pull busybox
        docker image ls
    depends_on:
      - docker

```
```bash

docker-compose -f docker-compose-dind.yml up
#表现为： 第一次镜像为空。重新拉取busybox。然后保存到dind容器里面。

docker-compose -f docker-compose-dind.yml stop
docker-compose -f docker-compose-dind.yml up
#然后如果简单的停止，下次重启后因为dind容器保持了状态，故镜像还在。但是重建了dind容器的话，镜像就没了。

docker-compose -f docker-compose-dind.yml rm docker
docker-compose -f docker-compose-dind.yml up
#重新拉取
```

而且在/var/lib/docker/overlay2/ 里面，每次拉取的hash都是不一样的。所以即使通过volumes挂载镜像层进去也没有用。

```bash
    volumes:
    - ./overlay2:/var/lib/docker/overlay2
```

---

Q： 如何把拉取到的镜像layer层进行打包成新的dind呢？

A: 镜像文件是放在docker容器里面的。/var/lib/docker/overlay2里面的

`docker commit -a "yinzishao" -m "compose with image" dj_docker_1 docker_wi`

但是以上语句的镜像构建，没有把拉下来的镜像打进去。TODO:镜像的数据跟容器内的数据不是一回事。

是因为声明了`Volumes:/var/lib/docker: {}` ?所以镜像忽略了这个目录？

Dockerfile中的VOLUME使每次运行一个新的container时，都会为其**自动创建一个匿名的volume**，如果需要在不同container之间共享数据，那么我们依然需要通过`docker run -it -v my-volume:/foo`的方式将/foo中数据存放于指定的my-volume中。

- [利用 commit 理解镜像构成](https://yeasy.gitbook.io/docker_practice/image/commit)

- [do-not-use-docker-in-docker-for-ci](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)
Q: And what about the build cache? That one can get pretty tricky too. People often ask me, “I’m running Docker-in-Docker; how can I use the images located on my host, rather than pulling everything again in my inner Docker?”

A: 通过cache文件进行/var/lib/docker的缓存？类似requirement.txt的机制。TODO： [Nikola Kovacs](https://gitlab.com/gitlab-org/gitlab-foss/-/issues/17861)

---

- [dind19.03 file](https://github.com/docker-library/docker/tree/b1d2628005e12e79079c025c3653cba248d6f264/19.03/dind)
docker:18.09-dind

```
chmod +x dockerd-entrypoint.sh
docker build -t my-dind --cache-from=my-dind .

> Cannot connect to the Docker daemon at tcp://docker:2375. Is the docker daemon running?

需要在19.03的dind加上：
    environment:
      DOCKER_TLS_CERTDIR: ""
      DOCKER_DRIVER: overlay2
      DOCKER_HOST: tcp://docker:2375/
```

如果把`VOLUME /var/lib/docker` 去掉， overlay2会报错

docker_1  | time="2020-10-31T07:04:03.487053839Z" level=error msg="failed to mount overlay: invalid argument" storage-driver=overlay2

docker_1  | failed to start daemon: error initializing graphdriver: driver not supported


---

# 那就换个思路

先把相关的文件打包到另一个目录。然后通过更改entrypoint进行打包到另一个目录下。

```bash
if [ "`ls -A /var-lib-docker/`" = "" ]; then
    echo "empty"
else
    mv /var-lib-docker/* /var/lib/docker
fi
ls /var/lib/docker
```

my-dind:19.03 添加文件

> 也不太行

---
# health check

新建的dind因为需要移动/var/lib/docker。启动较慢，如何进行健康检查。

/ # curl http://docker:2375
curl: (7) Failed to connect to docker port 2375: Connection refused


---
# 权限问题

19.03-dind、18.09原生就会有这个问题:

mysqld: error while loading shared libraries: libpthread.so.0: cannot stat shared object: Permission denied

- [Mysql, Privileged mode, cannot open shared object file](https://github.com/moby/moby/issues/7512#issuecomment-61787845)

但是上到gitlab ci 上却可以？因为我本机装了mysql的原因

`DOCKER_TLS_CERTDIR: ""` 、 `privileged: true` 配置作用？

docker:18.09-dind、19.03都可以正常启动ES

---
# 自建docker问题

```bash

docker run  --name=dind --privileged  -d registry.umlife.net:443/mt-service/ag-www/dind:2.0.0


error during connect: Get http://docker:2375/v1.40/containers/json: dial tcp: lookup docker on 8.8.8.8:53: no such host


commit 镜像后权限出错

docker run --rm --network host -e "ES_JAVA_OPTS=-Xms256m -Xmx256m" -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:5.5.3

/bin/bash: bin/es-docker: Permission denied

docker run docker.elastic.co/elasticsearch/elasticsearch:5.5.3 ls -ln /usr/share/

drwxr-xr-x 20 0 0 4096 Nov  2 06:06 zoneinfo

ls -ln /var/lib/docker/
drwxr-x---    3 0        0             4096 Nov  2 06:06 network
drwx------   25 0        0             4096 Nov  2 06:22 overlay2

```

> 权限问题？

---
- https://stackoverflow.com/questions/58749344/pre-pull-images-in-docker-in-docker-dind
- [Caching for docker-in-docker builds](https://gitlab.com/gitlab-org/gitlab-foss/-/issues/17861): 根源讨论
- [Docker in Docker (DinD) commit behaviour](https://github.com/docker/for-linux/issues/506): 有一个cache image的例子但实现不了 [例子](https://github.com/elhigu/gitlab-ci-dind-with-image-cache/tree/master/.gitlab-custom-dind)
- [Pulling build cache](https://github.com/moby/moby/issues/20316): build from cache讨论
- [Distributing Docker Cache across Hosts](https://runnable.com/blog/distributing-docker-cache-across-hosts): S3
- [Registry as a pull through cache](https://docs.docker.com/registry/recipes/mirror/): 您可以运行本地注册表镜像，并将所有守护程序指向该目录，以免产生额外的互联网流量。
- [FASTER CI BUILDS WHEN USING DOCKER-IN-DOCKER ON GITLAB](https://joealamo.co.uk/2019/07/28/faster-dind-ci-builds.html): max-concurrent-downloads
- [preloading-images-to-dind-container](https://libraries.io/gitlab/elhigu/preloading-images-to-dind-container): 总结了这个问题！ [preloading-images-to-dind-container](https://gitlab.com/elhigu/preloading-images-to-dind-container)
- [how-can-i-let-the-gitlab-ci-runner-dind-image-cache-intermediate-images](https://stackoverflow.com/questions/35556649/how-can-i-let-the-gitlab-ci-runner-dind-image-cache-intermediate-images): 独立的runner
