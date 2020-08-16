## redis 数据库下载配置启动文件

### 1.下载安装redis数据库。

我们在ubuntu虚拟机中可以去下载redis，稳定版的链接如下：

​	step1:

```
wget http://download.redis.io/releases/redis-3.2.8.tar.gz
```

​	step2:解压

```
tar -zxvf redis-3.2.8.tar.gz
```

​	step3:复制到redis目录下边：

```
sudo mv ./redis-3.2.8 /usr/local/redis/
```

​	step4进入到目录中，进行编译文件

```
cd /usr/local/redis
sudo make # 进行编译
```

​	step5:进行测试

```
sudo make test # 测试相关依赖关系
```

​	step6:进入到安装目录下面

```
cd /usr/local/bin
通过ls可以查看到其安装目录文件
```

​	step7：配置文件，移动到/etc目录下

```
将配置文件拷贝到etc目录下：(此文件所在目录是/usr/local/redis)
sudo cp redis.conf /etc/redis/redis.conf
```

### 2.配置redis数据库。

配置文件的路径是：**/etc/local/redis.conf**

```0
配置redis数据库，首先需要进入redis数据库配置文件
sudo vim /etc/redis/redis.conf
你需要注意修改一下参数：
绑定IP：如果需要远程访问，可以将此行进行注释，或者绑定一个真实IP
	
	bind 127.0.0.1

端口：默认为6379
  
  port 6379

是否以守护进程运行：
	如果以守护进程运行，则不会在命令行阻塞，类似于服务
	如果以非守护进程运行，则在当前终端被阻塞
	设置为yes表述守护进程，设置为no表示非守护进程，
	建议设置为：yes
	
	deamonize yes

数据文件：在进行数据持久化的时候将数据写入到那个文件中。
	
	dbfilename dump.rdb

数据文件的存储路径：
	
	dir /var/lib/redis

日志文件
	logfile /var/log/redis/redis-server.log
	
数据库，默认有16个，编号是0-15

	database 16
	
主从复制

	slaveof
```

### 3.启动redis数据库。

#### 服务端

服务器端的命令是redis-server

可以使用help查看帮助文档

> Redis-server —help

建议使用以下命令来管理redis服务

​	启动

	>sudo service redis start

​	停止

	>sudo service redis stop

​	重启

	> sudo service redis restart

```
也可以根据以下命令启动数据库服务，要明确的是你安装redis数据库的配置文件的位置
sudo redis-server /etc/redis/redis.conf
```

#### 客户端

>客户端使用的命令是 redis-cli
>
>可以使用help来查看文档 redis-cli —help

连接redis：

	> redis-cli

运行测试命令：

> ping

切换数据库：

> 数据库没有名称，默认有16个，通过0-15来标识，连接redis默认选择第一个数据库
>
> select n

