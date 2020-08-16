-- homework_day2.sql
-- MySQL第二天作业

/*1. 创建数据库bank, 并指定为utf8编码格式*/
CREATE DATABASE bank DEFAULT charset=utf8;

/*
2. 创建账户表(acct, utf8编码格式), 包含如下字段
	acct_no   	账号，字符串类型，长度32字符
	acct_name 	户名，字符串类型，长度128字符
	cust_no   	客户编号，字符串类型，长度32字符
	acct_type	账户类型, 整数型(1-存款账户 2-贷款账户)
	reg_date	开户日期, 日期类型
	status		账户状态(1-正常 2-注销 3-挂失 4-冻结)
	balance   	数字类型，最长16位，2位小数 */

  create table acct (
     acct_no varchar(32),
	 acct_name varchar(128),
	 cust_no varchar(32),
	 acct_type int,
	 reg_date date,
	 status int,
	 balance decimal(16,2)
  ) default charset=utf8;

/*3. 至少插入五笔数据(要求数据尽量看上去真实) */
insert into acct values
('622345000001','Jerry','C0001',1,
  date(now()), 1, 5000);

insert into acct values 
('622345000002','Tom','C0002',1,date(now()),1,500),
('622345000003','Lily','C0003',1,date(now()),1,700),
('622345000004','Emma','C0004',1,date(now()),1,900),
('622345000005','Dokas','C0005',1,date(now()),1,600);

/*4. 编写如下SQL语句 */
-- 1)查找某个客户账户信息(以客户编号做条件)
select * from acct where cust_no = 'C0002';
-- 2)查找余额大于等于5000的账户信息
select * from acct where balance > 5000;
-- 3)查找余额大于等于5000的贷款账户信息
select * from acct 
where balance > 5000 and acct_type = 2;
-- 4)查找账户名称以'D'开头的所有账户信息
select * from acct where acct_name like 'D%';
-- 5)查找所有账户信息，并按照金额倒序排列
select * from acct order by balance desc;
-- 6)统计每种状态的账户笔数
select status "账户状态", count(*) 
from acct group by status;
-- 7)查询账户余额的最大值、最小值、平均值、总金额
select max(balance), min(balance), avg(balance),
       sum(balance)
from acct;
-- 8)查询账户余额最大的前3笔账户
select * from acct order by balance desc limit 3;

