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
    name = models.CharField(
        max_length=30,
        db_index=True,
        verbose_name='姓名')
    age = models.IntegerField(
        verbose_name='年龄')
    email = models.EmailField(
        null=True,
        verbose_name='邮箱')
    #增加一个列isActive,表示是否被激活
    isActive = models.BooleanField(
        default=True,
        verbose_name='激活')
    #重写__str__函数以便修改在后台的展示名称
    def __str__(self):
        return self.name

    #声明内部类-Meta,定义其展现形式
    class Meta:
        #1.定义表名
        db_table = 'author'
        #2.定义实体类在admin中的显示名称(单数)
        verbose_name = '作者'
        #3.定义实体类在admin中的显示名称(复数)
        verbose_name_plural = verbose_name

class Book(models.Model):
    title = models.CharField(max_length=50)
    publicate_date = models.DateField()







