from django.contrib import admin
from .models import *
# Register your models here.
# class UserInfoAdmin(admin.ModelAdmin):
    # list_display = ['id','username','password','email']
    # search_fields = ['username']


    # def save_model(self, request, obj, form, change):
    #     obj.username = 'ABC'+obj.username
    #     obj.save()
    #
    # def delete_model(self, request, obj):
    #     pass

# admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(UserInfo)
admin.site.register(BankCard)