# coding: utf-8

# Module SQL 쿼리
class Container:
    # ---------------- select sql ----------------

    def getURLElem(self, db):
        return db.execute("select STORE_COUNTRY, STORE_TYPE, URL from TB_SMART_PLAYSTORE_URL")

    def getRankElem(self, db, access_day):
        return db.execute("select PACKAGE_NAME, STORE_COUNTRY, STORE_TYPE, rank_no from tb_smart_playstore_app_rank  where access_day = '" + access_day + "'")

    def getNewAppElem(self, db, access_day):
        return db.execute("select PACKAGE_NAME, SMART_ID, PROVIDER_NAME, SITE, CATEGORY_NAME, DOWN_CNT, APP_NAME from tb_smart_day_playstore_app where SMART_ID is not null and STORE_TYPE = 'newApp' and access_day = '" + access_day + "'")

    def getDayStoreElem(self, db):
        return db.execute("select PACKAGE_NAME, SMART_ID, STORE_COUNTRY, STORE_TYPE, RANK_NO, APP_NAME, PACKAGE_NAME, CATEGORY_NAME, PROVIDER_NAME, DOWN_CNT, REVIEW_CNT, REVIEW_SCORE, REVIEW1, REVIEW2, REVIEW3, REVIEW4, REVIEW5, UPDATE_DAY, SITE, DEVELOPER_ID, DEV_ID  from tb_smart_day_playstore_app ")

    # smart_id와 package_name 가져온다.
    def getSmartElem(self, db, access_day):
        return db.execute(
            "select package_name, smart_id from tb_smart_app_info where EF_TIME > to_date('" + access_day + "','YYYY/MM/DD')-5 and  EXP_TIME > to_char(sysdate, 'YYYY-MM-DD') and  smart_id not in ( select smart_id from tb_smart_provider_info )")

    def getSmartNewElem(self, db):
        return db.execute(
            "select package_name, smart_id from tb_smart_app_info where EF_TIME > to_char(sysdate, 'YYYY-MM-DD') and  EXP_TIME > to_char(sysdate, 'YYYY-MM-DD')")

    def getProvider_smartid(self, db):
        return db.execute(
            "select smart_id from tb_smart_provider_info")

    def getTempSmartData_test(self, db, access_day):
        return db.execute(
            "select package_name, smart_id from temp_sjhyun_smart_app_info where EF_TIME > to_char(sysdate, 'YYYY-MM-DD') and  EXP_TIME > to_char(sysdate, 'YYYY-MM-DD')")


    # pro_id 가져옴.
    def getProviderName(self, db, provider_name):
        return db.execute("select pro_id from ( select PRO_ID, rank() over(order by pro_name) rnk from tb_smart_provider_name_info where lower(pro_name) like lower('"+provider_name+"') ) where rnk = 1 ")

    # provider package_name, pro_id, site_id를 가져온다.
    def getProviderPattern(self, db):
        return db.execute("select PACKAGE_NAME, PRO_ID, SITE_ID from tb_smart_provider_pattern")

    # site_id 가져옴.
    def getSiteID(self, db, URL_LINK):
        return db.execute("select  site_id from vi_site_info where URL_LINK = '" + URL_LINK + "'")

    # date 포맷 확인을 위한 쿼리
    def getDateFormat(self, db):
        return db.execute("select sys_context('USERENV','NLS_DATE_FORMAT') ndf from dual")

    # date 포맷변환
    def alertDate(self, db):
        return db.execute("alter session set nls_date_format='YYYY-MM-DD'")

    
    
    # ---------------- update sql ----------------

    # pro_id update_기존
    def update_SmartProvider(self, db, pproid, smart_id):
        return db.execute(
            "update tb_smart_app_info set pro_id = " + pproid + " where smart_id = " + smart_id)

    # site_id update_기존
    def update_Site_id_14445(self, db, smart_id):
        return db.execute(
            "update tb_smart_app_info set site_id = 178, pro_id = 3126 where smart_id = " + smart_id)

    # site_id update_기존
    def update_Site_id(self, db, site_id, smart_id):
        return db.execute(
            "update tb_smart_app_info set site_id = " + site_id + " where smart_id = " + smart_id)

    def update_Smart_id(self, db, smart_id, package_name):
        return db.execute("update tb_smart_day_playstore_app set smart_id = " + smart_id + " where package_name = '" + package_name +"'")

    def update_SmartAppName(self, db, access_day):
        return db.execute("update tb_smart_app_name_info a set EXP_TIME = sysdate WHERE ROWID > (SELECT MIN(ROWID) FROM tb_smart_app_name_info b WHERE a.smart_id = b.smart_id) and ef_time >= '"+access_day+"'")

    def update_provider_name(self, db, access_day):
        return db.execute("update  tb_smart_provider_info a " + \
                            "set (domain_url, path_url, category, installs) = " + \
                            "( select domain_url, site, CATEGORY_NAME, DOWN_CNT " + \
                            "from tb_smart_day_playstore_app b " + \
                            "where b.access_day = '"+access_day+"' " + \
                            "and b.STORE_TYPE = 'newApp' " + \
                            "and a.smart_id = b.smart_id " + \
                            "and a.pro_name = b.provider_name)")


    # ---------------- insert sql ----------------

    def insertRankInfo(self, db, access_day, store_country, store_type, rank_no, package_name, app_name):
        sql = "insert into tb_smart_playstore_app_rank values(:access_day, :store_country, :store_type, :rank_no, :package_name, :app_name, sysdate)"
        db.cursor.execute(sql, {'access_day': access_day, 'store_country': store_country, 'store_type': store_type, 'rank_no': rank_no, 'package_name': package_name, 'app_name': app_name})
        db.db.commit()


    # smart_id 있는 테이블 기준 + new_app type 추가
    def newAppInsertSmart(self, db, access_day, STORE_COUNTRY, STORE_TYPE, RANK_NO, SMART_ID, APP_NAME, PACKAGE_NAME, CATEGORY_NAME, PROVIDER_NAME, DOWN_CNT, REVIEW_CNT, REVIEW_SCORE, REVIEW1, REVIEW2, REVIEW3, REVIEW4, REVIEW5, UPDATE_DAY, SITE, DEVELOPER_ID, DEV_ID, DOMAIN_URL):
        sql = "insert into tb_smart_day_playstore_app values (:access_day, :STORE_COUNTRY, :STORE_TYPE, :RANK_NO, :SMART_ID, :APP_NAME, :PACKAGE_NAME, :CATEGORY_NAME, :PROVIDER_NAME, :DOWN_CNT, :REVIEW_CNT, :REVIEW_SCORE, :REVIEW1, :REVIEW2, :REVIEW3, :REVIEW4, :REVIEW5, :UPDATE_DAY, :SITE, sysdate, :DEVELOPER_ID, :DEV_ID, :DOMAIN_URL)"
        db.cursor.execute(sql, {'ACCESS_DAY': access_day, 'STORE_COUNTRY': STORE_COUNTRY, 'STORE_TYPE': STORE_TYPE,
                                'RANK_NO': RANK_NO, 'PACKAGE_NAME': PACKAGE_NAME, 'APP_NAME': APP_NAME, 'DOWN_CNT': DOWN_CNT,
                                'REVIEW_CNT': REVIEW_CNT, 'REVIEW_SCORE': REVIEW_SCORE, 'REVIEW1': REVIEW1,
                                'REVIEW2': REVIEW2, 'REVIEW3': REVIEW3, 'REVIEW4': REVIEW4, 'REVIEW5': REVIEW5,
                                'UPDATE_DAY': UPDATE_DAY, 'CATEGORY_NAME': CATEGORY_NAME, 'site': SITE,
                                'smart_id': SMART_ID, 'provider_name': PROVIDER_NAME, 'DEVELOPER_ID': DEVELOPER_ID, 'DEV_ID': DEV_ID, 'DOMAIN_URL': DOMAIN_URL})
        db.db.commit()        
    # tb_smart_provider_info & tb_smart_app_name_info ( smart_id )
    def insertProviderInfo(self, db, smart_id, provider_name, site_name, site, category_name, down_cnt):
        sql = "insert into tb_smarT_provider_info values (:smart_id, :pro_name, :domain_url, :path_url, :category, :installs )"
        db.cursor.execute(sql, {'smart_id': smart_id, 'pro_name': provider_name, 'domain_url': site_name, 'path_url': site, 'category': category_name, 'installs': down_cnt})

    def insertAppNameInfo(self, db, smart_id, app_name):
        sql = "insert into tb_smart_app_name_info values (:smart_id, :app_name, sysdate,to_date('9999/01/01','yyyy/mm/dd'))"
        db.cursor.execute(sql, {'smart_id': smart_id, 'app_name': app_name})

    def insertAppNameExisting(self, db, access_day):
        sql = "insert into tb_smart_app_name_info " + \
            "select a.smart_id, a.app_name, sysdate, to_date('9999/01/01','yyyy/mm/dd') " + \
            "from tb_smart_day_playstore_app a, tb_smart_app_name_info b " + \
            "where a.access_day = '"+access_day+"' " + \
            "and STORE_TYPE = 'newApp' " + \
            "and a.smart_id = b.smart_id " + \
            "and a.app_name != b.app_name"
        db.cursor.execute(sql)

    # insert provider_info merge
    def insertProviderInfoMerge(self, db, access_day, site_name):
        sql = "MERGE INTO tb_smart_provider_info c " + \
            "USING tb_smart_day_playstore_app e " + \
            "ON (e.access_day = '" + access_day + "' and e.STORE_TYPE = 'newApp' and e.smart_id = c.smart_id and c.pro_name = e.PROVIDER_NAME) " + \
            "WHEN MATCHED THEN " + \
                      "UPDATE SET " + \
                            "c.DOMAIN_URL = '" + site_name + "', " + \
                            "c.PATH_URL = e.SITE, " + \
                            "c.installs = e.DOWN_CNT " + \
            "WHEN NOT MATCHED THEN " + \
                      "INSERT (c.SMART_ID, c.PRO_NAME, c.DOMAIN_URL, c.PATH_URL, c.CATEGORY, c.INSTALLS)  " + \
                                 "VALUES (e.SMART_ID, e.PROVIDER_NAME, '" + site_name + "', e.SITE, e.CATEGORY_NAME, e.DOWN_CNT)"
        db.cursur.execute(sql)

    def insert_provider_name(self, db, access_day):
        sql = "insert into tb_smart_provider_info " + \
            "select a.smart_id, a.provider_name, a.domain_url, a.site, a.CATEGORY_NAME, a.DOWN_CNT " + \
            "from tb_smart_day_playstore_app a " + \
            "where  a.access_day = '"+access_day+"' " + \
            "and a.STORE_TYPE = 'newApp' " + \
            "and ((a.smart_id, provider_name) not in (select smart_id, pro_name from tb_smart_provider_info))"
        db.cursor.execute(sql)
        db.db.commit()