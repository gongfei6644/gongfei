"""
    day09 复习
    1. 可变/不可变对象传参：
    2. 作用域：局部 --- 函数体内部定义的变量
              全局 --- py文件内定义的变量
              函数体中，可以访问全局变量，但是必须通过global语句修改。
    3. 面向对象：
        (1)面向过程：思考问题的解决步骤，然后逐步实现。
        (2)面向对象：思考解决问题的人，然后分配职责。
        (3)同类型的多个对象，行为相同，数据不同。
        (4)语法：
            -- 类
            class 类名:
                def __init__(self,参数):
                      self.数据 = 参数

                行为
            -- 对象
            变量 = 类名(参数)
"""

def fun1(list_target):
    # 修改的是列表对象
    list_target[0] = 200

list01 = [100]
fun1(list01)
print(list01) # ?200

def fun2(list_target):
    # 修改的是变量
    list_target = [200]

list02 = [100]
fun2(list02)
print(list02) # ?100


