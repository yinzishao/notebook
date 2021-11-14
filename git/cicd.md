# 引用云峰分享

**default**/**variables**/**inherit**

1. `default`(全局设置)
- image
- services
- before_script
- after_script
- tags
- cache
- artifacts
- retry
- timeout
- interruptible

2. `variables`(全局变量)
- global
- job

3. `inherit`
>gitlab 12.9 引入
- 自主选择要继承的全局参数和变量
```yaml
default:
  image: alpine:3.8
  before_script:
  - echo "run in default before_script"

variables:
  NAME: "global variables NAME"
  URL: "global variables URL"

job1:
  inherit:
    default: [image]
    variables: [NAME]
  script:
  - cat .gitlab-ci.yml
  - echo "run in job1"
  - echo $NAME
  - echo $URL
```
合并效果
```yaml
job1:
  image: alpine:3.8
  variables:
    NAME: "global variables NAME"
  script:
  - cat .gitlab-ci.yml
  - echo "run in job1"
  - echo $NAME
  - echo $URL
```

**include**
- local
- file
- remote
- template

```yaml
include:
  - local: &#39;/path/to/.gitlab-ci-template.yml&#39;
  - project: &#39;group/other-project&#39;
    file: &#39;/path/to/.gitlab-ci-template.yml&#39;
  - remote: &#39;https://gitlab.com/awesome-project/raw/master/.gitlab-ci-template.yml&#39;
  - template: Auto-DevOps.gitlab-ci.yml
```
_最多允许100个include，重复的include被视为配置错误，include的解析总时长不能超过30s，否则报错_

**stage**

默认的stages:
  - build
  - test
  - deploy

1. <details><summary>job未指定stage时，跑在哪个stage？</summary><pre><code>test</code></pre></details>
2. 隐藏的.pre和.post
>gitlab 12.4 引入
```yaml
stages:
  - a
  - b

job1:
  stage: .pre
  script:
  - cat .gitlab-ci.yml
  - echo "run in stage .pre"

job2:
  stage: a
  script:
  - cat .gitlab-ci.yml
  - echo "run in stage a"

job3:
  stage: .post
  script:
  - cat .gitlab-ci.yml
  - echo "run in stage .post"

```

_如果除.pre和.post之外没有其它的stage，pipeline不会被创建_

**job**

- image
- stage
- extends
- variables
- before_script
- script
- after_script
- artifacts

_<details><summary>job唯一必须项是？</summary><pre><code>script</code></pre></details>_

**extends**

extends可以同时有多个, 可以合并哈希，但不能合并数组
```yaml
.extends1:
  image: alpine:3.5
  variables:
    V1: "v1 in .extends1"
    V2: "v2 in .extends1"
  only:
  - master
  - tags

.extends2:
  variables:
    V2: "v2 in .extends2"
    V3: "v3 in .extends2"
  script:
  - echo "I&#39;m in extends2"
  only:
  - master

job1:
  extends:
  - .extends1
  - .extends2
  script:
  - echo "I&#39;m in job1"
```
合并结果
```yaml
job1:
  image: alpine:3.5
  variables:
    V1: "v1 in .extends1"
    V2: "v2 in .extends2"
    V3: "v3 in .extends2"
  script:
  - echo "I&#39;m in job1"
  only:
  - master
```

**script**
- <details><summary>命令返回非0还想继续往下执行可以怎么做？</summary><pre><code>false || exit_code=$?</code></pre></details>

**before_script**

_before_script与script是相同的shell环境_

**after_script**
- after_script跟script是不同的shell环境
- after_script超时时间：5分钟（硬编码）
- 如果script执行成功，after_script执行超时或失败，job仍算执行成功

**anchors**
- anchors合并，提升复用度
- 支持job，script，before_script，after_script，variables
```yaml
.job_template: &job_definition
  image: python:3.7

variables: &global-variables
  V1: "v1"

.before: &do_before
- echo "login"

.script: &do_script
- echo "do something"

.after: &do_after
- echo "logout"

job1:
  <<: *job_definition
  variables:
    <<: *global-variables
    V2: "v2"
  before_script:
  - *do_before
  - echo "other before_script"
  script:
  - *do_script
  - echo "do other things"
  after_script:
  - *do_after
  - echo "other after_script"
```
合并结果
```yaml
job1:
  image: python:3.7
  variables:
    V1: "v1"
    V2: "v2"
  before_script:
  - echo "login"
  - echo "other before_script"
  script:
  - echo "do something"
  - echo "do other things"
  after_script:
  - echo "logout"
  - echo "other after_script"
```
_利用include功能时，不能在多个文件中使用anchors，仅在定义它们的文件内有效_

**rules**
>gitlab 12.3 引入
- workflow:rules
一种设置管道策略的方法，确定是否创建管道
  - if: 定义规则
  - when: always或never
```yaml
workflow:
  rules:
  - if: $CI_COMMIT_MESSAGE =~ /^wip/
    when: never
  - if: $CI_COMMIT_MESSAGE =~ /skip-pipeline/
    when: never
  - when: always
```
- job:rules
一种设置作业策略的方法，确定是否将作业添加到管道
  - if: 定义规则
  - when: always，never，on_success，delayed
  - changes: 文件变更
  - exists: 文件存在
  - allow_failure: 允许失败
