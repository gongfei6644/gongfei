from django.db import models
from userinfo.models import UserInfo

EXAMIN_CHOICES = (
    (0,'审核中'),
    (1,'审核通过'),
    (2,'审核不通过'),
)
# Create your models here.
# 品牌表
class Brand(models.Model):
    btitle = models.CharField(verbose_name="品牌名称", max_length=50, null=True)
    logo_brand = models.ImageField(verbose_name="车标",upload_to='img/car',default='normal.png')
    is_delete = models.BooleanField(verbose_name="是否删除",default=False)

    def __str__(self):
        return self.btitle

    class Meta:
        verbose_name = "品牌表"
        verbose_name_plural = verbose_name


# 汽车表
class CarInfo(models.Model):
    brand = models.ForeignKey(Brand)
    ctitle = models.CharField(verbose_name="汽车名称", max_length=50, null=True)
    engineNo = models.CharField(verbose_name="发动机号", max_length=50, null=True)
    regist_date = models.DateField(verbose_name="上牌日期")
    mileage = models.IntegerField(verbose_name="公里数")
    price = models.DecimalField(verbose_name="价格", max_digits=8, decimal_places=2)
    debt = models.BooleanField(verbose_name="债务", default=False)
    picture = models.ImageField(verbose_name="图片", upload_to='img/cars', default='normal.png')
    promise = models.TextField(verbose_name="卖家承诺")
    isPurchase = models.BooleanField(verbose_name="是否购买", default=False)
    isDelete = models.BooleanField(verbose_name="是否删除", default=False)
    examine = models.IntegerField(verbose_name="审核进度", choices=EXAMIN_CHOICES, default=0)
    user = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "车辆表"
        verbose_name_plural = verbose_name


