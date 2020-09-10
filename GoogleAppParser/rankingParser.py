# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import os
os.environ["NLS_LANG"] = ".AL32UTF8"

from bs4 import BeautifulSoup
from network.webDriver import chromeDriver
import logging.handlers
from Module.DBconnect import DB
from Module.DBContainer import Container
from datetime import date, timedelta, datetime
from Module.LogFunction import Log


if __name__ == "__main__":
    print("Google PlayStore Pasering Program Start...")

    db = DB()
    container = Container()
    WD = chromeDriver()
    Log = Log()
    try:
        Log.Log_ranking_Start()
        dt = datetime.now()
        db.connect()
        proc_day = dt.strftime('%Y/%m/%d %H:%M:%S')
        yesterday = date.today() - timedelta(1)
        access_day = dt.strftime('%Y%m%d')

        URL_Pack = container.getURLElem(db)
        # db select한 결과값 list
        url_list = {}
        i = 0
        for info in URL_Pack:
            i = i + 1
            url_list[i] = list(info)

        for r in url_list:
            WD.get(url_list[r][2])
            WD.exeScroll()
            try:
                html_text = WD.getHtml()
                bs_view = BeautifulSoup(html_text, 'html.parser')
            except AttributeError:
                print("We're sorry, the requested URL was not found on this server.")

            rankingCards = bs_view.findAll("div", {'class': 'b8cIId ReQCgd Q9MA7b'})
            package_href = bs_view.findAll('a', attrs={'class': 'JC71ub'})
            package_elem = {}
            i=0
            for p_no in package_href:
                i= i+1
                package_elem[i] = p_no.get('href')
            title_data = {}
            package_data = {}
            rank_no = 0
            for rank_elem in rankingCards:
                rank_no = rank_no + 1
                title_data[rank_no] = rank_elem.text
                print(title_data[rank_no])

                package_temp2 = str(package_elem[rank_no])
                package_temp = package_temp2.split('=')
                package_data[rank_no] = package_temp[1]

                app_name = title_data[rank_no].encode('euc-kr', 'ignore').decode('euc-kr')
                package_name = package_data[rank_no]
                Log.LogFunction_ranking(str(rank_no), package_name, app_name)

                store_country = url_list[r][0]
                store_type = url_list[r][1]
                container.insertRankInfo(db, access_day, store_country, store_type, str(rank_no + 1), package_name,
                                         app_name)

    finally:
        WD.close()
        db.disconnect()
        print("Google PlayStore Pasering Program END...")
        Log.Log_ranking_End()

