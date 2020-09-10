# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import os
os.environ["NLS_LANG"] = ".AL32UTF8"

from Module.DBconnect import DB
from datetime import date, timedelta, datetime
from Module.DBContainer import Container
from parseApp.appInfoParser import AppInfo
from Module.LogFunction import Log
import time
import logging.handlers

def LogFunction_pro():
    Log.LogFunction_provider_id(pproid, smart_id)

def LogFunction_site():
    Log.LogFunction_site_id(site_id, smart_id)

if __name__ == "__main__":
    print("Google PlayStore Pasering Program Start...")

    db = DB()
    Log = Log()
    container = Container()
    appInfo = AppInfo()
    try:
        Log.Log_updateProvider_Start()
        db.connect()

        # date
        dt = datetime.now()
        proc_day = dt.strftime('%Y/%m/%d %H:%M:%S')
        yesterday = date.today() - timedelta(1)
        start_day = (date.today() - timedelta(7)).strftime('%Y%m%d')
        access_day = dt.strftime('%Y%m%d')
        print(start_day + " ~ " + access_day)

        # 오늘 기준 new app get
        App_Pack = container.getNewAppElem(db, access_day)
        # tb_smart_provider_pattern에서 PACKAGE_NAME, PRO_ID, SITE_ID get
        provider_pattern_Pack = container.getProviderPattern(db)

        # db select한 결과값 list
        a = 0
        smart_detail = {}
        for App_info in App_Pack:
            a = a + 1
            smart_detail[a] = list(App_info)
        p = 0
        pattern_detail = {}
        for pattern_info in provider_pattern_Pack:
            p = p + 1
            pattern_detail[p] = list(pattern_info)

        # ﻿ORA-01861 date 포맷 변환하여 오류 해결
        container.alertDate(db)

        # ------------------------------ pro_id&smart_app_name update START------------------------------
        container.insertAppNameExisting(db, access_day)
        for x in smart_detail:
            # tb_smart_provider_pattern 비교
            smart_id = str(smart_detail[x][1])
            site = smart_detail[x][3]
            category_name = smart_detail[x][4]
            down_cnt = smart_detail[x][5]
            app_name = smart_detail[x][6]
            # 문자열 치환
            URL_LINK = appInfo.site_name(site)

            for y in pattern_detail:
                # startswith는 pattern 비교 이기 때문에 완벽하게 같지않고 앞부분과 비슷한 name pattern을 가진다면 true가 반환됨.
                if smart_detail[x][0].startswith(pattern_detail[y][0]):
                    pproid = str(pattern_detail[y][1])
                    container.update_SmartProvider(db, pproid, smart_id)
                    LogFunction_pro()

            # tb_smart_provider_name_info 비교
            provider_name = str(smart_detail[x][2])
            try:
                pproid_temp = container.getProviderName(db, provider_name)
            except:
                try:
                    provider_name_euc = provider_name.encode('euc-kr', 'ignore').decode('utf-8')
                    pproid_temp = container.getProviderName(db, provider_name_euc)
                except:
                    pass
            try:
                pproid = str(pproid_temp[0][0])
                container.update_SmartProvider(db, pproid, smart_id)
                LogFunction_pro()
            except IndexError:
                print(provider_name, "||", smart_id, "||", '0')

        # ------------------------------ pro_id&smart_app_name update END ------------------------------
            # ----------------------- insert provider_info & app_name START -----------------------
            finally:
                try:
                    site_temp1 = site.split(':')
                    try:
                        site_temp2 = site_temp1[1][2:]
                        site_temp3 = site_temp2.split('/')
                        site_name = site_temp3[0]
                        if site_temp1[0] == "mailto":
                            site = ''
                            URL_LINK = ''
                            container.insertProviderInfo(db, smart_id, provider_name, URL_LINK, site, category_name, down_cnt)
                            #container.insertProviderInfoMerge(db, access_day, URL_LINK)
                        else:
                            container.insertProviderInfo(db, smart_id, provider_name, URL_LINK, site, category_name,down_cnt)
                            #container.insertProviderInfoMerge(db, access_day, URL_LINK)
                    except:
                        container.insertProviderInfo(db, smart_id, provider_name, URL_LINK, site, category_name,down_cnt)
                        #container.insertProviderInfoMerge(db, access_day, URL_LINK)
                except AttributeError:
                    site = str(site)
                    container.insertProviderInfo(db, smart_id, provider_name, URL_LINK, site, category_name, down_cnt)
                    #container.insertProviderInfoMerge(db, access_day, URL_LINK)
            # ----------------------- insert provider_info END -----------------------
        # ------------------------------ site_id update START! ------------------------------

        for s in smart_detail:
            smart_id = str(smart_detail[s][1])
            site = smart_detail[s][3]
            # 문자열 치환
            URL_LINK = appInfo.site_name(site)
            site_url_id = container.getSiteID(db, URL_LINK)
            try:
                site_id = str(site_url_id[0][0])
                if (site_id != '0') & (site_id != '8930'):
                    if site_id == 14445:
                        container.update_Site_id_14445(db, smart_id)
                        print("3. Update >> site_id_14445 :", site_id)
                    container.update_Site_id(db, site_id, smart_id)
                    print("3. Update >> site_id :", site_id)
                    LogFunction_site()

            except IndexError:
                print("site_id is null")

            # ------------------------------- site_id update end! -------------------------------
    finally:
        db.disconnect()
        print("Google PlayStore Pasering Program END...")
        Log.Log_updateProvider_End()