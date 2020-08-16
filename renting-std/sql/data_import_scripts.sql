-- 从sqlserver中数据中心导入相关sys_code数据
SELECT
	  ID as type,
	  codetype as type_name,
	  Code as subtype,
	  [CodeName] as subtype_name,*
	  FROM [fxtdatacenter].[dbo].[SYS_Code]
	  where CodeType in('户型结构','建筑类型','居住用途','朝向','装修档次','户型')
	  and id not in(1146,1145)

-- 从采集库中导入与系统不可匹配的code映射关系数据
-- 用途根据需求除了别墅类的，其它均清空重算，故其它用途类型的数据除了别墅其它可不维护
SELECT
  c.ID as type,
  m.[CodeName] as net_name,
  c.Code as sys_id,
  c.codename as sys_name,
  'SYS' as creator,
  GETDATE() as crt_time,
  1 as status
  FROM [DataCollecting].[dbo].[SYS_Code_Mapping] m
  inner join [DataCollecting].[dbo].sys_code c on m.Code=c.code
  where c.CodeType in('户型结构','建筑类型','居住用途','装修档次')
  and m.CodeName != c.CodeName


-- 原采集数据中的sub类型名称建的有误，修改语句如下
UPDATE sys_comparision t
set t.sys_name=(select c.subtype_name from sys_code c where c.subtype=t.sys_id)
where type !=1