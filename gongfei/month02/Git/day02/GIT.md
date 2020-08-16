GIT
==========================

[TOC]

## GIT���

1. ʲô��GIT

> git��һ����Դ�ķֲ�ʽ�汾����ϵͳ�����ڸ�Ч�Ĺ�����ִ�С��Ŀ���ļ���

2. ��������ߵ���;

>* ��ֹ���붪ʧ��������
>* ��Ŀ�İ汾����Ϳ��ƣ�����ͨ�����ýڵ������ת
>* �������ԵĿ���������֧������Ӱ�죬����ϲ�
>* �ڶ��ն˿���ʱ�����������໥����

3. git���ص�

>* git�ǿ�Դ�ģ�����*nix��ʹ�ã����Թ�������ļ�
>* git�Ƿֲ�ʽ����Ŀ������(svn�Ǽ���ʽ��)
>* git���ݹ�����������������ٶȿ죬���ݰ�ȫ
>* git ӵ�и��õķ�֧֧�֣��������Э��

4. git��װ

> sudo apt-get install git

## GITʹ��

![git�ṹ](img/git.jpeg)

### ��������

* ����������Ŀ���ڲ���Ŀ¼��ʵ�ʲ�����Ŀ������
* �ݴ���: ���ڼ�¼�������Ĺ������޸ģ�����
* �ֿ���: ���ڱ��ݹ�����������
* Զ�ֿ̲�: Զ�������ϵ�GIT�ֿ�

>ע�⣺ �ڱ��زֿ��У�git����ϣ����������������ֿ�������һ�£�����ֻ�вֿ��������ݲ��ܺ�����Զ�ֿ̲⽻����

### ��ʼ����

>��������: git config

>* ���������û��� git config --system [ѡ��]
>> �����ļ�λ��:  /etc/gitconfig

>* ���õ�ǰ�û��� git config --global [ѡ��]
>> �����ļ�λ��:  ~/.gitconfig

>* ���õ�ǰ��Ŀ�� git config  [ѡ��]
>> �����ļ�λ��:  project/.git/config

1. �����û���

```
e.g. ���û�������ΪTedu
sudo git config --system user.name Tedu
```

2. �����û�����

```
e.g. ����������Ϊlvze@tedu.cn
git config --global user.email lvze@tedu.cn
```

3. ���ñ�����

```
e.g. ���ñ�����Ϊpycharm
git config core.editor pycharm

```

4. �鿴������Ϣ

```
git config --list
```

### ��������

1. ��ʼ���ֿ�

> git  init 
> ���壺��ĳ����ĿĿ¼��Ϊgit����Ŀ¼������git���زֿ⡣������ĿĿ¼����ʹ��git����

2. �鿴���زֿ�״̬

> git  status
> ˵��: ��ʼ���ֿ��Ĭ�Ϲ�����master��֧������������ֿ�����һ��ʱ������ʾ��

3. ���������ݼ�¼���ݴ���

> git add [files..]

```
e.g. �� a ��b ��¼���ݴ���
git add  a b

e.g. �������ļ��������������ļ�����¼���ݴ���
git add  *
```

4. ȡ���ļ��ݴ��¼

>  git rm --cached [file] 

5. ���ļ�ͬ�������زֿ�

> git commit [file] -m [message]
> ˵��: -m��ʾ���һЩͬ����Ϣ�����ͬ������

```
e.g.  ���ݴ������м�¼ͬ�����ֿ���
git commit  -m 'add files'
```

6. �鿴commit ��־��¼

> git log
> git log --pretty=oneline

7. �ȽϹ������ļ��Ͳֿ��ļ�����

> git diff  [file]

8. �����������ļ��޸�

> git checkout -- [file]

9. �Ӳֿ����ָ��ļ�

> git checkout [file]

10 �ƶ�����ɾ���ļ�

> git  mv  [file] [path]
> git  rm  [files]
> ע��: �������������޸Ĺ��������ݣ�ͬʱ��������¼�ύ���ݴ�����


### �汾����

1. �˻ص���һ��commit�ڵ�

> git reset --hard HEAD^
> ע�� �� һ��^��ʾ����1���汾���������ơ����汾����֮���������Զ��͵�ǰcommit�汾����һ��

2. �˻ص�ָ����commit_id�ڵ�

> git reset --hard [commit_id]

3. �鿴���в�����¼

>git reflog
>ע��:�������Ϊ���¼�¼����������commit_idȥ���κβ���λ��

4. ������ǩ

>��ǩ: ����Ŀ����Ҫcommitλ����ӿ��գ����浱ʱ�Ĺ���״̬��һ�����ڰ汾�ĵ�����

> git  tag  [tag_name] [commit_id] -m  [message]
> ˵��: commit_id���Բ�д��Ĭ�ϱ�ǩ��ʾ���µ�commit_idλ�ã�messageҲ���Բ�д�����������ӡ�

```
e.g. �����µ�commit����ӱ�ǩv1.0
git tag v1.0 -m '�汾1'
```

5. �鿴��ǩ

