"""
    day16 复习
    面向对象小结
    1. 封装
        设计角度：分而治之  封装变化 高内聚  低耦合

    2. 继承
        重用现有类的功能与概念，并在此基础上进行扩展。
        优点：代码复用
             统一概念（人使用交通工具，而交通工具隔离了火车/汽车等具体类的变化）
        缺点：耦合度高
             切换不灵活(员工转岗)
             解决方案：使用关联关系代替继承关系。(员工有一个岗位)
        适用性：多个类在概念上是一致的，且需要统一的处理（统一调用他们的某个成员）。
                备注：建议不要将代码复用作为继承的适用性。

    3. 多态
        同一个方法，在不同的子类中，有不同的行为。
        调用父类成员，执行子类成员。
        作用：增强程序扩展性（子类增加，不影响调用者）
        重写：子类具有与父类相同名称的方法，在调用子类时，执行子类。
             运算符重载(重写)


"""

""" 语法层面 -- 封装
class 类名:
    def __init__(self,参数):
        self.数据 = 参数
    
    @property
    def 数据(self):
        return self.__数据

    @数据.setter
    def 数据(self,value):
        self.__数据 = value

    def 方法(self):
        pass

    def __私有方法(self):
        pass
"""

"""
# 语法层面 -- 继承
class 父类1:
    def __init__(self):
        print("爸爸的init")

    def 爸爸的方法(self):
        print("爸爸的方法")

class 儿子(父类1):
    def __init__(self):
        super().__init__() # 因为希望执行爸爸的构造函数，所以通过super函数调用。
        print("儿子的init")


# 爸爸01 = 父类1()  # 只执行爸爸的构造函数
儿子01 = 儿子()  # 只执行儿子的构造函数
儿子01.爸爸的方法()
"""

"""
# 语法层面 -- 多态
class 父类1:
    def 方法(self):
        print("爸爸的方法")

class 儿子1(父类1):
    def 方法(self):
        print("儿子1的方法")

class 儿子2(父类1):
    def 方法(self):
        print("儿子2的方法")


def 调用者(爸爸):
    爸爸.方法()

调用者(儿子1())
调用者(儿子2())
"""


