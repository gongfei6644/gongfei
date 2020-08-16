import datetime

from pymysql import connect

from setting import config
from utils.constants import WEBSITE_PAGESIZE


def get_pagesize_config():

    # 创建链接
    try:
        conn = connect(**config.MYSQL_INFO)
    except Exception as e:
        r = WEBSITE_PAGESIZE
        print("连接mysql异常{}, {}".format(config.MYSQL_INFO["host"], e))
    else:
        with conn.cursor() as cur:
            # 执行sql语句
            cur.execute("select * from dat_collecttionsettinginfo_pagecount")
            content = cur.fetchall()
            sources = {source for _, _, source, _ in content}
            r = {source: {} for source in sources}
            for index, level, source, count in content:
                r[source].update({level: count})
    try:
        conn.close()
    except Exception as e:
        print("关闭MySQL异常{}".format(config.MYSQL_INFO["host"], e))
    if r:
        return r
    else:
        print("MySQL数据city_pagesize为空表{}".format("dat_collecttionsettinginfo_pagecount"))



if __name__ == '__main__':
    r = get_pagesize_config()
    print(r)
