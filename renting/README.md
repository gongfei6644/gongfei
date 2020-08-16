## 房讯通案例采集项目


### 依赖生成及安装方式
    生成requirements.tx文件：pip freeze > requirements.txt
    安装依赖：pip install -r requirements.txt
    
 ### 应用开发流程
 1  列表
 
 1.1 创建app, 开发解析模块
 
 1.2 在manager_list模块导入解析函数,并加入映射
 
 1.3 在commons模块添加页码规则,
     如需特殊处理在common_tools中修改make_urls函数.
     
 1.4 在setting最下地方两行切换环境.
 
1.5 在manager_list模块进行测试和启动项目.

2  详情

2.1 创建app, 开发解析模块

2.2 在manager_list模块导入解析函数,并加入映射.

3  环境配置

   在setting文件最后切换环境变量config
 
4  启动文件

4.1 manager_list, 列表页爬虫启动入口

4.2 manager_detail, 详情页爬虫启动入口