课程：MySQL关系型数据库
进度：day2

上次内容回顾
1. 基本概念
1）数据库：按照一定理论模型
   科学、高效对数据进行管理的仓库
2）DBMS：数据库管理系统，专门用于数据管理的
   软件，功能主要有：快速数据存取；数据安全
   性、可靠性；备份/恢复工具、性能、友好的
   用户界面、丰富的程序接口
3）主流关系型数据库：Oracle, MySQL, SQL Server,
   DB2
4）数据管理三个阶段：人工阶段，文件管理，
   数据库管理阶段
5）概念模型：层次模型，网状模型
   关系模型：使用二维表来存储数据、数据联系
   非关系模型
6）关系模型重要的概念
  - 关系：规范的二维表（列名称不能重复、
    属性不能再分、数据的次序并不重要）
  - 实体：现实可以区分的事物
  - 元组：表中的一行数据
  - 属性：实体的数据特征
  - 键：可以区分实体的属性、属性组合
  - 主键：从所有的键中，选取一个作为主键
    在关系中作为逻辑上唯一区分实体的依据
	要求非空、唯一

2. MySQL操作
1）安装
2）服务管理
  - 启动：/etc/init.d/mysql start
    停止：stop参数
	查看状态：status参数
  - 查看端口：netstat -an | grep 3306
3）库管理
  - 查看库：show databases;
  - 进入库：use 库名;
  - 创建库：create DATABASE 库名 [字符集];
  - 查看库中的表：show tables;
4）表管理
  - 创建表
    CREATE TABLE 表名(
		字段1 类型(长度),
		字段2 类型(长度),
        ......
	);
  - 查看表结构：desc 表名;
  - 查看建表语句：show CREATE TABLE 表名

5）数据管理
  - 插入
    INSERT INTO orders
	values('20180101','C0001',now(),1,1,100)

    INSERT INTO orders(order_id, cust_id)
	values('20180101','C0001')

    INSERT INTO orders(order_id, cust_id)
	VALUES('20180101','C0001'),
	      ('20180102','C0002');

  - 查询
    SELECT * FROM orders;
	SELECT order_id, cust_id FROM orders;
	SELECT * FROM orders WHERE cust_id='C0001';
	
	SELECT * FROM orders
	WHERE cust_id = 'C0001'
	AND status = 1;

今天的内容

数据类型
1. 数值类型
  - 整数型：TINYINT, INT, BITINT
  - 浮点数: DECIMAL(16, 2)

  使用注意：整数要注意存储范围
            浮点数要注意精度

  练习：
  第一步：创建表，包含两个字段（整型、浮点型） 
  CREATE TABLE num_test(
    -- type是整数型，存储实际空间是4Bytes
    -- 大小是由数据类型决定的
    -- INT(3)表示默认显示3位
    -- unsigned表示无符号（0和整数）
    -- zerofill表示左边用0填充
	type INT(3) unsigned zerofill,
	rate DECIMAL(10,2)
  );

  第二步：插入数据 
  -- 正常值
  INSERT INTO num_test VALUES(1, 0.88);
  -- 小数部分超过定义长度
  INSERT INTO num_test VALUES(2, 123.456);
  -- 浮点数字段插入整数
  INSERT INTO num_test VALUES(3, 2);
  -- 整数超过最大显示宽度
  INSERT INTO num_test VALUES(1000,3.444);
  
2. 字符类型
1）定长字符(CHAR)
  - 最大存储255个字符
  - 定义长度后，如果数据不足，自动补充空格
  - 超过长度无法存入
  - 如果不设置长度，默认长度为1
2）变长字符(varchar)
  - 最大存储65535个字节
  - 实际存储空间根据实际数据进行分配
  - 长度超过定义长度时无法存入
3）大文本类型(TEXT)
  - 能存储超过65535字符的数据
  - 最大可以存储4G的数据

3. 枚举
1）ENUM：从给定的几个值中选取1个
2）SET: 从给定的值中选取1个或多个
3）示例：
  CREATE TABLE enum_test(
    name VARCHAR(32),
	sex  enum('boy','girl'),
	course SET('music','dance','paint')
  );
  INSERT INTO enum_test 
  VALUES('Jerry','girl','music,dance');
  -- 超过范围，报错
  INSERT INTO enum_test 
  VALUES('Tom','boy','music,football');

