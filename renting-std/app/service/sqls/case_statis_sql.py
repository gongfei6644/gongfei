# -*- coding: utf-8 -*-


select_statis_sql = """
SELECT * FROM dat_staticstic_acquisitioninfo
WHERE city_name = '{}' and web_site = '{}' and crt_time = '{}'
"""

insert_statis_sql = """
INSERT INTO dat_staticstic_acquisitioninfo 
 (city_name, web_site, case_count, projectname_count, 
  buildarea_count, unitprice_count, standardized_count, crt_time)
VALUES
 ('{}', '{}', {}, {}, {}, {}, {}, '{}');
"""

update_statis_sql = """
UPDATE dat_staticstic_acquisitioninfo 
SET
 case_count = {} , 
 projectname_count = {} , 
 buildarea_count = {} , 
 unitprice_count = {} , 
 standardized_count = {}
WHERE
 id = '{}'
"""
