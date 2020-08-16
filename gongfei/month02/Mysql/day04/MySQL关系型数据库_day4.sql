课程：MySQL关系型数据库
进度：day4

今天的内容

索引（重点）
1. 什么是索引：提高查询效率的一种技术
2. 原理：根据某一列（字段）进行分段、排序，通过避免
   全表扫描提高查询效率
3. 索引分类
1）普通索引、唯一索引
  普通索引：MySQL基本类型，字段值可以重复
  唯一索引：字段的值不能重复（可以为空）
2）单列索引、组合索引
  单列索引：一个索引只包含一个字段
  组合索引：一个索引包含多个字段
3）聚集索引、非聚集索引
  聚集索引(Cluster Index): 索引的键值顺序和数据
     顺序是一致的
  非聚集索引：索引的键值顺序和数据
     顺序不一致的
4）如何创建索引
  - 语法：index | UNIQUE | PRIMARY KEY
  - 示例：创建index_test表，在name字段上建立普通索引
          在cert_no上建立唯一索引
    CREATE TABLE index_test(
	  id INT PRIMARY key, 
	  cert_no VARCHAR(32),
	  name VARCHAR(32),
	  UNIQUE(cert_no), INDEX(name)
	);
    查看索引：show INDEX FROM index_test;
    INSERT INTO index_test 
	  VALUES(1,'0001', 'Jerry');
    INSERT INTO index_test 
	  VALUES(2,'0001', 'Jerry'); -- cert_no违反约束

5）删除索引
  - 语法：drop INDEX 索引名称 ON 表名称;
  - 示例：
    -- 删除cert_no
    DROP INDEX cert_no ON index_test; 
	-- 删除名称为name的索引
    DROP INDEX name ON index_test; 
6）修改表的方式添加索引
  - 语法: CREATE 索引类型 索引名称 ON 表(字段)
  - 示例：
    -- 在index_test表cert_no字段创建唯一索引
    CREATE UNIQUE INDEX idx_cert_no
	ON index_test(cert_no);

7）实验：索引效率测试（20分钟）
第一步：利用现有的orders表，插入10万笔数据
        执行insert_orders_many.py文件
第二步：在没有索引的情况下查询，条件如下：
        order_id = '2018010100000002'
        order_id = '2018010100055555'
        order_id = '2018010100099996'
第三步：给orders表添加索引
     CREATE INDEX idx_order_id ON orders(order_id)
	 再执行第二步的查询，查看执行时间
备注: 如果执行文件报错，检查连接参数
      核对字段的名称、顺序、类型
	  pymysql导入出错，因为缺少了pymysql模块，更换
	  到教学机上执行

8）索引的优缺点
  - 优点
    提高查询效率
	唯一索引能够保证数据的唯一性
	可能提高分组、排序的效率
  - 缺点
    降低增、删、改的效率（调整索引结构的开销）
	对表中的数据进行增删改操作，需要调整索引结构

	需要增加额外的存储空间

9）索引使用注意事项
  - 总体原则
    在合适的字段上，建立合适的索引
	索引不能太多，过多的索引会降低增删改效率
  - 适合使用索引的情况
    在经常进行查询、排序、分组的字段上建立索引
	数据分布比较均匀、连续的字段，适合建立索引
	查询操作较多的表，适合建立索引
  - 不适合建立索引的情况
    数据量太少的表不适合建立索引
	增删改操作较多的表，不适合建立较多的索引
	某个字段取值范围很少，不适合建索引
	某个字段很少用作查询、排序、分组，不适合建索引
	二进制字段不适合建立索引

10）索引失效的SQL语句
  索引失效：表中有索引，但是查询时候没有使用

  - 没有使用索引字段作为条件，会导致放弃使用索引
  - 条件判断中使用了<>符号，会导致放弃使用索引
  - 条件判断语句中使用了null值判断，会导致放弃使用索引
  - 模糊查询%前置，会导致放弃使用索引
  - 对字段做运算，会导致放弃使用索引

数据库事务（重点）
1. 什么是事务：指数据库执行的一组操作（增删改）
   要么全都执行，要么全都不执行
2. 作用：保证数据的一致性、完整性
3. 事务的特点（ACID特性）（重点）
1）原子性(Atomicity)：一个事务是不可分割的整体，
   要么全都执行，要么全都不执行
2）一致性(Consistency)：事务执行完成后，数据库
  从一个一致性状态变成下一个一致性状态
3）隔离性(Isolation)：不同的事务不会相互影响
4）持久性(Durability)：一旦事务提交，对数据库的
  修改会被持久保存到磁盘中

