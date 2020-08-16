from flask import Flask,render_template,request,redirect

app = Flask(__name__,template_folder="t",static_folder="s")

#注册路由
@app.route('/')
def index():
    #获取请求消息头(字典)
    print(request.headers)
    #从请求消息头中获取源地址（不一定有值）
    if "Referer" in request.headers:
        print(request.headers['Referer'])

    return render_template("index.html")

@app.route('/list')
def list_view():
    # 从请求消息头中获取源地址（不一定有值）
    if "Referer" in request.headers:
        print("list-referer:",request.headers['Referer'])

    return render_template("list.html")

@app.route('/parent')
def parent():
    return render_template("parent.html")

@app.route('/child')
def child():
    return render_template("child.html")

# 请求对象
@app.route('/request')
def request_view():
    # 查看request对象内部属性
    # print(dir(request))
    # 模板文件中使用的是单独的一套模板语法，所有可迭代元素都可以使用点语法访问．
    # python文件中不能随便使用点语法
    print(request.args['uname'])

    return render_template("child.html",params=request)

# 访问表单页
@app.route('/form')
def form_view():
    return render_template("01-get.html")


# 获取get请求提交的数据
# methods设置当前地址允许的请求方式，默认get
@app.route('/get',methods=['GET','POST'])
def show():
    # request.method获取此次请求的方式
    if request.method == 'GET':
        # 获取请求携带的数据
        # get('key','default')
        print(request.args.get('uname', 'XM'))
        print(request.args.get('upwd', '123'))
        print(request.args.getlist('hobby'))

        #重定向到首页
        res = redirect('/')
        print(res)
        return res

    else:
        #获取post请求提交的数据
        print(request.form.get('uname'))
        print(request.form['upwd'])
        print(request.form.getlist('hobby'))
        #获取所有上传的文件
        print(request.files)
        #保存文件
        f = request.files['uimg']
        #获取文件名
        filename = f.filename
        #保存至指定的文件夹
        #获取当前的日期字符串作为文件名
        #datetime.datetime.now()
        #分割文件后缀
        #保存之前手动拼接文件后缀
        f.save('s/images/'+filename)

        return "post　ok"



if __name__ == "__main__":
    app.run(debug=True)
