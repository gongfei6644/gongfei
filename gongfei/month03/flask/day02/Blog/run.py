from flask import Flask,render_template,url_for
app = Flask(__name__)

#注册路由
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/list')
def list_view():
    return render_template("child.html")





if __name__ == "__main__":
    app.run(debug=True)
