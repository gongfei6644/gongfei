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

    def add_student(self,stu):
        """
            添加学生对象
        :param stu: 需要添加的学生对象
        :return:
        """
        stu.id = len(self.__list_stu) +1
        self.__list_stu.append(stu)

# 测试
manager = StudentManagerController()
stu = StudentModel(name="zs",age = 24, score = 100)
manager.add_student(stu)

for item in manager.list_stu:
    print(item.id,item.name,item.age,item.score)











