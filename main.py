#!/usr/bin/env python
# coding=utf-8

import selenium
from selenium import webdriver 
#from selenium.webdriver.common.proxy import *
import time
import datetime
import re
from urlparse import urlparse
import sys

from config_local import *
#from config import *
from reminder import *


def check(driver):
	"read the configuration file (config.py) once a time"
	infoText=''
	pos_pattern=re.compile('left: -(\d){2}px')
	for demand in DEMANDS:
		# read date info
		start=demand['date_start'].split('-')
		end=demand['date_end'].split('-')
		date_start=datetime.date(int(start[0]),int(start[1]),int(start[2]))
		date_end=datetime.date(int(end[0]),int(end[1]),int(end[2]))

		one_day=datetime.timedelta(days=1)# 1 day

		dd=date_start
		while dd<=date_end:
			params={'':demand['src'],
					'':demand['dst'],
					'searchDepartureTime':dd.isoformat()}
			driver.get("%s?searchDepartureAirport=%s&searchArrivalAirport=%s&searchDepartureTime=%s"%(URL,demand['src'],demand['dst'],dd.isoformat()))
			
			# in case that the page's ajax has not finished 
			no_result=False
			need_validation=False
			threshold=10
			time.sleep(10)
			while True:
				try:
					driver.find_element_by_class_name('prc').find_elements_by_tag_name('b')
				except Exception as e:
					if driver.page_source.find(u'该航线当前无可售航班')!=-1:
						no_result=True
						break
					threshold-=1
					if threshold==0:
						need_validation=True
						break
					print 'wait 10s '
					time.sleep(10)
				else:
					break

			# no result under that day
			if no_result:
				print 'no result under'+dd.isoformat()+":"+demand['src']+" "+demand['dst']
				dd+=one_day
				continue
			# validation page appears because of too frequent requests
			if need_validation:
				print 'too frequent,need varification code'
				return

			first=True
			prc=[]
			len=0
			# only check the first price since the price is in an ascending sort order
			try:
				for block in driver.find_element_by_class_name('prc').find_elements_by_tag_name('b'):
					if first:
						prc=list(block.text)
						# whole length of the price
						len=int(pos_pattern.search(str(block.get_attribute('style'))).group(1))
						first=False
					else:
						# position of the number
						pos=int(pos_pattern.search(str(block.get_attribute('style'))).group(1))
						prc[len-pos]=block.text
				price=int(''.join(prc))
				if price<=demand['price']:
					infoText+="%s: %s to %s 's price is %d\r\n" %(dd.isoformat(),demand['src'],demand['dst'],price)
					# if important information arrives, send email immediately
					sendEmail(infoText)
					print infoText
					infoText=""
			# if some exception occurs,let it go
			except Exception as e:
				print e
					
			# the next day 
			dd+=one_day
			# wait 30s
			time.sleep(30)

if __name__=='__main__':

# attempt to use the http proxy, but fails.

#	myProxy = "217.169.209.2:6666"
#	proxy = Proxy({
#		'proxyType': ProxyType.MANUAL,
#		'httpProxy': myProxy,
#		'ftpProxy': myProxy,
#		'sslProxy': myProxy,
#		'noProxy': '' # set this value as desired
#		})
	#driver = webdriver.Firefox(proxy=proxy)

	driver=webdriver.Chrome()
	#sys.stdout=open('output','w')
	print 'here we go'
	while True:
		# every 0.5h
		print 'begin checking...'
		check(driver)
		print 'end checking...'
		sys.stdout.flush() # flush the output
		time.sleep(INTERVAL)
