# -*- coding: utf-8 -*-
import logging.handlers
from datetime import date, timedelta, datetime
# app 세부 정보 파싱
class Log:

    def __init__(self):
        dt = datetime.now()
        access_day = dt.strftime('%Y%m%d')
        # logger 생성
        logger = logging.getLogger(__name__)
        # log의 포맷 설정
        #formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s] >> %(message)s')
        # handler 생성
        streamHandler = logging.StreamHandler()
        fileHandler = logging.FileHandler('./logs/ParseApp_' + access_day + '.log')

        streamHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)

        # logger instance에 formatter 생성
        logger.addHandler(streamHandler)
        logger.addHandler(fileHandler)
        logger.setLevel(level=logging.DEBUG)
        self.logger = logger

    def LogFunction_ranking(self, rank_no, package_name, app_name):
        log_message_list = rank_no, package_name, app_name
        try:
            log_message = ", ".join(log_message_list)
            self.logger.debug(log_message)
        except:
            try:
                log_message = ", ".join(str(v) for v in log_message_list)
                self.logger.debug(log_message)
            except:
                log_message = ','.join([None])
                self.logger.debug(log_message)

    def LogFunction_day_store_APP(self, app_name, package_name, category_name, provider_info, down_cnt, review_cnt, review_score_info, review_num1, review_num2, review_num3, review_num4, review_num5, update_name, site, developer_info, dev_info):
        log_message_list = app_name, package_name, category_name, provider_info, str(down_cnt), str(
            review_cnt), review_score_info, str(review_num1), str(review_num2), str(review_num3), str(
            review_num4), str(review_num5), update_name, site, developer_info, dev_info

        try:
            log_message = ", ".join(log_message_list)
            self.logger.debug(log_message)
        except:
            try:
                log_message = ", ".join(str(v) for v in log_message_list)
                self.logger.debug(log_message)
            except:
                log_message = ','.join([None])
                self.logger.debug(log_message)

    def LogFunction_parse_provider(self, app_name, smart_id, package_name, category_name, provider_info, down_cnt, review_cnt, review_score_info, review_num1, review_num2, review_num3, review_num4, review_num5, update_name, site, developer_info, dev_info):
        log_message_list = app_name, smart_id, package_name, category_name, provider_info, str(down_cnt), str(
            review_cnt), review_score_info, str(review_num1), str(review_num2), str(review_num3), str(
            review_num4), str(review_num5), update_name, site, developer_info, dev_info
        try:
            log_message = ", ".join(log_message_list)
            self.logger.debug(log_message)
        except:
            try:
                log_message = ", ".join(str(v) for v in log_message_list)
                self.logger.debug(log_message)
            except:
                log_message = ','.join([None])
                self.logger.debug(log_message)

    def LogFunction_smart_id(self, smart_id, package_name):
        log_message_list = "Already App! update >> smart_id : ", smart_id,  "package_name : ", package_name
        try:
            log_message = ", ".join(log_message_list)
            self.logger.debug(log_message)
        except:
            try:
                log_message = ", ".join(str(v) for v in log_message_list)
                self.logger.debug(log_message)
            except:
                log_message = ','.join([None])
                self.logger.debug(log_message)

    def LogFunction_provider_id(self, pproid, smart_id):
        log_message_list = "1. update >> pro_id : ", pproid, " smart_id : ", smart_id
        try:
            log_message = ", ".join(log_message_list)
            self.logger.debug(log_message)
        except:
            try:
                log_message = ", ".join(str(v) for v in log_message_list)
                self.logger.debug(log_message)
            except:
                log_message = ','.join([None])
                self.logger.debug(log_message)

    def LogFunction_site_id(self, site_id, smart_id):
        log_message_list = "2. Update >> site_id : ", site_id, " smart_id : ", smart_id
        try:
            log_message = ", ".join(log_message_list)
            self.logger.debug(log_message)
        except:
            try:
                log_message = ", ".join(str(v) for v in log_message_list)
                self.logger.debug(log_message)
            except:
                log_message = ','.join([None])
                self.logger.debug(log_message)

    def LogFunction_Start(self):
        self.logger.debug(" \n Hello Parser! ")

    def LogFunction_End(self):
        self.logger.debug(" Goodbye Parser! \n")


    def Log_ranking_Start(self):
        self.logger.debug("*************** (1) ranking imfomation Start ***************")

    def Log_ranking_End(self):
        self.logger.debug("*************** (1) ranking imfomation End *************** \n")

    def Log_Daystoreapp_Start(self):
        self.logger.debug("*************** (2) Day store App parsing Start ***************")

    def Log_Daystoreapp_End(self):
        self.logger.debug("*************** (2) Day store App parsing End *************** \n")

    def Log_newProvider_Start(self):
        self.logger.debug("*************** (3) new provider Start ***************")

    def Log_newProvider_End(self):
        self.logger.debug("*************** (3) new provider End *************** \n")

    def Log_updateProvider_Start(self):
        self.logger.debug("*************** (4) update Provider Start ***************")

    def Log_updateProvider_End(self):
        self.logger.debug("*************** (4) update Provider End *************** \n")