5）示例
  第一步：创建测试账户表并添加测试账号
  CREATE TABLE acct(
    acct_no VARCHAR(32),
    acct_name VARCHAR(32),
    balance DECIMAL(16,2)
  );
  
  INSERT INTO acct VALUES
  ('0001','Jerry',1000),('0002','Tom',2000);

  第二步：通过事务操作语句，观察事务提交、回滚的作用
  start transaction;  -- 启动事务
  UPDATE acct SET balance = balance - 100
    WHERE acct_no = '0001';  -- 模拟扣付款人的金额
  UPDATE acct SET balance = balance + 100
    WHERE acct_no = '0002';  -- 模拟给收款人加金额
  commit;   -- 事务提交，所修改的数据正式生效
  -- rollback;  -- 第二次，模拟事务回滚

  -- 在执行commit之前，重新开启一个mysql的客户端，
  -- 查询acct表的余额（查看事务的隔离性）

6）如何操作事务
  - 启动事务
    显式启动：start TRANSACTION;
	隐式启动：执行insert,update,delete操作
  - 提交事务：commit;
  - 回滚：rollback;

7）使用事务的情况及先决条件
  - 先决条件：InnoDB存储引擎支持事务
  - 使用事务的情况：
    一个操作涉及一组SQL语句（增删改语句）
	需要这一组操作完成后，保证数据的一致性、完整性
  
8）事务对效率的影响：数据库事务降低数据库的性能
   原因是为了保证数据的一致性、事务的隔离性，
   事务需要对数据进行加锁；如果有其它事务需要
   操作这部分加锁的数据，必须等待上一个事务
   结束（提交、回滚）

9）事务对哪些语句起作用
  SQL语句按照功能可以分为4类：
  - 数据查询语言(DQL): 查询数据，不会修改数据
  - 数据定义语句(DDL)：定义库/表/索引
  - 数据操作语言(DML)：对数据进行增、删、改
    （数据库事务只对这一类语言起作用）
  - 数据控制语言(DCL): 授权/吊销权限，事务管理

权限管理
1. 什么是权限：用户可以执行哪些操作
2. 权限分类
1）用户类：创建/删除/修改用的权限
   给其他用户授权的权限
2）库/表操作：建库/删库/修改库的权限
   建表/删表/修改表的权限
3）数据操作：增删改查

3. 权限相关的表
1）user: 最重要的一个系统表，存储了用户、密码
   以及用户所拥有的权限
2）db: 记录了库的授权信息
3）table_priv: 记录表的授权信息
4）column_priv：记录对字段的授权信息

4. 权限操作
1）授予权限
 - 语法：
   GRANT 权限列表 ON 库名.表名
   TO '用户名'@'客户端地址'
   [identified BY '密码']
   [WITH GRANT option];
 - 说明
   权限列表：表示授予哪些权限
     ALL privileges: 所有权限
	 select: 只授予查询权限
	 select,insert: 授予查询、插入权限
   库名.表名：
     *.*:  所有库下的所有表
	 bank.*: bank库下所有表
	 bank.acct: bank库下的acct表授权
   客户端
     %: 表示所有的客户端（任意机器）
	 localhost: 表示只能从本机登录
	 192.168.1.5: 表示只能从指定的IP机器登录
   identified BY '密码'：设置用户密码
   WITH GRANT option：用户是否有授权的权限

  - 示例：创建Tom用户，只授予eshop库下所有表
    的查询权限
   -- 第一步：创建Tom用户并授权
   GRANT SELECT ON eshop.*
   TO 'Tom'@'%' identified BY '123456';
   -- select * from mysql.db where User='Tom'\G;
   -- 第二步：刷新权限生效
   flush privileges;
   -- 第三步：使用Tom用户登录，执行一下操作
   进入mysql库，失败
   进入eshop库，成功
   在eshop中执行查询，成功
   在eshop中执行增删改，失败

  - 练习：创建Jerry用户，能对eshop库下所有表
    进行增删改查，并且将密码设置为'123456',
	限定只能从本机登录数据库
    GRANT select,insert,update,DELETE
	ON eshop.* 
	TO 'Jerry'@'localhost'
	identified BY '123456';
2）吊销权限
  - 语法：
    REVOKE 权限列表 ON 库名.表名
	FROM '用户名'@'客户端地址';
  - 示例：吊销Jerry用户eshop库下所有表的
    删除权限
	REVOKE DELETE ON eshop.*
	FROM 'Jerry'@'localhost';
	-- 刷新权限后，重新用Jerry登录验证
3）查看权限
  - 查看自己权限：show grants;
  - 查看别人的权限：show grants FOR 'Tom'@'%';

锁（理解）
1. 概念：对某个范围的控制(操作)权
2. 目的：解决两个或多个工作单元并发操作数据
   引发的问题
3. 分类
  - 锁类型
  读锁(共享锁)：select操作加锁，可以进行数据
	            读取，但是不能写入
  写锁(排它锁)：insert/update/delete时加锁，
                加锁后的数据不能读、写

  - 锁粒度(锁定范围)
  行级锁（细粒度）：锁定一行，并发效率高，资源消耗多
  表级锁（粗粒度）：锁定一个表，并发效率低，资源消耗少



