#!/usr/bin/env python
# -*- coding: utf-8 -*-

user_name = '你的账号'
password = '你的密码'
login_url = ('https://passport.baidu.com/v2/?login&tpl=mn&u='
             'http%3A%2F%2Fwww.baidu.com%2F')
one_week_trend_url = ('http://index.baidu.com/?tpl=trend&type=0'
                      '&area=0&time=12&word={word}')
time_range_trend_url = ('http://index.baidu.com/?tpl=trend&type=0&area=0'
                        '&time={start_date}|{end_date}&word={word}')

all_index_url = ('http://index.baidu.com/Interface/Search/getAllIndex/'
                 '?res={res}&res2={res2}&startdate={start_date}'
                 '&enddate={end_date}')
index_show_url = ('http://index.baidu.com/Interface/IndexShow/show/?res='
                  '{res}&res2={res2}&classType=1&res3[]={enc_index}'
                  '&className=view-value&{t}'
                  )
user_center_url = 'http://i.baidu.com/'
login_sign = 'http://passport.baidu.com/?logout'
# extension = 'txt'
# out_file_path = './data/out'