4. 日期时间类型
1）日期：DATE，范围'1000-01-01'~'9999-12-31'
2）时间：TIME
3）日期时间类型
4）时间戳类型：TIMESTAMP
5）示例
  SELECT now(), sysdate(); -- 取当前时间
  SELECT curdate(), curtime(); -- 取当前日期、时间
  -- 分别取出当前时间中的年、月、日
  SELECT YEAR(now()),MONTH(now()),DAY(now());
  -- 取出当前系统时间中日期、时间部分
  SELECT DATE(now()), TIME(now());

修改记录
1. 语法
   UPDATE 表名
   SET 字段1 = 值1,
       字段2 = 值2,
	   ...
   WHERE 条件表达式;
2. 示例
  - 修改某个订单的状态
  UPDATE orders SET status = 2
  WHERE order_id = '201801010001';

  - 修改订单的商品数量和订单金额
  UPDATE orders 
     SET products_num = 2,
	     amt = 400
   WHERE order_id = '201801010002';

删除记录
1. 语法
  DELETE FROM 表名 WHERE 条件表达式;
2. 示例
  -- 删除201801010002订单的信息
  DELETE FROM orders 
  WHERE order_id = '201801010002';
3. 特别注意
  1）进行严格条件限定，如果不带条件删除所有
  2）真实项目中，删除、修改数据之前一定要备份

更多查询
1. 带比较操作符的查询：>,<,>=,<=,<>(或!=)
  示例1：查询所有订单金额大于200元的订单
  SELECT * FROM orders WHERE amt > 200;

  示例2：查询所有状态不为2的订单
  SELECT * FROM orders WHERE status <> 2;

2. 逻辑运算符：AND，OR
  - and: 多个条件同时满足
  - or: 满足其中一个

  示例：查询客户编号为C0002或C0003，并且
        订单状态为1的订单
  SELECT * FROM orders
  WHERE (cust_id='C0002' OR cust_id='C0003')
  AND status = 1;

3. 范围比较
1）between...AND...: 在...和...之间(包含两边)
2）in/NOT in: 在/不在某个指定的范围
3）示例
  示例1：查找所有金额在200~300之间的订单
  SELECT * FROM orders 
  WHERE amt BETWEEN 200 AND 300;

  示例2：查询客户编号在('C0003','C0004')
         范围内的订单
  SELECT * FROM orders
  WHERE cust_id IN ('C0003','C0004');
  -- where status in(1,2,3)
  -- NOT IN 表示cust_id不在指定范围内

4. 模糊查询
1）格式：where 字段 LIKE "通配字符"
2）通配符匹配
   下划线(_): 匹配单个字符
   百分号(%): 匹配任意个字符
3）示例
  第一步：建客户信息表
  CREATE TABLE customer(
    cust_id VARCHAR(32),
	cust_name VARCHAR(32),
	tel_no VARCHAR(32)
  ) DEFAULT charset=utf8;
  第二步：插入测试数据
  INSERT INTO customer VALUES
  ('C0001','Jerry','13512345678'),
  ('C0002','Dekie','13522334455'),
  ('C0003','Dokas','15844445555');
  第三步：模糊查询
  -- 查询所有名字以D开头的客户
    SELECT * FROM customer 
	WHERE cust_name LIKE 'D%';
  -- 查询所有电话号码中包含44和55
    SELECT * FROM customer
	WHERE tel_no LIKE '%44%55%';
4）注意事项：
   模糊查询不精确匹配，速度较慢
   尽量避免%前置

5. 空值、非空判断
1）语法
   判断空值：字段 IS NULL
   判断非空：字段 IS NOT NULL
2）示例：查询电话号码为空值的客户信息
  SELECT * FROM customer
  WHERE tel_no IS null;
  -- where tel_no is not null; -- 电话非空

查询子句
1. ORDER BY: 排序
1）格式：order BY 字段 [ASC/DESC]
   ASC-升序    DESC-降序
2）示例：查询所有订单，按照金额降序排列
  SELECT order_id, amt 
  FROM orders
  ORDER BY amt desc;  -- asc或不写，升序

