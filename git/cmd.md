# alias

```bash
alias git-mm="git fetch origin master && git submodule update && git merge --no-edit origin/master && git push"
```

# fileMode

`git config core.fileMode false`

# 获取最近更改的分支

```bash

git for-each-ref --sort=-committerdate refs/heads/

git for-each-ref --sort=committerdate refs/heads/
```

Or using git branch (since version 2.7.0)

```bash
git branch --sort=-committerdate  # DESC
git branch --sort=committerdate  # ASC
```

---
# 单独删除某个文件的所有历史记录

```bash

git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch elasticsearch/dump.md' --prune-empty --tag-name-filter cat -- --all
```

- [git rm history](https://blog.csdn.net/q258523454/article/details/83899911#commentBox)

---
# Git warning of file overwriting due to (supposedly) untracked files

```bash
ll `git rebase develop 2>&1 | sed "s/^[^\t].*/ /g" `
rm `git rebase develop 2>&1 | sed "s/^[^\t].*/ /g" `
```

---
# 发版本压缩

git flow release finish -S

## public

git flow release finish -p

---
# 回滚

git reflog

---
# 切换标签

```bash

git checkout tag_name

git checkout -b branch_name tag_name
```

---
# 删除没跟踪的文件

```bash
git clean -f

git clean -df
```


```bash
git remote -v                    # 查看远程服务器地址和仓库名称
git remote show origin           # 查看远程服务器仓库状态
git remote add origin git@github.com:username/robbin_site.git         # 添加远程仓库地址
git remote set-url origin git@ github.com:robbin/robbin_site.git # 设置远程仓库地址(用于修改远程仓库地址)
git remote rm <repository>       # 删除远程仓库
```

---
# git branch
* 分支重命名

`git branch -m <oldname> <newname>`


---
# git rm

如下，我把src里的pyc文件全部移除，但是本地文件还保留。

```bash
//-r 包括子目录
//--cached 索引库中删除，并没有删除本机文件
git rm -r -n --cached  */src/\*      //-n：加上这个参数，执行命令时，是不会删除任何文件，而是展示此命令要删除的文件列表预览。

git rm -r --cached  *.pyc      //最终执行命令.

git add -A	//将添加所有改动的已跟踪文件和未跟踪文件。
git commit -m"移除pyc"    //提交

git push origin master   //提交到远程服务器
```

# 删除远程不存在的本地分支

- [参考链接](https://stackoverflow.com/questions/13064613/how-to-prune-local-tracking-branches-that-do-not-exist-on-remote-anymore)

```bash
git branch -r | awk '{print $1}' | egrep -v -f /dev/fd/0 <(git branch -vv | grep origin) | awk '{print $1}' | xargs git branch -d
```

---
# git flow 删除feature分支

```bash
git branch -D feature/brand
#删除后start不成功原因应该是： git flow 存了某个配置
#可以通过git flow feature delete 删除， 但删除后start成功后的记录不是最新的，原因是：
git branch -a | grep brand
#发现本地分支虽然去了，但是远程分支还在
#通过git remote prune origin 删除本地分支不在，远程分支依然存在的分支

git gc --prune=now
```

---
# tag回滚

```bash
git checkout v1.0

git checkout -b


#删除本地tag

git tag -d Remote_Systems_Operation

git push origin :refs/tags/Remote_Systems_Operation

#删除远程分支
git branch -r -d origin/branch-name
git push origin :branch-name
```

---
# status乱码
```bash
git config --global core.quotepath false
```

# cicd
```
  except:
    variables:
    - $CI_COMMIT_MESSAGE =~ /skip-docker-compose-test/
```
commit message 填写跳过compose