>git tag  �鿴��ǩ�б�
>git show [tag_name]  �鿴��ǩ��ϸ��Ϣ

6. ȥ��ĳ����ǩ�ڵ�

> git reset --hard [tag]

7. ɾ����ǩ

> git tag -d  [tag]


### ���湤����

1.  ���湤��������

> git stash save [message]
> ˵��: ��������δ�ύ���޸ķ�棬�ù������ص��޸�ǰ��״̬

2. �鿴�������б�

> git stash  list
> ˵��:���±���Ĺ�������������

3. Ӧ��ĳ��������

> git stash  apply  [stash@{n}]

4. ɾ��������

> git stash drop [stash@{n}]  ɾ��ĳһ��������
> git stash clear  ɾ�����б���Ĺ�����


### ��֧����

>����: ��֧��ÿ������ԭ�д��루��֧���Ļ����Ͻ����Լ��Ĺ��������������������������š���ɿ����������ٽ��з�֧ͳһ�ϲ���

1. �鿴��֧���

> git branch
> ˵��: ǰ��� * �ķ�֧��ʾ��ǰ������֧

2. ������֧

> git branch [branch_name]
> ˵��: ����a��֧����b��֧����ʱb��֧��ӵ��a��֧ȫ�����ݡ��ڴ���b��֧ʱ��ñ���a��֧"�ɾ�"״̬��

3. �л�������֧

> git checkout [branch]
> ˵��: 2,3����ͬʱ���������������л���֧
>> git checkout -b [branch_name]

4. �ϲ���֧

> git merge [branch]

> ��ͻ�����Ǻϲ���֧��������Ϊ���ֵ�����
>> ����֧�ϲ�ʱ��ԭ��֧����ǰ�����˱仯�ͻ������ͻ
>> ���ϲ���֧ʱ����µ�ģ�飨�ļ��������ֳ�ͻ�����Զ������ֻ���Լ�����commit�������ɡ�
>> ���ϲ���֧ʱ������֧�޸���ͬһ���ļ�������Ҫ�ֶ������ͻ��

5. ɾ����֧

> git branch -d [branch]  ɾ����֧
> git branch -D [branch]  ɾ��û�б��ϲ��ķ�֧


### Զ�ֿ̲�

1. ʲô��Զ�ֿ̲�

> Զ�������ϵ�git�ֿ⡣ʵ����git�Ƿֲ�ʽ�ṹ��ÿ̨������git�ֿ�ṹ���ƣ�ֻ�ǰѱ��������ϵ�git�ֿ��ΪԶ�ֿ̲⡣

2. ����ֿ�

> ��git�ֿ���bare����ΪTrue�Ĺ���ֿ���Ժܺõĺ�Զ�ֿ̲���н���

�������裺

* ѡ����ֿ�Ŀ¼������Ŀ¼��������Ϊ��ǰ�û�

```
mkdir gitrepo
chown tarena:tarena gitrepo
```

* ����Ŀ¼��ʼ��Ϊgit����Ŀ¼��������teduΪ�Լ�ȡ����Ŀ���ƣ�.gitΪͨ�ý�β��׺

```
cd gitrepo
git init --bare tedu.git
```

* ��git����Ŀ¼����ĿĿ¼����Ϊ��ͬ������

```
chown -R tarena:tarena tedu.git
```

#### Զ�ֿ̲��������

���в����ڱ���git�ֿ��½���

1. ���Զ�ֿ̲�

```
git remote  add origin tarena@127.0.0.1:/home/tarena/gitrepo/tedu.git
```

2. ɾ��Զ������

>git remote rm [origin]

3. �鿴���ӵ�����

>git remote�ɶ�
>ע��: һ��git��Ŀ���ӵ�Զ�������������ظ�

4. �����ط�֧���͸�Զ�ֿ̲�

```
��master��֧���͸�origin����Զ�ֿ̲⣬��һ�����ͷ�֧ʹ��-u��ʾ��Զ�̶�Ӧ��֧�����Զ�����
git push -u origin  master
```

5. ɾ��Զ�̷�֧

> git branch -a  �鿴���з�֧
> git push origin  [:branch]  ɾ��Զ�̷�֧

6. �������ͷ���

> git push --force origin  ���ڱ��ذ汾��Զ�̰汾��ʱǿ�����ͱ��ذ汾

> git push origin [tag]  ���ͱ��ر�ǩ��Զ��

7. ��Զ�̻�ȡ��Ŀ

```
git clone tarena@127.0.0.1:/home/tarena/gitrepo/tedu.git
```

> ע�⣺ ��ȡ�����ص���Ŀ���Զ���Զ�ֿ̲⽨�����ӡ��һ�ȡ����Ŀ����Ҳ�Ǹ�git��Ŀ��

8. ��Զ�̻�ȡ����

> git pull 

> ��Զ�̷�֧master��ȡ�����أ���Ϊtmp��֧
> git fetch origin  master:tmp  

> ����
>> pull��Զ������ֱ����ȡ�����أ����Ͷ�Ӧ��֧���ݽ��кϲ�
>> fetch��Զ�̷�֧������ȡ�����أ����ǲ���ͱ��ض�Ӧ��֧�ϲ��������Լ��жϺ���ʹ��merge�ϲ���


