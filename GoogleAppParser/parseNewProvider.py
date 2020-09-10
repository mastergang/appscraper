# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import os
os.environ["NLS_LANG"] = ".AL32UTF8"


from bs4 import BeautifulSoup
from Module.DBconnect import DB
from datetime import date, timedelta, datetime
from network.webDriver import chromeDriver
from Module.DBContainer import Container
from parseApp.appInfoParser import AppInfo
import logging.handlers
from Module.LogFunction import Log

def AppInsertFunction():
    container.newAppInsertSmart(db, access_day, country_type, store_type, rank_no, smart_id, app_name, package_name,
                                category_name, provider_info, down_cnt, review_cnt, review_score_info, review_num[1],
                                review_num[2], review_num[3], review_num[4], review_num[5], update_name, site,
                                developer_info, dev_info, site_name)


def LogFunction():
    log_message_list = app_name, smart_id, package_name, category_name, provider_info, str(down_cnt), str(
        review_cnt), review_score_info, str(review_num[1]), str(review_num[2]), str(review_num[3]), str(
        review_num[4]), str(review_num[5]), update_name, site, developer_info, dev_info, site_name
def LogFunction_smart_id():
    Log.LogFunction_smart_id(smart_id, package_name)

if __name__ == "__main__":
    print("Google PlayStore Pasering Program Start...")
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
    db = DB()
    driver = chromeDriver()
    container = Container()
    appInfo = AppInfo()
    Log = Log()
    try:
        db.connect()
        # date
        dt = datetime.now()
        proc_day = dt.strftime('%Y/%m/%d %H:%M:%S')
        yesterday = date.today() - timedelta(1)
        start_day = (date.today() - timedelta(7)).strftime('%Y%m%d')
        access_day = dt.strftime('%Y%m%d')
        print(start_day + " ~ " + access_day)
        Log.Log_newProvider_Start()

        # ﻿date format check
        #dateFormat = container.getDateFormat(db)
        #print(dateFormat)
        # ﻿ORA-01861 date 포맷 변환하여 오류 해결
        container.alertDate(db)

        smart_Pack = container.getSmartNewElem(db)
        daystore_Pack = container.getDayStoreElem(db)

        # db select한 결과값 list
        smart_detail = {}
        s = 0
        for smart_info in smart_Pack:
            s = s + 1
            smart_detail[s] = list(smart_info)

        day_app_detail = {}
        s = 0
        for smart_info in daystore_Pack:
            s = s + 1
            day_app_detail[s] = list(smart_info)

        parse_list = {}
        print(">> new App Parsing Stmart >>")
        for i in smart_detail:
            package_name = smart_detail[i][0]
            smart_id = str(smart_detail[i][1])
            # 굳이 안해도 되는 url 찾기 (구글 플레이 스토어 파싱한 부분 비교)

            for y in day_app_detail:
                if smart_detail[i][0] == day_app_detail[y][0]:
                    print(smart_detail[i][0], day_app_detail[y][0])
                    container.update_Smart_id(db, smart_id, package_name)
                    LogFunction_smart_id()
                else:
                    parse_list[i] = smart_detail[i][0]

        for i in smart_detail:
            package_name = smart_detail[i][0]
            smart_id = str(smart_detail[i][1])
            for y in parse_list:
                if smart_detail[i][0] == parse_list[y]:
                    # 파싱할 url 설정 및 페이지 가져오기.
                    url_text = 'https://play.google.com/store/apps/details?id={}'.format(smart_detail[i][0])
                    driver.get(url_text)

                    # BS4를 사용하기 위한 코드
                    try:
                        html_text = driver.getHtml()
                        bs_view = BeautifulSoup(html_text, 'html.parser')
                    except AttributeError:
                        print("We're sorry, the requested URL was not found on this server.")

                    try:
                        # -------------------App 세부 정보 파싱 smart!-------------------
                        country_type = ""
                        store_type = "newApp"
                        rank_no = ""
                        app_name = appInfo.app_name(bs_view)
                        review_score_info = appInfo.review_score(bs_view)
                        review_width_list = appInfo.review_width(bs_view)
                        provider_info = appInfo.provider_name(bs_view)
                        category_name = appInfo.category_name(bs_view)
                        review_cnt = appInfo.review_cnt(bs_view)
                        down_update_list = appInfo.down_update_elem(bs_view)
                        update_name = appInfo.down_update_elem(bs_view)[0]
                        down_cnt = appInfo.down_update_elem(bs_view)[1]
                        site = appInfo.site(bs_view)
                        site_name = appInfo.site_name(site)
                        developer_info = appInfo.developer_id(bs_view)[0]
                        dev_info = appInfo.developer_id(bs_view)[1]
                        r = 0
                        review_num = {}
                        for width in review_width_list:
                            r = r + 1
                            review_num[r] = width

                        # --------------------App 세부 정보 파싱 end!--------------------
                        print(app_name, down_cnt, review_cnt, review_score_info,
                              review_num[1], review_num[2], review_num[3], review_num[4], review_num[5],
                              proc_day, update_name, category_name, site, site_name, provider_info, developer_info,
                              dev_info)

                        try: 
                            # facebook이 실공급자가 아닌 경우 
                            if (provider_info != 'Facebook') & (site_name == 'www.facebook.com'):
                                site = ''
                                AppInsertFunction()
                                LogFunction()
                            else:
                                AppInsertFunction()
                                LogFunction()
                        except UnicodeEncodeError:
                            app_name = appInfo.app_name_ascii(bs_view)
                            AppInsertFunction()
                            LogFunction()
                    except:
                        try:
                            try:
                                app_name = appInfo.app_name_ascii(bs_view)
                                AppInsertFunction()
                                LogFunction()
                            except AttributeError:
                                print("Cannot Found URL")
                        except:
                            try:
                                app_name = appInfo.app_name_euckr(bs_view)
                                AppInsertFunction()
                                LogFunction()
                            except:
                                app_name = appInfo.app_name_euckr(bs_view)
                                try:
                                    AppInsertFunction()
                                    LogFunction()
                                except:
                                    pass

    finally:
        driver.close()
        db.disconnect()
        print("Google PlayStore Pasering Program END...")
        Log.Log_newProvider_Start()