2. limit子句
1）作用：限制显示的笔数
2）格式
   limit n     只显示前面n笔
   limit m,n   从第m开始，总共显示n笔
3）示例
   -- 查询所有订单，显示前2笔
   SELECT * FROM orders limit 2;
   -- 查询所有订单，显示金额最大的2笔
   SELECT * FROM orders 
   ORDER BY amt DESC limit 2;
   
   -- 利用limit分页：每页3笔数据
   -- 第1页
   SELECT * FROM customer limit 0,3;
   -- 第2页
   SELECT * FROM customer limit 3,3;
   -- 第3页
   SELECT * FROM customer limit 6,3;

3. distinct子句
1）作用：去除重复数据
2）语法格式
    SELECT DISTINCT(要去重的字段)
	FROM 表名
3）示例：查询客户表中一共有几个不重复的名字
    SELECT DISTINCT(cust_name)
	FROM customer;

4. 聚合函数
1）什么是聚合：不是直接查询表中的数据，
   而是对数据进行总结，返回结果
2）聚合函数有：
   max     求最大值
   MIN     求最小值
   AVG     求平均值
   SUM     求和
   COUNT   统计笔数
3）示例
   SELECT MAX(amt) "最大金额",
          MIN(amt) "最小金额",
		  AVG(amt) "平均金额",
		  SUM(amt) "订单总金额"
   FROM orders;

   -- 统计订单笔数
   SELECT COUNT(*) FROM orders;

   -- 统计电话号码以135开头的客户数量
   -- 查customer表
   SELECT COUNT(*) FROM customer
   WHERE tel_no LIKE '135%';

   说明：对某个字段调用聚合函数时，如果
         字段的值为空，不会参与聚合操作

4. 分组：group BY
1）作用：对查询结果进行分组，通常和聚合函数
   搭配使用
2）语法格式：group BY 字段
3）示例
   -- 统计客户数量，按照客户名称分组
   SELECT cust_name, COUNT(*)
   FROM customer GROUP BY cust_name;

   -- 从orders表，统计每种状态订单的总金额
   SELECT status, SUM(amt) 
   FROM orders GROUP BY status; 

5. Having：对分组结果进行过滤
1）作用：对分组结果进行过滤，需要和group BY
   语句配合使用
2）语法格式
   GROUP BY 分组字段 HAVING 过滤条件
3）示例
   -- 按照订单状态统计总金额
   -- 查询结果中只保留总金额大于500的
   SELECT status, SUM(amt) 
   FROM orders 
   GROUP BY status
   HAVING SUM(amt) > 500;

   说明：group by分组聚合的结果，只能用
         having，不能用where，where只能
		 用户表中有的字段作为条件时候

表结构调整
1. 添加字段
1）语法
  - 添加到表的最后一个字段
   ALTER table 表名 ADD 字段名 类型(长度) 
  - 添加到表的第一个字段
   ALTER table 表名 ADD 字段名 类型(长度) first
  - 指定添加到某个字段后面
   ALTER table 表名 ADD 字段名 类型(长度) 
   after 字段名称
2）示例
  CREATE TABLE student(
    stu_no VARCHAR(32),
	stu_name VARCHAR(128)
  );
  添加字段
  -- 在最后添加年龄字段
  ALTER TABLE student ADD age int;
  -- 将id字段添加到第一个字段
  ALTER TABLE student ADD id INT first;
  -- 将tel_no添加到stu_name后面
  ALTER TABLE student ADD tel_no VARCHAR(32)
  after stu_name;
  
2. 修改字段
1）修改字段类型
  ALTER TABLE 表名 modify 字段 类型(长度)
2）修改字段名称
  ALTER TABLE 表名 
  change 旧字段名 新字段名 类型(长度)
3）示例
  -- 修改student表stu_name字段长度为64
  ALTER TABLE student 
  modify stu_name VARCHAR(64);

  -- 将student表age字段改为stu_age
  ALTER TABLE student
  change age stu_age int;

3. 删除字段
1）语法：ALTER TABLE 表名 DROP 字段名
2）示例：删除student表id字段
  ALTER TABLE student DROP id;





