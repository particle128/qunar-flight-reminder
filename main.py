#!/usr/bin/env python
# coding=utf-8

import time
import datetime
import re

import selenium
from selenium import webdriver 

from reminder import *
from config import *
# config_local.py will override the previous config.py
try: 
    from config_local import *
except:
    pass

class FlightChecker():
    def __init__(self):
        self.driver = webdriver.Chrome()


    def parse_date(self, date_str):
        date_elements = date_str.split('-')
        year = int(date_elements[0])
        month = int(date_elements[1])
        day = int(date_elements[2])
        return datetime.date(year, month, day)


    def get_position(self, number_block):
        "relative position of the price number"
        pos_pattern = re.compile('left: -(\d){2}px')
        target = str(number_block.get_attribute('style'))
        return int(pos_pattern.search(target).group(1))


    def check_demand_without_except(self, cur_date_str):
        # skip '邻近推荐' and choose the first element (lowest cost)
        price_block = self.driver.find_element_by_id('hdivResultPanel').find_element_by_class_name('prc')

        number_blocks = price_block.find_elements_by_tag_name('b')
        number_list = list(number_blocks[0].text)
        len = self.get_position(number_blocks[0])

        for number_block in number_blocks[1:]:
            pos = self.get_position(number_block)
            number_list[len-pos] = number_block.text

        price = ''.join(number_list)
        print u'￥' + price
        if int(price) <= self.price:
            info = "%s: %s to %s 's price is %s\r\n" % (cur_date_str, self.src, self.dst, price)
            send_email(info)


    def check_demand(self, cur_date_str):
        current_url = "%s?searchDepartureAirport=%s&searchArrivalAirport=%s&searchDepartureTime=%s" % (QUNAR_URL, self.src, self.dst, cur_date_str)
        self.driver.get(current_url)
        time.sleep(TIME_FOR_PAGE_LOAD_IN_SEC)
        if self.driver.page_source.find(u'该航线当前无可售航班') != -1:
            print 'no flight under ' + cur_date_str + ":" + self.src + " to " + self.dst
            return
        try:
            self.check_demand_without_except(cur_date_str)
        except Exception as e:
            print e


    def load_current_option(self, demand):
        self.start_date = self.parse_date(demand['start_date'])
        self.end_date = self.parse_date(demand['end_date'])
        self.src = demand['src']
        self.dst = demand['dst']
        self.price = demand['price']
        print self.src + ' to ' + self.dst


    def check(self):
        one_day = datetime.timedelta(days=1) # 1 day
        for demand in DEMANDS:
            self.load_current_option(demand)

            cur_date = self.start_date
            while cur_date <= self.end_date:
                self.check_demand(cur_date.isoformat())
                cur_date += one_day
                time.sleep(INTERVAL_BETWEEN_TWO_DAYS_IN_SEC)
 
                                    

if __name__ == '__main__':
    flightChecker = FlightChecker()
    print 'here we go'
    while True:
        print 'begin checking...'
        flightChecker.check()
        print 'end checking...'
        time.sleep(INTERVAL_BETWEEN_TWO_CHECKS_IN_SEC)
