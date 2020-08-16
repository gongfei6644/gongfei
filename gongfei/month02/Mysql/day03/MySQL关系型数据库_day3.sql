课程：MySQL关系型数据库
进度：day3

今天的内容

高级查询
1. 子查询
1）定义：一个查询语句中嵌套另一个查询
2）例如：
   -- 查询金额超过平均值的订单
   SELECT * FROM orders WHERE amt > 
   (SELECT AVG(amt) FROM orders);

   -- 查询所有名字以D开头的客户下的订单
   SELECT * FROM orders WHERE cust_id IN
   (SELECT DISTINCT cust_id 
     FROM customer
    WHERE cust_name LIKE 'D%');
3）说明：
  - 括号中的部分称为子查询
  - 子查询可以返回一个值，也可以多个值
    根据外层查询的要求来决定
  - 先执行子查询，将子查询的结果，作为外层
    查询的条件，再执行外层查询
  - 子查询只执行一遍
4）使用子查询的情况：一个语句无法查出来，
   或者不方便查询出结果，使用子查询

5）示例：查询所有没有下过订单的客户信息
   提示：订单表中先找出所有客户编号
         再从客户表中去掉这一部分客户
   SELECT * FROM customer 
   WHERE cust_id NOT IN (
     SELECT DISTINCT cust_id FROM orders
   );

2. 联合查询
1）什么是联合查询：也叫连接查询，将多个表中的
   数据进行连接，得到一个查询结果集
2）什么情况下使用联合查询：当从一个表无法查询
   到所有想要的数据时，使用联合查询
   前提：联合的表之间一定要有逻辑上的关联性
   SELECT a.order_id, a.amt,
          b.cust_name, b.tel_no
   FROM orders a, customer b
   WHERE a.cust_id = b.cust_id;

3）笛卡尔积（联合查询的理论依据）
  - 什么是笛卡尔积：两个集合的乘积，产生一个
    新的集合。表示两个集合所有的可能的组合情况
  - 笛卡尔积和关系：笛卡尔积中，去掉没有意义
    或不存在的组合，就是关系（规范的二维表）

4）连接查询
  - 内连接(INNER Join)：没有关联到的数据不显示    
   示例：查询订单编号、金额、客户名称、客户电话
   -- 方式一：where进行条件关联
   SELECT a.order_id, a.amt,
          b.cust_name, b.tel_no
   FROM orders a, customer b
   WHERE a.cust_id = b.cust_id;

   -- 方式二：利用Inner join关键字
   SELECT a.order_id, a.amt,
          b.cust_name, b.tel_no
   FROM orders a INNER JOIN customer b
   ON a.cust_id = b.cust_id;

  - 外连接(OUTER Join)：没有关联到的数据也要
    显示到结果集
  左连接：以左边为基准，右表的数据进行关联
          左表数据全部显示，右表中的字段
		  如果没有关联到，则显示NULL
          LEFT JOIN 实现
   SELECT a.order_id, a.amt,
          b.cust_name, b.tel_no
   FROM orders a LEFT JOIN customer b
   ON a.cust_id = b.cust_id;

  右连接：以右边为基准，左表的数据进行关联
          右表数据全部显示，左表中的字段
		  如果没有关联到，则显示NULL
		  right JOIN 实现
   SELECT a.order_id, a.amt,
          b.cust_name, b.tel_no
   FROM orders a right JOIN customer b
   ON a.cust_id = b.cust_id;

课堂练习：
1. 创建一个订单明细表(orders_detail), 包含
的字段有：
   订单编号   order_id   字符串 32字符
   商品编号   product_id 字符串 32字符
   商品金额   amt        浮点数 2小数

2. 在商品明细表中插入3笔数据(注意逻辑关联性)

3. 做三个表的联合查询，查询结果为：
订单编号 下单日期 客户名称 商品编号 商品金额

SQL语句：
  CREATE TABLE orders_detail (
    order_id VARCHAR(32),
	product_id VARCHAR(32),
	amt DECIMAL(16,2) );
  
  INSERT INTO orders_detail VALUES
  ('201801010001', 'P0001', 80),
  ('201801010001', 'P0002', 20),
  ('201801010003', 'P0003', 200);

  SELECT a.order_id, a.order_date,
         b.cust_name, 
		 c.product_id, c.amt
  FROM orders a, customer b, orders_detail c
  WHERE a.cust_id = b.cust_id
  AND a.order_id = c.order_id;


约束(Constraint)
1.什么是约束：数据必须遵循的规则
2.目的：保证数据一致性、完整性
  从数据库层面对数据进行“安检”
3.分类
1）非空约束
  - 定义：Not null，要求字段的值不能为空
  - 语法：
    字段名称  类型(长度)  NOT null

2）唯一约束
  - 定义：unique，字段的值不能重复
  - 语法：
    字段名称  类型(长度) unique

3）主键(PRIMARY KEY, 简写PK)：非空、唯一
  - 定义：主键在表中唯一标识、区分一个实体
          非空、唯一
  - 语法：
    字段名称  类型(长度) PRIMARY KEY
  
  示例：
  CREATE TABLE t1(
    stu_no VARCHAR(32) PRIMARY key, -- 主键
	stu_name VARCHAR(32) NOT null,  -- 非空
	id_card_no VARCHAR(32) UNIQUE   -- 唯一
  );
  -- 正常数据
  INSERT INTO t1 
  VALUES('001','Jerry','513822199001011111');
  -- 插入stu_name为空数据，报错
  INSERT INTO t1 
  VALUES('002', NULL,'51382219900102222');
  -- 插入id_card_no重复的数据，报错
  INSERT INTO t1 
  VALUES('003','Tom','513822199001011111');
  -- 主键stu_no插入空值，报错
  INSERT INTO t1(stu_no, stu_name)
  VALUES(NULL, 'Dekie');
  -- 主键stu_no值重复，报错
  INSERT INTO t1(stu_no, stu_name)
  VALUES('001','Dokas');

