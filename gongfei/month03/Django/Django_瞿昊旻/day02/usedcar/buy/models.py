from django.db import models
from userinfo.models import UserInfo
from sale.models import CarInfo

ORDER_CHOICES = (
    (0,'未支付'),
    (1,'已支付'),
    (2,'交易成功'),
    (3,'交易失败'),
)
# Create your models here.
# 购买意愿表
class Cart(models.Model):
    suser = models.ForeignKey(UserInfo)
    car = models.ForeignKey(CarInfo)
    price = models.DecimalField(verbose_name="价格", max_digits=8, decimal_places=2)
    mileage = models.IntegerField(verbose_name="公里数")
    carDetail = models.TextField(verbose_name="车辆信息")

    def __str__(self):
        return self.suser.username

    class Meta:
        verbose_name = "购买意愿表"
        verbose_name_plural= verbose_name

# 交易记录表
class Orders(models.Model):
    buser = models.ForeignKey(UserInfo)
    suser = models.ForeignKey(UserInfo)
    price = models.DecimalField(verbose_name="价格", max_digits=8, decimal_places=2)
    ordertime = models.DateTimeField(verbose_name="成交时间",auto_now_add=True)
    car = models.OneToOneField(CarInfo,verbose_name="车辆信息")
    orderStatus = models.IntegerField(verbose_name="订单状态", choices=ORDER_CHOICES,default=0)
    isDelete = models.BooleanField(verbose_name="是否删除", default=False)

    def __str__(self):
        return self.buser.username

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name