from flask import Flask,render_template
#创建flask的实例
app = Flask(__name__)

#注册路由
@app.route('/')
@app.route('/index')
@app.route('/index/<name>')
def index(name="游客"):
    return "<h1>首页,%s</h1>" % name

#定义动物类
class Pet(object):
    name = None
    def play(self):
        return "来和"+self.name+"玩耍吧"

@app.route('/show')
def show():
    name = "老Ｑ"
    age = 30
    dic = {
        "name":"Maria",
        "age":30
    }
    list = ["保健","唱Ｋ"]
    tup = ("ZX","DB")
    #　render_template("")返回模板字符串
    #print("%s",render_template("01-show.html"))

    #locals()将当前局部作用域中所有的局部变量转换成字典形式返回
    #print(locals())

    #实例化对象
    cat = Pet()
    cat.name = "妲己"
    s1 = "hello world"
    s2 = "  hello  "

    #key=value
    return render_template("01-show.html",params=locals())






#启动服务
if __name__ == "__main__":
    app.run(debug=True,port="5555")







