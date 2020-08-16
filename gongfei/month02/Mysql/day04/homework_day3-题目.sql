-- homework_day3.sql
-- MySQL第三天作业

/*
1. 修改acct表结构
  1）在acct_no上添加主键约束
  2）在acct_name, acct_type字段上添加非空约束
  3）在status字段添加默认约束，默认值为1
*/
alter table acct add primary key(acct_no);
alter table acct modify acct_name 
  varchar(128) not null;
alter table acct modify acct_type
  int not null;
alter table acct modify status int default 1;

/*
2. 创建客户信息表customer，包含字段有：
   cust_no		客户编号，字符串类型，最长32位，主键
   tel_no     	电话号码，字符串类型，最长32位，非空
   cust_name	客户姓名，字符串类型，最长64位，非空
   address		送货地址，字符串类型，最长128位，非空
*/
create table customer (
  cust_no varchar(32) primary key,
  tel_no  varchar(32) not null,
  cust_name varchar(64) not null,
  address varchar(128) not null
) default charset=utf8;

/*
3. 为customer添加数据，
   每个acct表中的cust_no都添加一笔 */
insert into customer values
('C0001','13512345678', 'Jerry', '北京东城区');

/*4. 查询所有贷款账户所属客户名称、电话号码
  （利用子查询实现）*/
  select cust_name, tel_no from customer 
  where cust_no in (
    select distinct cust_no from acct 
    where acct_type = 2
  );

/*5. 编写一个查询语句，查询结果包含如下字段：
  （联合查询来实现）
账号 户名 账户类型 余额 客户编号 客户电话 地址 */
select a.acct_no, a.acct_name, a.acct_type,a.balance,
       b.cust_no, b.tel_no, b.address
from acct a, customer b
where a.cust_no = b.cust_no;

