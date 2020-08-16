mongodb客户端连接命令:
    -- mongo 192.168.4.103 -u admin -p fxtxq1205 --authenticationDatabase admin

# 统计某段时间标准化量
db.Dat_case.find({city: {$ne: null}, d_status: 1, is_std: 1, case_happen_date: {$ne: null},
                  detail_time: {$gte: '2019-05-05 00:00:00', $lt: '2019-05-06 00:00:00'},
                  std_date: {$gte: ISODate('2019-05-05 00:00:00'), $lt: ISODate('2019-05-06 00:00:00')}})
                .count()


db.Dat_case_46.find({city: {$nin:[null, '', '周边', '其它']}, d_status: 1, is_std: {$nin:[-1, 1]},
    case_happen_date: {$nin: [null, '']}
}).explain()


# $in正则匹配
db.Dat_case_02.find({city: '荆州市', project_name: {$in: [/\d+栋.*/, /\d+单元.*/, /\(/]}})