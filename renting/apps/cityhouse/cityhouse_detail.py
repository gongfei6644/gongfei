from lxml import etree
import datetime


class CityHouse:

    def parse_xpath(self, html_str):
        dic = {}
        now_time = datetime.datetime.now()
        dic['detail_time'] = now_time.strftime('%Y-%m-%d %H:%M:%S')
        dic['d_status'] = 1
        if html_str['str'] == '404':
            dic['d_status'] = 0
            return dic
        elif html_str['str'] == '访问页面不存在':
            dic['d_status'] = "Page missing"
            return dic
        elif html_str['str']:
            html = etree.HTML(html_str['str'])

            # 建筑面积
            try:
                dic['build_area'] = html.xpath('string(//dt[text()="面积："]/following-sibling::dd)').strip().strip('--').strip('㎡')
            except Exception as e:
                dic['build_area'] = ''

            # 行政区
            # try:
            #     dic['area'] = html.xpath('string(//span[text()="位置："]/following-sibling::a)').strip()
            # except Exception as e:
            #     dic['area'] = ''

            # 楼盘
            try:
                dic['"project_name"'] = html.xpath('string(//span[text()="小区："]/following-sibling::a)').strip()
            except Exception as e:
                dic['"project_name"'] = ''

            # 地址
            try:
                dic['address'] = html.xpath('string(//span[text()="位置："]/following-sibling::a/following-sibling::text()[1])').strip()
            except Exception as e:
                dic['address'] = ''

            # 户型
            try:
                dic['house_type'] = html.xpath('string(//dt[text()="户型："]/following-sibling::dd)').strip().strip('--').strip('--')
            except Exception as e:
                dic['house_type'] = ''

            # 所在楼层
            try:
                dic['floor_no'] = \
                    html.xpath('string(//dt[text()="楼层："]/following-sibling::dd)').strip().strip('--').split('/')[0]
            except Exception as e:
                dic['floor_no'] = ''

            # 总楼层
            try:
                dic['total_floor_num'] = \
                html.xpath('string(//dt[text()="楼层："]/following-sibling::dd)').strip().strip('--').split('/')[1]
            except Exception as e:
                dic['total_floor_num'] = ''

            # 朝向
            try:
                dic['orientation'] = \
                    html.xpath('string(//dt[text()="朝向："]/following-sibling::dd)').strip().strip('--').strip('向')
            except Exception as e:
                dic['orientation'] = ''

            # 用途
            try:
                dic['usage'] = \
                    html.xpath('string(//dt[text()="用途："]/following-sibling::dd)').strip().strip('--')
            except Exception as e:
                dic['usage'] = ''

            # 案例日期
            try:
                dic['case_happen_date'] = \
                    html.xpath('string(//dt[text()="发布时间："]/following-sibling::dd)').strip().strip('--')
            except Exception as e:
                dic['case_happen_date'] = ''
            # 配套
            try:
                dic['supporting_facilities'] = \
                    html.xpath('string(//dt[text()="附属设施："]/following-sibling::dd)').strip().strip('--').replace(' ','').replace('\n','')
            except Exception as e:
                dic['supporting_facilities'] = ''

            # 装修情况
            try:
                dic['decoration'] = html.xpath('string(//*[text()="装修"]/node())').strip().strip('--')
            except Exception as e:
                dic['decoration'] = ''
            # 租赁方式: 整租
            try:
                rent_info = html.xpath('string(//span[@class="price_big"]/parent::*[1])').strip()
                dic['rental_method'] = rent_info.split("：")[0]
            except:
                dic['rental_method'] = ""
            try:
                dic['tel'] = html.xpath('string(//span[@class="tel"])').strip()
            except:
                dic['tel'] = ""
            # 建筑年代
            try:
                dic["build_date"] = html.xpath('string(//div[@class="hs_cont_infolist column2"]//dt[contains(text(), "建筑年代：")]/following-sibling::dd[1])').strip(" 年")
            except:
                dic["build_date"] = ""
            # 押付方式
            try:
                dic["deposit_method"] = html.xpath('string(//span[contains(text(), "付款方式：")]/span)').strip()
            except:
                dic["deposit_method"] = ""
        else:
            dic['d_status'] = "err"

        # 补充字段
        dic['build_type'] = ""
        dic['house_structure'] = ""
        dic['affiliated_house'] = ""
        dic['usable_area'] = ""
        dic['remaining_years'] = ""
        dic['new_ratio'] = ""
        dic['remark'] = ""
        dic['build_name'] = ""
        dic['house_name'] = ""
        dic['currency'] = "人民币"
        dic['case_type'] = "月平方米租报盘"
        print(dic)
        return dic
