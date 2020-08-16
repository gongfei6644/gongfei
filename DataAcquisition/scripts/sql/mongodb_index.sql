# 小区信息表唯一索引
db.dat_project_info.ensureIndex({uid: 1}, {unique: true, background: true});
db.dat_project_info.createIndex({source_link:1}, {background:true});
db.dat_project_info.createIndex({data_source:1, city: 1, d_status: 1, detail_time:1}, {background: true});