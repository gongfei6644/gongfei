from django.db import models
from django.contrib.auth.models import AbstractUser


SEX_CHOICES = (
    (0,'男'),
    (1,'女'),
)

BANK_CHOICES = (
    (0,'ICBC'),
    (1,'CBC'),
    (2,'BC'),
    (3,'ABC'),
    (4,'CCB'),
    (5,'Alipay'),
)

# Create your models here.
# 用户表
class UserInfo(AbstractUser):
    email = models.EmailField(verbose_name="邮箱")
    uphone = models.CharField(verbose_name="电话", max_length=50, null=True)
    #     role角色B INc
    realname = models.CharField(verbose_name="真实姓名", max_length=50, null=True)
    idenity = models.CharField(verbose_name="身份证号", max_length=50, null=True)
    sex = models.IntegerField(verbose_name="性别", choices=SEX_CHOICES, default=0)

    def __str__(self):
        return self.username

    def get_sex(self):
        if self.sex == 0:
            return u'男'
        else:
            return '女'

    # def get_url(self):
    #     url = 'http://localhost:8001/user?id='+self.id
    #     return url
    #
    # http: // localhost: 8001 / user?id=1
    # http: // localhost: 8001 / user?id=2

    class Meta:
        # db_table = "Users"
        verbose_name="用户列表"
        verbose_name_plural="用户列表展示"


# 银行卡表
class BankCard(models.Model):
    user = models.ForeignKey(UserInfo)
    bank = models.IntegerField(verbose_name="银行", choices=BANK_CHOICES, default=0)
    bankNo = models.CharField(verbose_name="银行卡号", max_length=50,null=True)
    bankpwd = models.CharField(verbose_name="交易密码", max_length=200, null=True)

    def __str__(self):
        return self.user.username