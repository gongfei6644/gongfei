# 采集数据标准化

### 依赖生成
    1. 生成requirements.tx文件：pip freeze > requirements.txt
    2. 安装依赖：pip install -r requirements.txt


### 开发模式：
    1. 启动flask应用需设置FLASK_APP,：
    
        windows: set FLASK_APP=flask_server.py
        linux: export FLASK_APP=flask_server.py
    2. 使用python命令启动：python flask_server.py
    
    
### uwsgi启动命令
    /usr/local/nginx/uwsgi/uwsgi --ini /usr/local/nginx/uwsgi/uwsgi.ini --wsgi-file /usr/local/daq-std/flask_server.py
### gunicorn 启动命令
    gunicorn -c /usr/local/gunicorn/gunicorn.conf renting_flask_server:app -t 30000 --preload
    gunicorn：如果未设置软连接需要绝对路径
    -t: timeout 由于统计时间较长，所以timeout时间设置长一些，同时对应的nginx server timeout时间也设置长一些，避免超时异常
    --preload： 避免多个进程同时调度统计邮件发送多次
