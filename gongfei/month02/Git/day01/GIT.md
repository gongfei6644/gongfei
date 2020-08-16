GIT
==========================

## GIT简介

1. 什么是GIT

> git是一个开源的分布式版本控制系统，用于高效的管理各种大小项目和文件。

2. 代码管理工具的用途

>* 防止代码丢失，做备份
>* 项目的版本管理和控制，可以通过设置节点进行跳转
>* 建立各自的开发环境分支，互不影响，方便合并
>* 在多终端开发是，方便代码的相互传输

3. git的特点

>* git是开源的，多在*nix下使用，可以管理各种文件
>* git是分布式的项目管理工具(svn是集中式的)
>* git数据管理更多样化，分享速度快，数据安全
>* git 拥有更好的分支支持，方便多人协调

4. git安装

> sudo apt-get install git

## GIT使用

![git结构](img/git.jpeg)

### 基本概念

* 工作区：项目所在操作目录，实际操作项目的区域
* 暂存区: 用于记录工作区的工作（修改）内容
* 仓库区: 用于备份工作区的内容
* 远程仓库: 远程主机上的GIT仓库

>注意： 在本地仓库中，git总是希望工作区的内容与仓库区保持一致，而且只有仓库区的内容才能和其他远程仓库交互。

### 初始配置

>配置命令: git config

>* 配置所有用户： git config --system [选项]
>> 配置文件位置:  /etc/gitconfig

>* 配置当前用户： git config --global [选项]
>> 配置文件位置:  ~/.gitconfig

>* 配置当前项目： git config  [选项]
>> 配置文件位置:  project/.git/config

1. 配置用户名

```
e.g. 将用户名设置为Tedu
sudo git config --system user.name Tedu
```

2. 配置用户邮箱

```
e.g. 将邮箱设置为lvze@tedu.cn
git config --global user.email lvze@tedu.cn
```

3. 配置编译器

```
e.g. 配置编译器为pycharm
git config core.editor pycharm

```

4. 查看配置信息

```
git config --list
```

### 基本命令

1. 初始化仓库

> git  init 
> 意义：将某个项目目录变为git操作目录，生成git本地仓库。即该项目目录可以使用git管理

2. 查看本地仓库状态

> git  status
> 说明: 初始化仓库后默认工作在master分支，当工作区与仓库区不一致时会有提示。

3. 将工作内容记录到暂存区

> git add [files..]

```
e.g. 将 a ，b 记录到暂存区
git add  a b

e.g. 将所有文件（不包含隐藏文件）记录到暂存区
git add  *
```

4. 取消文件暂存记录

>  git rm --cached [file] 

5. 将文件同步到本地仓库

> git commit [file] -m [message]
> 说明: -m表示添加一些同步信息，表达同步内容

```
e.g.  将暂存区所有记录同步到仓库区
git commit  -m 'add files'
```

6. 查看commit 日志记录

> git log
> git log --pretty=oneline