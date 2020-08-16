from rest_framework import serializers
from .models import UserInfo, BankCard

class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ('username','email','sex')

    sex = serializers.SerializerMethodField('sex_field')
    def sex_field(self, obj):
        if obj.sex == 0:
            sex ="男"
        else:
            sex = "女"
        return sex

class BankCardSerializer(serializers.ModelSerializer):

    user = UserInfoSerializer(many=True,read_only=True)

    class Meta:
        model = BankCard
        fields = ('user')