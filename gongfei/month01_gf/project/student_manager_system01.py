"""
    学生管理系统
"""

class StudentModel:
    """
        学生数据模型
    """
    def __init__(self, id = 0, name = "", age = 0,score = 0):
        """
        创建学生对象
        :param id: 编号
        :param name: 姓名
        :param age: 年龄
        :param score: 成绩
        """
        self.id = id
        self.name = name
        self.age = age
        self.score = score

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value


class StudentManagerController:
    __slots__ = ("__list_stu")
    """
        学生核心逻辑控制器
    """
    def __init__(self):
        """
            创建学生管理器对象
        """
        self.__list_stu = []

    @property
    def list_stu(self):
        return self.__list_stu

    def __generate_id(self):
        # 生成编号策略：在最后一个学生编号基础上增加1
        #             如果是第一个学生，则设置为1
        # if语句的真值表达式
        return 1 if len(self.__list_stu) == 0 else self.__list_stu[-1].id + 1

    def add_student(self,stu):
        """
            添加学生对象
        :param stu: 需要添加的学生对象
        :return:
        """
        # stu.id = len(self.__list_stu) +1
        stu.id = self.__generate_id()
        self.__list_stu.append(stu)

    def remove_student(self,id):
        for item in self.__list_stu:
            if item.id == id:
                self.__list_stu.remove(item)
                return True # 表达删除成功
        return False # 表达删除失败

    def update_student(self,stu_info):
        # 需要修改的学生编号： stu_info.id
        # 需要修改的信息：stu_info.name  stu_info.age  .....
        for item in self.list_stu:
            if item.id == stu_info.id:
                item.name = stu_info.name
                item.age = stu_info.age
                item.score = stu_info.score
                return True
        return False

    def order_by_score(self):
        # 由于不允许改变self.__list_stu，所以通过切片生成一个新列表
        new_list = self.__list_stu[:]
        for r in range(len(new_list) - 1):
            for c in range(r + 1, len(new_list)):
                if new_list[r].score < new_list[c].score:
                    new_list[r], new_list[c] = new_list[c], new_list[r]
        return new_list


# 测试 添加学生
# manager = StudentManagerController()
# stu = StudentModel(name="zs",age = 24, score = 100)
# manager.add_student(stu)
#
# for item in manager.list_stu:
#     print(item.id,item.name,item.age,item.score)

# 测试 删除学生
# manager = StudentManagerController()
# stu01 = StudentModel(name="zs1",age = 24, score = 100)
# stu02 = StudentModel(name="zs2",age = 24, score = 100)
# manager.add_student(stu01)
# manager.add_student(stu02)
# result =manager.remove_student(1)
# print(result)
# for item in manager.list_stu:
#     print(item.id,item.name,item.age,item.score)

# 测试 修改学生
# manager = StudentManagerController()
# stu01 = StudentModel(name="zs1", age=24, score=100)
# manager.add_student(stu01)
# result = manager.update_student(StudentModel(2, "zss", 25, 120))
# print(result)
# for item in manager.list_stu:
#     print(item.id, item.name, item.age, item.score)

#练习：order_by_score 按照成绩降序排序（不允许改变self.__list_stu）

class StudentManagerView:
    """
        学生管理器视图类
    """
    def __init__(self):
        # 创建学生管理控制器对象
        self.__controller = StudentManagerController()


    def __display_menu(self):
        """
            显示菜单
        :return:
        """
        print("---------------------")
        print("1)添加学生")
        print("2)显示学生")
        print("3)删除学生")
        print("4)修改学生")
        print("5)按照成绩降序显示")
        print("---------------------")

    def __select_menu(self):
        """
            选择菜单
        :return:
        """
        number = input("请输入选项：")
        if number == "1":
            pass
        elif number =="2":
            pass
        elif number == "3":
            pass
        elif number == "4":
            pass
        elif number == "5":
            pass

    def main(self):
        """
            学生管理器入口
        :return:
        """
        while True:
            self.__display_menu()
            self.__select_menu()


view = StudentManagerView()
view.main()



