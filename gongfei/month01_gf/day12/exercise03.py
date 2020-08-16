"""
    练习：小明在招商银行取钱。
"""

class Person:
    def __init__(self,name,money):
        self.name = name
        self.money = money

    @property
    def name(self):
        return  self.__name

    @name.setter
    def name(self,value):
        self.__name = value

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, value):
        self.__money = value


class Bank:
    def __init__(self,name,money):
        self.name = name
        self.total_money = money

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def total_money(self):
        return self.__total_money

    @total_money.setter
    def total_money(self, value):
        self.__total_money = value

    def draw_money(self,value,person):
        if self.total_money >= value:
            self.total_money -= value
            person.money += value
        else:
            raise  ValueError("没钱啦")


xm = Person("小明",0)
bank = Bank("招商银行",100000)
bank.draw_money(1000,xm)

print("取完钱之后的小明：",xm.money)
print("取完钱之后的银行：",bank.total_money)




