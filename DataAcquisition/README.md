## 房讯通案例采集项目


### SCRAPY创建项目：
    1. 创建工程: scrapy startproject oschina_crawler
    2. 创建爬虫程序: scrapy genspider oschina www.oschina.net/blog
    3. 编写相关代码
    4. 执行爬虫(***该命令必须在项目根路径执行***): scrapy crawl oschina_crawler
    5. 调试: 新建debug.py文件，然后在debug.py的执行configurations里配置Parameters为：crawl oschina
    
###  创建依赖文件   
* 生成requirements.tx文件：`pip freeze > requirements.txt`
    
* 安装依赖：`pip install -r requirements.txt`
    
### 启动方式：   
* 多SPIDER启动方式: `nohup scrapy crawl fangtan_list fangtan_detail > /dev/null 2>&1 &`
    
* 持久化任务到磁盘目录: `scrapy crawl somespider -s JOBDIR=目录`
    
* 单任务 + 自定义日志文件: `scrapy crawl somespider -a logfile=xxx.log`

#### 项目爬虫启动命令：
    scrapy crawl fangtan_cities -a logfile=scrapy_fangtan_cities.log
    scrapy crawl fangtan_list -a logfile=scrapy_fangtan_list.log
    scrapy crawl fangtan_detail -a logfile=scrapy_fangtan_detail.log
    
    scrapy crawl house365_cities -a logfile=scrapy_house365_cities.log
    scrapy crawl house365_list -a logfile=scrapy_house365_list.log
    scrapy crawl house365_detail -a logfile=scrapy_house365_detail.log
    
    crawl anjuke_cities_community -a logfile=anjuke_cities_community.log

### 注意 
需将scheduler里的sched_persist_cases.py脚本保证时刻运行； <br>
如要确保统计数据的发送，那么sched_field_statis.py同样需要确保时刻运行。
    
保持调度脚本不断运行的方法

    1./scripts/shell/sched_persist.sh
    2.使用系统定时任务:
        输入：crontab -e
        编辑，如每1分钟检查一次：
        */1 * * * * /usr/bin/sh /usr/local/FxtDataAcquisition/scripts/shell/sched_persist.sh check
        */5 * * * * /usr/bin/sh /usr/local/FxtDataAcquisition/scripts/shell/sched_statis.sh check
    3.查看脚本是否启动： ps -ef | grep /usr/local/FxtDataAcquisition   或者 通过上面脚本用status查看
运行时会报FxtDataAcquisition.**模块找不到，需将项目目录加到环境变量：<br>
    `export PYTHONPATH=.:$PYTHONPATH:/usr/local/FxtDataAcquisition` <br>
或在被执行的脚本加入如下代码，注意查看路径是否正确：<br>
    `sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))`
    
#### 定期重命名mongodb表名启动方式
    1.手动启动：./mongo_collection_rename > /usr/local/mongo_collection_rename.log 2>&1
    2.定时启动：crontab -e
        0 0 1 * * /usr/local/mongo_collection_rename > /usr/local/mongo_collection_rename.log 2>&1
