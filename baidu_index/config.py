#!/usr/bin/env python
# -*- coding: utf-8 -*-

user_name = 'your_account'
password = 'your_password'
login_url = ('https://passport.baidu.com/v2/?login&tpl=mn&u='
             'http%3A%2F%2Fwww.baidu.com%2F')
one_week_trend_url = ('http://index.baidu.com/?tpl=trend&type=0'
                      '&area=0&time=12&word={word}')
all_index_url = ('http://index.baidu.com/Interface/Search/getAllIndex/'
                 '?res={res}&res2={res2}&startdate={start_date}'
                 '&enddate={end_date}')
index_show_url = ('http://index.baidu.com/Interface/IndexShow/show/?res='
                  '{res}&res2={res2}&classType=1&res3[]={enc_index}'
                  '&className=view-value&{t}'
                  )
