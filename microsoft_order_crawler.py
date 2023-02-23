# -*- coding:utf-8 -*-
# author: Tony Chang
# Class: MicrosoftOrderCrawler
# Description: bala...

import requests
import json
import time
import os


class MicrosoftOrderCrawler:
    orders_list: list[dict] = []
    new_orders_list: list[dict] = []
    continue_flag: bool = True
    str_continuation_token: str = "FirstPage"
    date_today: str = time.strftime("%Y-%m-%d", time.localtime())
    # stupid_currency_codes = [
    #     "EUR", "HUF", "ARS", "RUB", "TRY", "CLP", "NOK"
    # ]

    def __init__(self):
        self.session = requests.session()
        request_header = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/15.3 Safari/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'Correlation-Context': 'v=1,ms.b.tel.market=en-US',
            'Accept-Language': 'en-US;q=1'
        }
        self.session.headers.update(request_header)
        path_root = os.path.join("json_files", self.date_today)
        file_paths = self.searchFiles(path_root=path_root, search_key="OrdersList")
        if file_paths.__len__():
            file_path = file_paths[0]
            file = open(file=file_path, mode='r', encoding='utf-8')
            self.orders_list = json.load(fp=file)
            file.close()
        file_paths = self.searchFiles(path_root=path_root, search_key="New_Orders_List")
        if file_paths.__len__():
            file_path = file_paths[0]
            file = open(file=file_path, mode='r', encoding='utf-8')
            self.new_orders_list = json.load(fp=file)
            file.close()

    @staticmethod
    def dumpToFile(data_to_dump, file_name: str):
        date_today = time.strftime("%Y-%m-%d", time.localtime())
        time_now = time.strftime("%H-%M-%S", time.localtime())
        dump_path = os.path.join("json_files", date_today)
        if not os.path.exists(dump_path):
            os.makedirs(name=dump_path, exist_ok=True)
        new_file_name = file_name + "_" + time_now + ".json"
        dump_file_path = os.path.join("json_files", date_today, new_file_name)
        dump_file = open(file=dump_file_path, mode='w', encoding='utf-8')
        json.dump(obj=data_to_dump, fp=dump_file)
        dump_file.close()
        return 0

    @staticmethod
    def searchFiles(path_root: str, search_key: str):
        file_paths = []
        if os.path.exists(path=path_root):
            for root, lists, files in os.walk(top=path_root):
                for file in files:
                    if search_key in file:
                        file_path = os.path.join(root, file)
                        file_paths.append(file_path)
        return file_paths

    @staticmethod
    def print(something):
        print(type(something), something)

    def updateSession(self, str_request_verification_token: str, str_amcsecauth: str):
        str_cookie = "AMCSecAuth=" + str_amcsecauth + ";market=US"
        request_header = {
            '__RequestVerificationToken': str_request_verification_token,
            'Cookie': str_cookie
        }
        self.session.headers.update(request_header)
        # print(self.session.headers)
        return 0

    def getJSONData(self):
        path_root = os.path.join("json_files", self.date_today)
        file_paths = self.searchFiles(path_root=path_root, search_key=self.str_continuation_token)
        if file_paths.__len__():
            file_path = file_paths[0]
            file = open(file=file_path, mode='r', encoding='utf-8')
            json_data = json.load(fp=file)
            file.close()
        else:
            request_url = "https://account.microsoft.com/billing/orders/list?period=AllTime&orderTypeFilter=All" \
                          "&filterChangeCount=1&isInD365Orders=true&isPiDetailsRequired=true&timeZoneOffsetMinutes=-480"
            if self.continue_flag \
                    and not self.str_continuation_token == "FirstPage":
                request_url = request_url + "&continuationToken=" + self.str_continuation_token
            response = self.session.get(url=request_url)
            json_data = response.json()
            self.dumpToFile(data_to_dump=json_data, file_name=self.str_continuation_token)
        # print(type(json_data), json_data)
        return json_data

    def aLoopGettingJSONData(self):
        json_data = self.getJSONData()
        if json_data.__contains__('continuationToken'):
            self.continue_flag = True
            self.str_continuation_token = json_data['continuationToken']
        else:
            self.continue_flag = False
        for order_dict in json_data['orders']:
            # self.print(order_dict)
            self.orders_list.append(order_dict)
        return 0

    def getOrders(self, str_request_verification_token: str, str_amcsecauth: str):
        if not self.orders_list.__len__():
            self.updateSession(str_request_verification_token=str_request_verification_token, str_amcsecauth=str_amcsecauth)
            while self.continue_flag:
                self.aLoopGettingJSONData()
            self.dumpToFile(data_to_dump=self.orders_list, file_name="OrdersList")
        return self.orders_list

    def generateNewOrdersList(self):
        if not self.new_orders_list.__len__():
            for order_dict in self.orders_list:
                order_items_array = order_dict['items']
                for item_dict in order_items_array:
                    new_order_dict = {
                        'localTitle': item_dict['localTitle'],
                        'orderId': order_dict['orderId'],
                        'vanityOrderId': order_dict['vanityOrderId'],
                        'currencyCode': order_dict['currencyInfo']['currencyCode'],
                        'localTotalInDecimal': order_dict['localTotalInDecimal'],
                        'market': order_dict['market'],
                        'isEUMarket': order_dict['isEUMarket'],
                        'itemTypeName': item_dict['itemTypeName'],
                        'productId': item_dict['productId'],
                        'totalListPrice': item_dict['totalListPrice'],
                        'itemState': item_dict['itemState'],
                        'daysFromPurchase': order_dict['daysFromPurchase'],
                        'localSubmittedDate': order_dict['localSubmittedDate'],
                        'hasMultipleItems': order_dict['hasMultipleItems']
                    }
                    # # Deal with stupid price format with stupid currency codes
                    # if new_order_dict['currencyCode'] in self.stupid_currency_codes:
                    #     # print(new_order_dict['currencyCode'], new_order_dict['totalListPrice'])
                    #     new_order_dict['totalListPrice'] = new_order_dict['totalListPrice'].replace(',', '_').replace('.', ',').replace('_', '.')
                    #     # print(new_order_dict['totalListPrice'])
                    # Token Code (tokenCode) and Payment Instrument (paymentInstrument)
                    if item_dict.__contains__('tokenDetails') \
                        and item_dict['tokenDetails'].__len__() \
                        and item_dict['tokenDetails'][0].__contains__('tokenCode'):
                        new_order_dict.update({'tokenCode': item_dict['tokenDetails'][0]['tokenCode']})
                    elif order_dict.__contains__('paymentInstruments') \
                        and order_dict['paymentInstruments'].__len__() \
                        and order_dict['paymentInstruments'][0].__contains__('id'):
                        new_order_dict.update({'tokenCode': order_dict['paymentInstruments'][0]['id']})
                    else:
                        new_order_dict.update({'tokenCode': "Unknown"})
                    if item_dict.__contains__('tokenDetails') \
                        and item_dict['tokenDetails'].__len__() \
                        and item_dict['tokenDetails'][0].__contains__('state'):
                        new_order_dict.update({'paymentInstrument': item_dict['tokenDetails'][0]['state']})
                    elif order_dict.__contains__('paymentInstruments') \
                        and order_dict['paymentInstruments'].__len__() \
                        and order_dict['paymentInstruments'][0].__contains__('localNameAndTotalCharged'):
                        new_order_dict.update(
                        {'paymentInstrument': order_dict['paymentInstruments'][0]['localNameAndTotalCharged']})
                    else:
                        new_order_dict.update({'paymentInstrument': "Unknown"})
                    new_order_dict.update({'datetime': time.strftime("%Y-%m-%d %H:%M:%S")})
                    # print(new_order_dict)
                    self.new_orders_list.append(new_order_dict)
            self.dumpToFile(data_to_dump=self.new_orders_list, file_name="New_Orders_List")
        return self.new_orders_list

    def generateCSVFile(self):
        if self.new_orders_list.__len__():
            csv_file_path_root = os.path.join("csv_files", self.date_today)
            if not os.path.exists(csv_file_path_root):
                os.makedirs(name=csv_file_path_root, exist_ok=True)
            csv_file_name = "csv_file_" + time.strftime("%H-%M-%S") + ".csv"
            csv_file_path = os.path.join(csv_file_path_root, csv_file_name)
            csv_file = open(file=csv_file_path, mode='w', encoding='utf-8')
            # csv_file.writelines("localTitle,orderId,vanityOrderId,currencyCode,localTotalInDecimal,"
            #                     + "market,isEUMarket,itemTypeName,productId,totalListPrice,itemState,"
            #                     + "daysFromPurchase,localSubmittedDate,hasMultipleItems,tokenCode,"
            #                     + "paymentInstrument,datetime\n")
            csv_file.writelines("localTitle\torderId\tvanityOrderId\tcurrencyCode\tlocalTotalInDecimal\t"
                                + "market\tisEUMarket\titemTypeName\tproductId\ttotalListPrice\titemState\t"
                                + "daysFromPurchase\tlocalSubmittedDate\thasMultipleItems\ttokenCode\t"
                                + "paymentInstrument\tdatetime\n")
            for order_dict in self.new_orders_list:
                values = [
                    str(order_dict['localTitle']), str(order_dict['orderId']), str(order_dict['vanityOrderId']),
                    str(order_dict['currencyCode']), str(order_dict['localTotalInDecimal']), str(order_dict['market']),
                    str(order_dict['isEUMarket']), str(order_dict['itemTypeName']), str(order_dict['productId']),
                    str(order_dict['totalListPrice']), str(order_dict['itemState']), str(order_dict['daysFromPurchase']),
                    str(order_dict['localSubmittedDate']), str(order_dict['hasMultipleItems']), str(order_dict['tokenCode']),
                    str(order_dict['paymentInstrument']), str(order_dict['datetime'])
                ]
                line_to_write = "\t".join(values) + '\n'
                csv_file.writelines(line_to_write)
            csv_file.close()
        else:
            print("self.new_orders_list is empty!")
            return 255
        return 0