4）默认值(DEFAULT constraint)
  - 定义：指定某个字段的默认值，如果新插入
    一笔数据没有对该字段赋值，系统会自动
	填入一个默认值
  - 语法：
    字段名称 类型(长度) DEFAULT 值

5）自动增长(auto_increment)
  - 定义：当字段被设置为自增长时，插入时
    不需要赋值，系统在原最大值的基础上
	自动加1（要求：要求这个字段必须是PK，
	或设置了unique约束）
  - 语法：
    字段名称 类型(长度) auto_increment

  示例：
  CREATE TABLE t2(
    id INT PRIMARY KEY auto_increment,
    name VARCHAR(32),
	status INT DEFAULT 0
  );
  INSERT INTO t2 VALUES(NULL,'Jerry',1);
  INSERT INTO t2 VALUES(NULL,'Tom',2);
  INSERT INTO t2(id, name) 
  VALUES(NULL,'Hennry');  

6）外键约束（Foreign Key, 简称FK）
  - 什么是外键：一种约束，建立外键的前提是：
    某个字段在当前表中不是PK，但在另外表
	（也称为“外表”）是主键
  - 作用：保证被参照的实体一定存在
    （参照的完整性）
  - 字段被设置外键约束后，影响有：
    当插入一个在外表中不存在的实体是，报错
	当删除外表中已经被参照的实体，报错
  - 创建外键语法：
    字段名称 类型(长度) ,
    -- 所有字段定义完成后
	CONSTRAINT 外键名称 FOREIGN KEY(当前表字段)
	REFERENCES 外表(字段名)
  - 示例：
    创建course(课程信息表, 主键course_id)
	创建teacher(教师信息表，包含course_id，
	    在course_id字段创建外键)
CREATE TABLE course(
  course_id VARCHAR(32) PRIMARY key,
  name VARCHAR(32)
) DEFAULT charset=utf8;

CREATE TABLE teacher(
  id INT auto_increment PRIMARY key,
  name VARCHAR(32),
  course_id VARCHAR(32),
  CONSTRAINT fk_course FOREIGN KEY(course_id)
  REFERENCES course(course_id)
) DEFAULT charset=utf8;
          
  -- 在course表中插入一笔课程数据
  -- （一个课程实体）
  INSERT INTO course 
  VALUES('0001','Python编程基础');
  -- 再在teacher表中插入一笔数据
  -- 参照0001课程实体. 
  INSERT INTO teacher 
  VALUES(1,'Jerry', '0001');  -- OK
  -- 删除0001课程，报错
  DELETE FROM course WHERE course_id='0001';
  -- 在teacher表插入course_id为0003的信息
  -- 报错，参照0003课程实体不存在
  INSERT INTO teacher 
  VALUES(2,'Jerry', '0003');  -- 报错

  - 外键使用的条件
    表的存储引擎必须为InnoDB
    外键字段在另外表中必须是主键
	当前表、外表中字段类型必须一致

课堂练习：通过修改表的方式添加约束
7）通过修改字段方式添加约束
首先，创建测试表t6
create table t6(  
	id int, name varchar(32),
	status int, course_id varchar(4),
	tel_no varchar(32)  );
通过修改表定义语句添加约束
alter table t6 add primary key(id);      -- 添加主键
alter table t6 modify id int auto_increment;       -- 添加自增长
alter table t6 modify status int default 0;           -- 添加默认值
alter table t6 modify tel_no varchar(32) 
                    unique;   -- 添加唯一约束
alter table t6 add CONSTRAINT fk_course_id    -- 添加外键约束
FOREIGN KEY(course_id) 
REFERENCES course(course_id);

数据导入导出
1. 导出
1）show variables LIKE 'secure_file%';
   结果：/var/lib/mysql-files/
   导出只能导出到该目录
   导入只能从该目录导入
2）语法
   select查询语句
   INTO outfile '文件路径'
   fields terminated BY '字段分隔符'
   lines terminated BY '行分隔符';
3）示例：导出orders表中所有的数据
   SELECT * FROM orders
   INTO outfile '/var/lib/mysql-files/orders.csv'
   fields terminated BY ','
   lines terminated BY '\n';
   -- 查看导出的文件(Linux Shell下执行)： 
   sudo cat /var/lib/mysql-files/orders.csv

2. 导入
1）语法
  LOAD data infile '备份文件路径'
  INTO TABLE 表名称
  fields terminated BY ','
  lines terminated BY '\n';
2）示例
-- 先删除orders表中数据，再执行导入
LOAD data infile '/var/lib/mysql-files/orders.csv'
INTO TABLE orders
fields terminated BY ','
lines terminated BY '\n';
-- 导入完成后，查询、确认

表的复制、重命名
1. 表的复制
  -- 将orders数据、表结构全部复制到orders_new表
  CREATE TABLE orders_new
  SELECT * FROM orders;
  -- 将orders表结构复制到orders_new表
  CREATE TABLE orders_new
  SELECT * FROM orders WHERE 1=0; --查询结果为空
  
  备注：该方式不会将键的属性复制到新表中

2. 表的重命名
  -- 将orders表重命名为orders_bak
  ALTER TABLE orders rename TO orders_bak;

  









