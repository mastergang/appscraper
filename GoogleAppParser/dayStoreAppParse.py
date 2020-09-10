# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import os
os.environ["NLS_LANG"] = ".AL32UTF8"

from bs4 import BeautifulSoup
from Module.DBconnect import DB
from datetime import date, timedelta, datetime
from network.webDriver import chromeDriver
from parseApp.appInfoParser import AppInfo
from Module.DBContainer import Container
import time
import logging.handlers
from Module.LogFunction import Log

def AppInsertFunction():
    container.newAppInsertSmart(db, access_day, country_type, store_type, rank_no, smart_id, app_name, package_name,
                                category_name, provider_info, down_cnt, review_cnt, review_score_info, review_num[1],
                                review_num[2], review_num[3], review_num[4], review_num[5], update_name, site,
                                developer_info, dev_info, site_name)

def LogFunction():
    Log.LogFunction_day_store_APP(app_name, package_name, category_name, provider_info, str(down_cnt), str(
        review_cnt), review_score_info, str(review_num[1]), str(review_num[2]), str(review_num[3]), str(
        review_num[4]), str(review_num[5]), update_name, site, developer_info, dev_info)

# ( 일간 ) tb_smart_playstore_app_rank 에 들어가있는 모든 app 파싱
if __name__ == "__main__":
    print("Google PlayStore Pasering Program Start...")
    db = DB()
    driver = chromeDriver()
    container = Container()
    appInfo = AppInfo()
    Log = Log()
    try:
        dt = datetime.now()
        db.connect()
        proc_day = dt.strftime('%Y/%m/%d %H:%M:%S')
        yesterday = date.today() - timedelta(1)
        access_day = dt.strftime('%Y%m%d')
        Log.Log_Daystoreapp_Start()
        Package_list = container.getRankElem(db, access_day)
        # db select한 결과값 list
        detailList = {}
        s = 0
        for smart_info in Package_list:
            s = s + 1
            detailList[s] = list(smart_info)

        for i in detailList:
            # detailList[0] = package, detailList[1] = STORE_COUNTRY, detailList[2] = STORE_TYPE, detailList[3] = rank_no , detailList[4] = access_day
            # DB에서 가져온 패키지명 리스트화 (url_text 형성)
            url_text = 'https://play.google.com/store/apps/details?id={}'.format(detailList[i][0])

            # 파싱할 페이지 가져오기.

            driver.get(url_text)
            time.sleep(2)
            # BS4를 사용하기 위한 코드
            try:
                html_text = driver.getHtml()
                time.sleep(2)
                bs_view = BeautifulSoup(html_text, 'html.parser')
            except AttributeError:
                print("We're sorry, the requested URL was not found on this server.")

            try:
                # -------------------App 세부 정보 파싱 smart!-------------------
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
                smart_id = ''
                country_type = detailList[i][1]
                store_type = detailList[i][2]
                rank_no = detailList[i][3]
                package_name = detailList[i][0]
                try:
                    AppInsertFunction()
                    LogFunction()
                except UnicodeEncodeError:
                    try:
                        app_name = appInfo.app_name_ascii(bs_view)
                        AppInsertFunction()
                        LogFunction()
                    except:
                        app_name = appInfo.app_name_euckr(bs_view)
                        AppInsertFunction()
                        LogFunction()
            except:
                smart_id = ''
                country_type = detailList[i][1]
                store_type = detailList[i][2]
                rank_no = detailList[i][3]
                package_name = detailList[i][0]
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
                        try:
                            app_name = appInfo.app_name_ascii(bs_view)
                            AppInsertFunction()
                            LogFunction()
                        except:
                            pass

    finally:
        driver.close()
        db.disconnect()
        print("Google PlayStore Pasering Program END...")
        Log.Log_Daystoreapp_End()