```yaml
job1:
  rules:
  - if: $CI_COMMIT_MESSAGE =~ /build golang/
    when: on_success
    changes:
    - *.go
  - if: $CI_COMMIT_MESSAGE =~ /build python/
    exists: .test_success
    allow_failure: true
```
_rules:allow_failure覆盖job级allow_failure_

**needs**
>gitlab 12.2 引入
- 无需等待阶段顺序即可运行某些作业
```yaml
stages:
- a
- b

job1:
  stage: a
  script:
  - echo "do job1"

job2:
  stage: a
  script:
  - echo "do job2"

job3:
  stage: b
  script:
  - echo "do job3"
  needs: ["job1"]
```
[运行示例](https://git.umlife.net/guanyunfeng/gitlabci-test/-/blob/needs/.gitlab-ci.yml)

- _不能指向因only/except规则而未实例化的job_
- _支持数组，默认全局最多10个_
- _只能needs之前阶段的作业，不能needs本阶段的job（已有计划支持此功能）_
- _设置artifacts: true/false自主控制是否下载artifacts_
- _支持从当前项目其它分支甚至其它项目下载artifacts，最多5个artifacts_

```yaml
job3:
  needs:
  - job: job1
    artifacts: false
  - project: group2/project2
    job: job2
    ref: master
    artifacts: true
```

**when**
- always
- on_success
- on_failure
- manual
- delayed

设置when: manual+allow_failure: false，阻塞式作业，实现审批功能，经过批准后才能继续执行pipeline后续job

[运行示例](https://git.umlife.net/guanyunfeng/gitlabci-test/-/blob/when/.gitlab-ci.yml)

_支持自定义设置哪些用户有可执行when: manual的权限（通过environment的allowed to deploy设置）_
```yaml
deploy:
  stage: deploy
  script:
  - echo "deploy to production server"
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
  - master
```

**trigger**
- 在job中触发指定yaml中的pipeline
```yaml
trigger_job:
  trigger:
    include: path/to/child-pipeline.yml
```
- 在job中触发其它项目的pipeline，实现多项目协同作业
```yaml
trigger_job:
  trigger:
    project: group/project
    strategy: depend
```
_设置strategy: depend以等待被触发的pipeline执行完，并且将被触发的pipeline的执行状态作为自己的执行状态_

**resource_group**
>gitlab 12.7 引入
- 有时在环境中同时运行多个作业或管道可能会导致出错，如部署过程
- 定义resource_group key，确保Runner不会同时运行某些作业
```yaml
deploy-to-production:
  script: deploy
  resource_group: production
```
_属于相同resource_group的多个作业同时进入队列时，仅有一个能运行，其它的将等待_

<details>
<summary>dj项目ci运行慢的一些调优建议：</summary>
<pre><code>
1. 大job拆分
2. 有变化才运行
3. 善用needs抢跑
</code></pre>
</details>

<details>
<summary>随堂小练习</summary>

```yaml
default:
  image: alpine:3.8
  before_script:
  - echo "run in default before_script"

variables:
  NAME: "[global-name]"
  URL: "[global-url]"
  DOMAIN: "[global-domain]"

.hidden_job1:
  image: alpine:3.5
  variables:
    URL: "[.hidden_job1-url]"
  after_script:
  - echo ".hidden_job1 after_script"

.hidden_job2:
  variables:
    URL: "[.hidden_job2-url]"
  script:
    - echo ".hidden_job2 script"
  after_script:
  - echo ".hidden_job2 after_script"

job1:
  extends:
  - .hidden_job1
  - .hidden_job2
  inherit:
    default: [image]
    variables: [NAME]
  script:
  - echo "job1 script NAME:$NAME, URL:$URL, DOMAIN:$DOMAIN"
```
job1的最终合并结果是？
</details>

<details>
<summary>选项</summary>

```yaml
A
job1:
  image: alpine:3.5
  variables:
    NAME: "[global-name]"
    URL: "[.hidden_job2-url]"
  before_script:
  - echo "default before_script"
  script:
  - echo "job1 script NAME:$NAME, URL:$URL, DOMAIN:$DOMAIN"
  after_script:
  - echo ".hidden_job2 after_script"

B
job1:
  image: alpine:3.5
  variables:
    NAME: "[global-name]"
    URL: "[.hidden_job2-url]"
  script:
  - echo "job1 script NAME:$NAME, URL:$URL, DOMAIN:$DOMAIN"
  after_script:
  - echo ".hidden_job1 after_script"
  - echo ".hidden_job2 after_script"

C
job1:
  image: alpine:3.5
  variables:
    NAME: "[global-name]"
    URL: "[.hidden_job2-url]"
  script:
  - echo "job1 script NAME:$NAME, URL:$URL, DOMAIN:$DOMAIN"
  after_script:
  - echo ".hidden_job2 after_script"

D
job1:
  image: alpine:3.5
  variables:
    NAME: "[global-name]"
    URL: "[.hidden_job2-url]"
    DOMAIN: "[global-domain]"
  script:
  - echo "job1 script NAME:$NAME, URL:$URL, DOMAIN:$DOMAIN"
  after_script:
  - echo ".hidden_job1 after_script"
  - echo ".hidden_job2 after_script"
```
</details>

<details>
<summary>答案</summary>
<pre><code>C</code></pre>
</details>
