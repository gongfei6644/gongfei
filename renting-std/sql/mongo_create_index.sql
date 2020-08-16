# 为Dat_case表添加索引
db.Dat_case.createIndex({city:1, d_status:1, detail_time:1, is_std:1, case_happen_date:1, std_date:1,
                         data_source:1, project_name:1, house_area:1, unitprice:1, crt_time: 1},
                        {background:true, name: 'idx_01'});



# 为std_case表添加索引
db.std_case.createIndex({case_happen_date:1, status:1, city_name:1, area_name:1,
                         project_name:1, usage:1, building_type:1, data_source:1},
                        {background:true, name: 'idx_01'});
db.std_case.createIndex({case_id:1, md5_:1}, {background:true, name: 'idx_02'});


