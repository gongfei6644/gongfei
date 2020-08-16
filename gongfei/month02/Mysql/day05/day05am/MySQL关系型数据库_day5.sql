课程：MySQL关系型数据库
进度: day5

存储引擎
1. 什么是存储引擎：表的物理实现方式，由于物理
   实现不一样，决定不同存储引擎类型的技术特性
   不一样，例如：存储机制，索引机制，锁定方式
2. 查看存储引擎
1）查看MySQL支持的存储引擎:show engines;
2）查看某个表的存储引擎
   show CREATE TABLE 表名称;
3）修改表的存储引擎
   ALTER TABLE 表名称 engine = 引擎名称;
4）示例：创建表，并修改存储引擎
   CREATE TABLE t3 (
     id INT PRIMARY key,
	 name VARCHAR(32)
   ) engine = InnoDB;
   ALTER TABLE t3  engine=MyISAM;
   查看：show CREATE TABLE t3;

3.常用存储引擎特点
1）InnoDB(MySQL5.5及以后的版本默认)
  - 特点：支持事务、支持行级锁、支持外键、
        共享表空间

  - 文件构成：
    *.frm: 表的结构、索引
	*.ibd: 表的数据

  - 实验：查看表的存储文件
  说明：通过下面的指令可以查看数据存储目录
  show global variables like '%datadir%';

  如果权限不够，使用sudo -i 进入root用户，
  进入上面的目录查看

  cd /var/lib/mysql
  ls orders.*  (查看orders表的存储文件)

  - 什么时候选用InnoDB:
    更新(增删改)操作密集的表；
	要求支持数据库事务、外键；
	自动灾备和恢复；
	要求支持自动增长(auto_increment)字段；

  - MyISAM
  特点：支持表级锁定；不支持事务、外键、行锁定
        独占表空间；该类存储引擎容易损坏，所以
		灾备、恢复性能不佳
  文件构成：
    *.frm: 表结构
	*.myd: 数据
	*.myi: 表索引
  适用场合：
    查询请求较多；
	数据一致性要求较低；
	没有外键约束要求；

  - Memory
  特点：表结构存与磁盘，数据存在内存中
        服务器重启或断电后，表中的数据丢失
  文件：*.frm   表结构
  使用场合：数据量小；数据需要快速访问；
            数据丢失不会造成损失；
  实验：
  第一步：修改t3的存储引擎为Memory
    ALTER TABLE t3 engine=Memory;
  第二步：查看文件
    sudo -i
	cd /var/lib/mysql/eshop
	ls t3.*
  第三步：插入一条数据，查询(可以看到数据)
    insert into t3 values(1,'Jerry');
  第四步：重启服务，再查询（数据消失）
    /etc/init.d/mysql restart

pymysql库使用
1. 确认pymysql库已经安装
  进入python交互模式，执行: import pymysql
  如果不报错说明已安装
 
  如果报错，更换到教学机
  建orders表，SQL参照第一天的内容

2. 删除orders表多余的数据
  DELETE FROM orders 
  WHERE cust_id > 'C00000005';









