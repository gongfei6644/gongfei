from flask import Flask,render_template

#　创建Ｆｌａｓｋ的程序实例
app = Flask(__name__)

@app.route('/')
@app.route('/index')
#视图函数
def index():
    return "<h1>欢迎</h1>"

@app.route('/login/<name>/<age>')
def login(name,age):
    return "<h1>欢迎登录，%s,%s</h1>" % (name,age)

@app.route('/calcute/<int:n1>/<int:n2>')
def calcute(n1,n2):
    #n1 = int(n1)
    #n2 = int(n2)
    n3 = n1 + n2
    return "%d + %d = %d" %(n1,n2,n3)

@app.route('/show')
@app.route('/show/list')
@app.route('/show/<name>')
def show(name="ze"):
    return "show %s" % name

#模板
@app.route('/info')
def info():
    #返回模板文件，可以传递变量
    return render_template("01-show.html",name="flask",age=20)


if __name__ == "__main__":
    app.run(debug=True)
