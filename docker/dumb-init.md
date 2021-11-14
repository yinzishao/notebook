# dumb-init

- [dumb-init-Docker](https://www.infoq.cn/article/2016/01/dumb-init-Docker)

---
- [Containers: Terminating with grace](https://itnext.io/containers-terminating-with-grace-d19e0ce34290)

bash的exec命令:

`The exec command allows us to execute a command that completely replaces the current process.`


---
# 小结

之前的镜像无法捕获信号是因为即使用了`ENTRYPOINT ["dumb-init", "./entrypoint.sh"]`构建镜像，但是因为entrypoint.sh运行了python命令，相当于又启动了子进程，而sh并不是会传递信号给子进程。

```bash
/home/webapp # ps
PID   USER     TIME  COMMAND
    1 root      0:00 dumb-init ./entrypoint.sh signal --sleep 30
    8 root      0:00 {entrypoint.sh} /bin/sh ./entrypoint.sh signal --sleep 30
   11 root      0:00 python ./manage.py signal --sleep 30
```

直接通过dumb-init运行相关的python命令可以捕获到相关的docker stop信号。

```bash
docker run  --name sync_shop --rm  --entrypoint dumb-init  python-signals  python manage.py signal --sleep 30

PID   USER     TIME  COMMAND
    1 root      0:00 dumb-init python manage.py signal --sleep 30
    8 root      0:00 python manage.py signal --sleep 30

```

**所以entrypoint.sh要通过exec命令启动脚本命令**
