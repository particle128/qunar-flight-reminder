#!/usr/bin/env python
# coding=utf-8

QUNAR_URL = 'http://flight.qunar.com/site/oneway_list.htm'

# demand lists
# Don't make the time span too large, such as 2014-01-10 ~ 2014-02-10. This may lead to the verification code page 
DEMANDS = [
	{'src':'大连',
	'dst':'济南',
	'start_date':'2014-01-08',
	'end_date':'2014-01-10',
	'price':250},

	{'src':'大连',
	'dst':'济宁',
	'start_date':'2014-01-08',
	'end_date':'2014-01-10',
	'price':350},
]

# Don't use a small interval such as 60*5(5mins), because if you frequently check the website, verification code page will appear.
INTERVAL_BETWEEN_TWO_CHECKS_IN_SEC = 60*15  # 15min
INTERVAL_BETWEEN_TWO_DAYS_IN_SEC = 30
TIME_FOR_PAGE_LOAD_IN_SEC = 10

# mail sender
FROM_ADDR = 'username@126.com'
# sender user
MAIL_USER = 'username'
# sender passwd
MAIL_PWD = 'passwd'
# sender smtp host
MAIL_HOST = 'smtp.126.com'
# mail receiver
TO_ADDR = 'phonenumber@wo.com.cn' # China unicom
# TO_ADDR = 'phonenumber@139.com' # China mobile
# TO_ADDR = 'phonenumber@189.com' # China telecom
