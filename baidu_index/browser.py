#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib
import json
from datetime import datetime, timedelta

from selenium import webdriver

import config
from .api import Api


class BaiduBrowser(object):
    def __init__(self, cookie_json='', check_login=True):
        self.browser = webdriver.Firefox()
        self.browser.set_page_load_timeout(50)
        self.browser.set_script_timeout(10)
        self.user_name = config.user_name
        self.password = config.password
        self.cookie_json = cookie_json
        self.api = None
        self.cookie_dict_list = []

        self.init_api(check_login=check_login)

    def is_login(self):
        self.login_with_cookie(self.cookie_json)
        self.browser.get(config.user_center_url)
        html = self.browser.page_source
        print html
        return config.login_sign in html

    def init_api(self, check_login=True):
        need_login = False
        if not self.cookie_json:
            need_login = True
        elif check_login and not self.is_login():
            need_login = True
        if need_login:
            self.login(self.user_name, self.password)
            self.cookie_json = self.get_cookie_json()
        cookie_str = self.get_cookie_str(self.cookie_json)
        self.api = Api(cookie_str)

    def get_date_info(self, start_date, end_date):
        if start_date.find('-') != -1 and end_date.find('-') != -1:
            start_date = start_date.replace('-', '')
            end_date = end_date.replace('-', '')
        start_date = datetime.strptime(start_date, '%Y%m%d')
        end_date = datetime.strptime(end_date, '%Y%m%d')

        date_list = []
        temp_date = start_date
        while temp_date <= end_date:
            date_list.append(temp_date.strftime("%Y-%m-%d"))
            temp_date += timedelta(days=1)
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
        return start_date, end_date, date_list

    def get_baidu_index_by_date_range(self, keyword, start_date, end_date):
        print 'start_date:%s, end_date:%s' % (start_date, end_date)
        url = config.time_range_trend_url.format(
            start_date=start_date, end_date=end_date,
            word=urllib.quote(keyword.encode('gbk'))
        )
        self.browser.get(url)
        res = self.browser.execute_script('return PPval.ppt;')
        res2 = self.browser.execute_script('return PPval.res2;')
        start_date, end_date, date_list = self.get_date_info(
            start_date, end_date
        )

        # 尝试一下数据抓取
        url = config.all_index_url.format(
            res=res, res2=res2, start_date=start_date, end_date=end_date
        )
        print url
        all_index_info = self.api.get_all_index_html(url)
        enc_s = all_index_info['data']['all'][0]['userIndexes_enc'].split(',')

        baidu_index_dict = dict()
        for index, _ in enumerate(enc_s):
            url = config.index_show_url.format(
                res=res, res2=res2, enc_index=_, t=int(time.time()) * 1000
            )
            try_num = 0
            try_max_num = 5
            while try_num < try_max_num:
                try:
                    try_num += 1
                    img_url, val_info = self.api.get_index_show_html(url)
                    value = self.api.get_value_from_url(img_url, val_info)
                    break
                except:
                    pass
            baidu_index_dict[date_list[index]] = value.replace(',', '')
            print keyword, date_list[index], value.replace(',', '')
        return baidu_index_dict

    def _get_index_period(self, keyword):
        url = config.one_week_trend_url.format(
            word=urllib.quote(keyword.encode('gbk'))
        )
        self.browser.get(url)
        res = self.browser.execute_script('return PPval.ppt;')
        res2 = self.browser.execute_script('return PPval.res2;')
        start_date, end_date = self.browser.execute_script(
            'return BID.getParams.time()[0];'
        ).split('|')
        start_date, end_date, date_list = self.get_date_info(
            start_date, end_date
        )
        url = config.all_index_url.format(
            res=res, res2=res2, start_date=start_date, end_date=end_date
        )
        all_index_info = self.api.get_all_index_html(url)
        start_date, end_date = all_index_info['data']['all'][0]['period'].split('|')
        # 重置start_date, end_date，以api返回的为准
        start_date, end_date, date_list = self.get_date_info(
            start_date, end_date
        )
        print 'all_start_date:%s, all_end_date:%s' % (start_date, end_date)
        return date_list

    def get_baidu_index(self, keyword):
        date_list = self._get_index_period(keyword)

        baidu_index_dict = dict()
        start = 0
        skip = 90
        end = len(date_list)
        while start < end:
            try:
                start_date = date_list[start]
                end_date = date_list[start + skip]
                result = self.get_baidu_index_by_date_range(
                    keyword, start_date, end_date
                )
                baidu_index_dict.update(result)
                start += skip + 1
            except:
                import traceback
                print traceback.format_exc()
        return baidu_index_dict

    def login(self, user_name, password):
        login_url = config.login_url
        self.browser.get(login_url)
        user_name_obj = self.browser.find_element_by_id(
            'TANGRAM__PSP_3__userName'
        )
        user_name_obj.send_keys(user_name)
        ps_obj = self.browser.find_element_by_id('TANGRAM__PSP_3__password')
        ps_obj.send_keys(password)
        sub_obj = self.browser.find_element_by_id('TANGRAM__PSP_3__submit')
        sub_obj.click()
        while self.browser.current_url == login_url:
            time.sleep(1)

    def close(self):
        self.browser.quit()

    def get_cookie_json(self):
        return json.dumps(self.browser.get_cookies())

    def get_cookie_str(self, cookie_json=''):
        if cookie_json:
            cookies = json.loads(cookie_json)
        else:
            cookies = self.browser.get_cookies()
        return '; '.join(['%s=%s' % (item['name'], item['value'])
                          for item in cookies])

    def login_with_cookie(self, cookie_json):
        self.browser.get('https://www.baidu.com/')
        for item in json.loads(cookie_json):
            try:
                self.browser.add_cookie(item)
            except:
                continue
