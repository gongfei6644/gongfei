def foo():
    return [lambda x:i+x for i in range(4)]
print(foo())
print([x(3) for x in foo()])



今日工作内容：
1.学习慕课网Django项目。主要是模板的继承，前端页面数据分页展示完成了20%（主要有课程机构的展示与筛选）。