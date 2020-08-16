"""
    day17 复习
    模块module
    1. 定义： .py 文件
    2. 作用： 将代码有逻辑的组织在一起。
             便于团队开发。
    3. 导入：
        import 模块名   ：  本质就是定义一个变量，与模块代码进行关联。
        -- 使用 模块名.成员

        from  模块名 import 成员  ：  将指定成员引入到当前作用域中
        -- 直接使用 成员

        from 模块名 import * ：  将所有成员引入到当前作用域中
        -- 直接使用 成员
        -- 可能导入多个模块，其中的成员命名冲突。
        -- 不能导入隐藏成员(_成员名)

    4. 模块变量
        __name__ : 存储模块名（如果从当前模块开始运行，名称是__main__）
        if __name__ =="__main__"
            作为主模块执行的代码

        __file__:获取模块完整路径

    5.time 模块
      时间戳：从计算机元年(1970年) 到当前时间的秒数
             1553131800.7883673
      时间元组:(年份  月份  日  小时  分钟  秒  一周的第几天  一年的第几天  夏令时)
      时间戳   <-->   时间元组：略....
      时间元组 <-->  字符串：略....

"""
import  time
print(time.time())















