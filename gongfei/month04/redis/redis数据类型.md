### redis数据类型

**数据结构**

>redis是key-value的数据结构，每条数据都是一个键值对
>
>键的类型是字符串
>
>⚠️注意：键是不能重复的
>
>**值的类型分为5种：**
>
>字符串string
>
>哈希hash
>
>列表list
>
>集合set
>
>有序集合zset

##string类型

​	字符串类型是Redis中最为基础的数据存储类型，它在redis中是二进制，它便意味着可以接受任何格式的数据，如JPEG图像数据或Json对象的描述信息，在Redis中字符串类型的Value最多可以容纳的数据长度是512M。

## 保存

**如果设置的键不存在，则为添加，如果设置的键已经存在，则为修改。**

#### 设置键值

```
set key value
eg: set name itchat
```

#### 设置键值以及过期时间，以秒为单位。

```
setex key seconds value
eg:setex aa 3 bb  # 设置键为aa值为bb过期时间为3秒的数据
```

#### 设置多个键值

```
mset key1 value1 key2 value2 
eg:mset aa python bb java cc javascript
```

#### 追加值

```
append key value 
# 我们在上面已经给aa设置的值为python，此时我们可以使用append来给aa去追加值
append aa hahah
get aa
pythonhahah
```

## 获取

#### 根据键获取值，如果不存在此键则返回nil

```
get key
eg:et aa
>pythonhahah
get bb
>java
# 此时也可以根据多个键获取多个值
mget key1 key2 key3
eg: mget aa bb cc
```

## 键命令（类似于mysql中的select）

#### 查找键，参数支持正则表达式

```
keys pattern
# 查找所有键
keys *
# 查找名字中包含a的键
keys a*
```

#### 判断键是否存在，如果存在则返回1，不存在则返回0

```
exists key1 
# 判断键a1是否存在
exists a1 
```

#### 查看键对应的value的值

```
type key
# 查看键a1的值的类型，为redis支持的五种类型中的一种
eg：type a1
```

#### 删除键以及对应的值

```
del key1 key2
# 删除键a1 a2
eg: del a1 a2
```

#### 在我们添加键值对的时候没有指定过期时间，此键值对会一直存在，知道用户使用del命令之后才会被移除，但是我们有办法第二次去添加过期时间

```
exprie key seconds
# 设置键 a1 的过期时间为3秒
eg：expire a1 3
```

#### 查看有效时间，以秒为单位

```
ttl key
# 先试给bb设置有效时间为10秒，然后可以使用ttl bb去查看其过期时间
expire bb 10
ttl bb
```

## hash类型

hash用于存储对象，对象的结构为属性和值。

值的类型为字符串string

#### 增加、修改

```
设置单个属性
$ hset key filed value
eg:hset user name tarena

[error] 如果出现MISCONF等提示信息，说明此事不能持久化到硬盘中，运行一下命令即可解决；
config set stop-writes-on-bgsave-error no

设置多个属性
$hmset key1 field1 value1 field2 value2
eg:设置用户的属性年龄为22名字是tarena
$	hmset u2 name tarena age 22

```

#### 查询

```
获取指定键的所有属性

$ hkeys key
eg:hkeys u2
 1) name
 2) age
 
获取某一个属性的值
$hget key field
eg:hget u2 name
   tarena
   
获取多个属性的值
$ hmget key field1 field2
eg: hmget u2 name age
  1) name
  2) age
 
获取所有属性的值
$hvals key
$ hvals u2
	1) name
 	2) age
```

#### 删除

```
删除整个hash键以及值，使用del命令
删除属性，属性对应的值也会一起被删除
		$ hdel key field1 field2 
删出u2的属性age
		$ hdel u2 age
```

## list类型

列表的元素类型为string

按照插入顺序排序

####增加

```
在左侧插入数据
lpush key value1 value2 .....
eg:从键为a1的列表左侧加入数据 a,b,c
lpush a1 a b c  

在右侧插入数据
rpush key value1 value2 
eg:从键a1的列表右侧加入数据0 1 
$ rpush a1 0 1 

在指定元素的前后插入新元素
linsert key	before/after 现有元素 新元素
eg：insert a1 before b 3 
```

#### 获取

返回列表指定范围内的元素

​	start stop 为元素的下标索引

​	索引从左侧开始，第一个元素为0

​	索引可以是负数，表示从尾部开始计数，如-1表示最后一个元素

```
查看列表中有多少个元素
lrange key start stop
$ lrange a1 0 3

eg：获取键为a1的列表的所有元素
lrange a1 0 -1
```

#### 设置指定索引位置的元素值

索引从左侧开始，第一个元素为0

```
lset key index value
eg:修改键为a1的列表下标为1的元素的值为 z
lset a 1 z
```

#### 删除

 删除指定元素

​	将列表中前count次出现的值为value的元素移除

​	count > 0 从头往尾移除

​	count < 0 从尾往头部移除

​	count = 0 移除所有

```
lrem key count value
向列表a2中加入元素a b a b a b
lpush a2 a b a b a b

从a2 列表右侧开始删除2个b
lrem a2 -2 b
```

## set类型

​	无序集合

​	元素为string类型

​	元素具有唯一性，不重复

​	说明：对于集合没有修改操作

#### 增加

```
添加元素
	sadd key member1 member2 .....
eg: 向a3的集合中添加元素 zhangsan lisi wangwu 
	 sadd a3 zhangsan lisi wangwu
```

#### 获取

```
返回所有的元素
smembers keys
eg：获取a3集合中的所有元素
 smembers a3

```

#### 删除

```
删除指定元素
srem key
eg：删除指定键a3集合中的wangwu
srem a3 wangwu
```

## zset数据类型

​	sorted set 有序集合

​	元素为string类型

​	元素具有唯一性，不重复

​	每个元素都会关联一个double类型的score，表述权重，通过权重将元素进行排序。

​	没有修改操作

####增加

```
zadd key score1 member1 score2 member2 ...
eg: 向键a4的集合中添加元素lisi wangwu zhangsan zhaoliu 他们的权重分别是 5 4 3 6
  zadd a4 5 wangwu 5 lisi 4 wangwu  3 zhangsan 6 zhaoliu 
```

#### 获取

   返回指定范围内的元素

​	start stop 为元素的下标索引

​    索引从左侧开始第一个元素为0

​	索引可以为负数，表示从尾部开始计数，如-1表示最后一个元素

```
zrange key start stop
eg：获取a4集合中的所有元素
	zrange a4 0 -1
	
返回score值在min和max之间的成员（包括max和min）
zrangebyscore key min max
eg：获取键为a4 的集合中权限值在5和6之间的成员
zrangebyscore a4 5 6 
	1）wangwu
	2）zhaoliu
	
返会成员member的score值
	zscore key member 
eg：获取键a4的集合中元素zhangsan的权重
	zscore a4 zhangsan
```

#### 删除



```
	删除指定元素
zrem key member1 member2
eg:删除集合a4中的元素zhangsan
zrem a4 zhangsan

删除权重在指定范围内的元素
 zremrangebyscore key min max 
eg：删除集合a4 中权重在5、6之间的元素
zremrangebyscore a4 5 6 
```

