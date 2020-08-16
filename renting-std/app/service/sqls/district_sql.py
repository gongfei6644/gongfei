# -*- coding: utf-8 -*-


city_sql = """
select * from (
  select id, city_name, alias from sys_city where sys_status=1
  UNION ALL
  SELECT sys_id as id,sys_name as city_name,net_name as alias 
  FROM sys_comparision where status=1 and type=1
)t where 1=1
"""

city_sql2 = """
select id, city_name, alias from sys_city where sys_status=1
"""

alias_sql = """
case
  when LOCATE('市城区',area_name) > 0 and CHAR_LENGTH(area_name)>4 and POSITION('市城区' IN area_name) = (CHAR_LENGTH(area_name) -2) then REPLACE(area_name,'市城区','')
  when LOCATE('市',area_name) > 0 and CHAR_LENGTH(area_name)>2 and POSITION('市' IN area_name) = CHAR_LENGTH(area_name) then REPLACE(area_name,'市','')
  when LOCATE('镇',area_name) > 0 and CHAR_LENGTH(area_name)>2 and POSITION('镇' IN area_name) = CHAR_LENGTH(area_name) then REPLACE(area_name,'镇','')
  when LOCATE('开发区',area_name) > 0 and CHAR_LENGTH(area_name)>4 and POSITION('开发区' IN area_name) = (CHAR_LENGTH(area_name) -2) then REPLACE(area_name,'开发区','')
  when LOCATE('高新区',area_name) > 0 and CHAR_LENGTH(area_name)>4 and POSITION('高新区' IN area_name) = (CHAR_LENGTH(area_name) -2) then REPLACE(area_name,'高新区','')
  when LOCATE('新区',area_name) > 0 and CHAR_LENGTH(area_name)>3 and POSITION('新区' IN area_name) = (CHAR_LENGTH(area_name) -1) then REPLACE(area_name,'新区','')
  when LOCATE('经济区',area_name) > 0 and CHAR_LENGTH(area_name)>4 and POSITION('经济区' IN area_name) = (CHAR_LENGTH(area_name) -2) then REPLACE(area_name,'经济区','')
  when LOCATE('经开区',area_name) > 0 and CHAR_LENGTH(area_name)>4 and POSITION('经开区' IN area_name) = (CHAR_LENGTH(area_name) -2) then REPLACE(area_name,'经开区','')
  when LOCATE('区',area_name) > 0 and CHAR_LENGTH(area_name)>2 and POSITION('区' IN area_name) = CHAR_LENGTH(area_name) then REPLACE(area_name,'区','')
  when LOCATE('自治县',area_name) > 0 and CHAR_LENGTH(area_name)>4 and POSITION('自治县' IN area_name) = (CHAR_LENGTH(area_name) -2) then REPLACE(area_name,'自治县','')
  when LOCATE('县',area_name) > 0 and CHAR_LENGTH(area_name)>2 and POSITION('县' IN area_name) = CHAR_LENGTH(area_name) then REPLACE(area_name,'县','')
  else area_name
end alias
"""

area_sql = """
select * from (
  SELECT a.id,area_name,
  {},
	c.id as city_id
  FROM sys_area a RIGHT JOIN sys_city c ON a.city_id=c.id 
	where a.sys_status=1
  UNION ALL
  SELECT sys_id as id,sys_name as area_name,net_name as alias,c.id as city_id 
  FROM sys_comparision cp RIGHT JOIN sys_area a on cp.sys_id=a.id 
	RIGHT JOIN sys_city c on a.city_id=c.id where cp.status=1 and cp.type=2
	UNION ALL
	SELECT id,sys_name as area_name,
  {},
	city_id
	FROM (
    SELECT sys_id as id,sys_name,net_name as area_name,c.id as city_id 
    FROM sys_comparision cp RIGHT JOIN sys_area a on cp.sys_id=a.id 
    RIGHT JOIN sys_city c on a.city_id=c.id where cp.status=1 and cp.type=2
	)ts
)t where 1=1
""".format(alias_sql, alias_sql)

area_sql2 = """
SELECT a.id,area_name,
{},
c.id as city_id
FROM sys_area a RIGHT JOIN sys_city c ON a.city_id=c.id 
where a.sys_status=1
""".format(alias_sql)
