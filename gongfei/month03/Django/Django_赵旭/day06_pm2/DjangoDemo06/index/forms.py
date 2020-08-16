from django import forms
from .models import *

#为level控件准备初始化数据
LEVEL_CHOICE = (
    ("1","好评"),
    ("2","中评"),
    ("3","差评"),
)

#描述一个表示评论内容的表单类
#控件1-评论标题(title)-文本框
#控件2-电子邮件(email)-邮件框
#控件3-评论内容(message)-多行文本域
#控件4-评论级别(level)-下拉列表
#控件5-是否保存(isSaved)-复选框
class RemarkForm(forms.Form):
    # 描述一个表示评论内容的表单类
    # 控件1-评论标题(title)-文本框
    # label:表示的是控件前的文本
    title = forms.CharField(
        required=True,
        label='标题',
        error_messages = {
            'required':'请填写您的标题'
        }
    )
    # 控件2-电子邮件(email)-邮件框
    email = forms.EmailField(
        label='邮箱',
    )
    # 控件3-评论内容(message)-多行文本域
    # widget=forms.Textarea 目的是将当前的控件变为多行文本域
    message = forms.CharField(
        label='内容',
        widget=forms.Textarea
    )
    # 控件4-评论级别(level)-下拉列表
    level = forms.ChoiceField(
        label='级别',
        choices=LEVEL_CHOICE
    )
    # 控件5-是否保存(isSaved)-复选框
    isSaved = forms.BooleanField(label='保存')

class RegisterForm(forms.ModelForm):
    # uname = forms.CharField(label='姓名')
    # upwd = forms.CharField(label='密码')
    # uage = forms.IntegerField(label='年龄')
    # uemail = forms.EmailField(label='邮箱')
    class Meta:
        model = Users
        fields = "__all__"
        labels = {
            "uname" : "姓名",
            "uage" : "年龄",
            "upwd" : "密码",
            "uemail" : "邮箱",
        }

class LoginForm(forms.ModelForm):
    class Meta:
        #1.model:指定关联的实体类
        model = Users
        #2.fields:指定显示的属性
        fields = ["uname","upwd"]
        #3.labels:指定每个属性对应的label
        labels = {
            "uname" : "登录名称",
            "upwd" : "登录密码"
        }

class InfoForm(forms.Form):
    uname = forms.CharField(
        label = "用户名称",
        widget = forms.TextInput(
            attrs = {
                'class':'form-control',
                'placeholder':"请输入用户名称",
            }
        )
    )

    upwd = forms.CharField(
        label = '用户密码',
        widget = forms.PasswordInput(
            attrs = {
                'class':'form-control',
                'placeholder':'请输入密码',
            }
        )
    )

    uemail = forms.EmailField(
        label = '电子邮件',
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '请输入邮箱',
            }
        )
    )

    url = forms.CharField(
        label='个人主站',
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入网址',
            }
        )
    )












