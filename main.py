# -*- coding:utf-8 -*-
# author: Tony Chang
# Python: main.py
# Description: bala...

import configparser
from microsoft_order_crawler import *


def crawler_method():
    config_file = "config.conf"
    conf = configparser.RawConfigParser()
    if os.path.isfile(config_file):
        conf.read(config_file)
    else:
        print("The file `%s` not exsist." % config_file)
        exit(255)
    str_request_verification_token = conf.get("config", "str_request_verification_token")
    str_amcsecauth = conf.get("config", "str_amcsecauth")

    # crawler = MicrosoftOrderCrawler()
    # crawler.setSession(str_request_verification_token=str_request_verification_token, str_amcsecauth=str_amcsecauth)
    # json_data = crawler.getJSONData()
    # crawler.print(json_data)
    # str_continuation_token = "M10L0R0D0"
    # json_data = crawler.getJSONData(continue_flag=True, str_continuation_token=str_continuation_token)
    # crawler.print(json_data)

    crawler = MicrosoftOrderCrawler()
    orders_list = crawler.getOrders(str_request_verification_token=str_request_verification_token, str_amcsecauth=str_amcsecauth)
    # print(type(orders_list), orders_list)
    new_orders_list = crawler.generateNewOrdersList()
    # print(type(new_orders_list), new_orders_list, new_orders_list.__len__())
    crawler.generateCSVFile()


if __name__ == '__main__':
    crawler_method()