## GitHubʹ��

1. ����

>github��һ����Դ����Ŀ������վ��ӵ��ȫ�����Ŀ�Դ��Ŀ�������߿���ע����վ��github�����Լ�����Ŀ�ֿ⡣

>��ַ�� github.com

>��������ߣ�git







�� github ����� SSH key �Ĳ��裺
1��������Ҫ���������Ƿ��Ѿ��� SSH key 
���� git Bash �ͻ��ˣ��������´��룺

$ cd ~/.ssh
$ ls
������������Ǽ���Ƿ��Ѿ����� id_rsa.pub �� id_dsa.pub �ļ�������ļ��Ѿ����ڣ���ô�������������2��ֱ�ӽ��벽��3��

 

2������һ�� SSH key 
$ ssh-keygen -t rsa -C "your_email@example.com"
����������壺

-t ָ����Կ���ͣ�Ĭ���� rsa ������ʡ�ԡ�
-C ����ע�����֣��������䡣
-f ָ����Կ�ļ��洢�ļ�����

���ϴ���ʡ���� -f ��������ˣ���������������������������һ���ļ��������ڱ���ղ����ɵ� SSH key ���룬�磺

Generating public/private rsa key pair.
# Enter file in which to save the key (/c/Users/you/.ssh/id_rsa): [Press enter]
��Ȼ����Ҳ���Բ������ļ�����ʹ��Ĭ���ļ������Ƽ�������ô�ͻ����� id_rsa �� id_rsa.pub ������Կ�ļ���

 

�����ֻ���ʾ�������������루����������push�ļ���ʱ��Ҫ��������룬������github�����ߵ����룩��

��Ȼ����Ҳ���Բ��������룬ֱ�Ӱ��س�����ôpush��ʱ��Ͳ���Ҫ�������룬ֱ���ύ��github���ˣ��磺

Enter passphrase (empty for no passphrase): 
# Enter same passphrase again:
���������ͻ���ʾ���´�����ʾ���磺

Your identification has been saved in /c/Users/you/.ssh/id_rsa.
# Your public key has been saved in /c/Users/you/.ssh/id_rsa.pub.
# The key fingerprint is:
# 01:0f:f4:3b:ca:85:d6:17:a1:7d:f0:68:9d:f0:a2:db your_email@example.com
���㿴��������δ�����գ��Ǿ�˵������� SSH key �Ѿ������ɹ�����ֻ��Ҫ��ӵ�github��SSH key�ϾͿ����ˡ�

 

3�������� SSH key �� github����ȥ
a����������Ҫ���� id_rsa.pub �ļ������ݣ�������ñ༭�����ļ����ƣ�Ҳ������git����Ƹ��ļ������ݣ��磺

$ clip < ~/.ssh/id_rsa.pub
b����¼���github�˺ţ������Ͻǵ����ã� Account Settings �����룬Ȼ�����˵����� SSH key ����ҳ����� SSH key��

c����� Add SSH key ��ť���һ�� SSH key �����㸴�Ƶ� SSH key ����ճ���� key ����Ӧ��������У��ǵ� SSH key �����ǰ��Ҫ���пո���߻س�����Ȼ������� Title ����Ӧ���������Ҳ��������һ���� SSH key ��ʾ�� github �ϵ�һ��������Ĭ�ϵĻ�ʹ������ʼ����ơ�

 

4������һ�¸�SSH key
��git Bash ���������´���

$ ssh -T git@github.com
�����������ϴ���ʱ������һ�ξ�����룬�磺

The authenticity of host 'github.com (207.97.227.239)' can't be established.
# RSA key fingerprint is 16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48.
# Are you sure you want to continue connecting (yes/no)?
���������ģ������� yes �س��ȿɡ�����㴴�� SSH key ��ʱ�����������룬�������ͻ���ʾ���������룬�磺

Enter passphrase for key '/c/Users/Administrator/.ssh/id_rsa':
��Ȼ�������������ˣ�����Ҫ�������룬֪������Ϊֹ��

ע�⣺��������ʱ������һ���־ͻ᲻��ȷ��ʹ��ɾ�������޷������ġ�

������ȷ����ῴ��������λ����磺

Hi username! You've successfully authenticated, but GitHub does not
# provide shell access.
����û�������ȷ��,���Ѿ��ɹ�����SSH��Կ������㿴�� ��access denied�� ���߱�ʾ�ܾ����ʣ���ô�����Ҫʹ�� https ȥ���ʣ������� SSH ��





https �� SSH ������
1��ǰ�߿��������¡github�ϵ���Ŀ����������˭�ģ��������������������Ҫ��¡����Ŀ��ӵ���߻����Ա������Ҫ����� SSH key �������޷���¡��

2��https url ��push��ʱ������Ҫ��֤�û���������ģ��� SSH ��push��ʱ���ǲ���Ҫ�����û����ģ��������SSH key��ʱ�����������룬����Ҫ��������ģ�����ֱ���ǲ���Ҫ��������ġ�






