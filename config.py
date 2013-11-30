#!/usr/bin/env python
# coding=utf-8

URL='http://flight.qunar.com/site/oneway_list.htm'

# demand lists
DEMANDS= [
	{'src':'大连',
	'dst':'济南',
	'date_start':'2014-01-08',
	'date_end':'2014-01-10',
	'price':250},

	{'src':'大连',
	'dst':'济宁',
	'date_start':'2014-01-08',
	'date_end':'2014-01-10',
	'price':350},
]

# time interval in seconds between two checkings
# Don't use a small interval such as 60*5(5mins),because if you frequently check the website, verification code page may appear.
INTERVAL=60*20

# mail sender
FROM_ADDR='[username]@126.com'
# sender user
MAIL_USER='[username]'
# sender passwd
MAIL_PWD='[passwd]'
# sender smtp host
MAIL_HOST='smtp.126.com'
# mail receiver
TO_ADDR='[phonenumber]@wo.com.cn' # China unicom
# TO_ADDR='[phonenumber]@139.com' # China mobile
# TO_ADDR='[phonenumber]@189.com' # China telecom
