from django.db import models

# Create your models here.
#创建一个实体类 - Publisher(表示出版社的信息)
#Django中允许省略自增主键的声明,Django会自动声明
#1.name:出版社名称(字符串)
#2.address:出版社所在地址(字符串)
#3.city:出版社所在城市(字符串)
#4.country:出版社所在国家(字符串)
#5.website:网址(字符串)
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    website = models.URLField()

class Author(models.Model):
    name = models.CharField(max_length=30,db_index=True)
    age = models.IntegerField()
    email = models.EmailField(null=True)
    #增加一个列isActive,表示是否被激活
    isActive = models.BooleanField(default=True)

class Book(models.Model):
    title = models.CharField(max_length=50)
    publicate_date = models.DateField()







