#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib
from datetime import datetime, timedelta

from selenium import webdriver

import config
from .api import Api
from .utils.log import logger


class BaiduBrowser(object):
    def __init__(self):
        self.browser = webdriver.PhantomJS()
        self.browser.set_page_load_timeout(50)
        self.browser.set_script_timeout(10)
        self.user_name = config.user_name
        self.password = config.password
        self.cookie = ''
        self.api = None
        self.cookie_dict_list = []

        self.init_api()

    def init_api(self):
        if not self.cookie:
            self.login(self.user_name, self.password)
        self.api = Api(self.cookie)

    def get_date_info(self, start_date, end_date):
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

    def get_baidu_index(self, keyword):
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
        enc_s = all_index_info['data']['all'][0]['userIndexes_enc'].split(',')

        baidu_index_dict = dict()
        for index, _ in enumerate(enc_s):
            url = config.index_show_url.format(
                res=res, res2=res2, enc_index=_, t=int(time.time()) * 1000
            )
            img_url, val_info = self.api.get_index_show_html(url)
            value = self.api.get_value_from_url(img_url, val_info)
            baidu_index_dict[date_list[index]] = value.replace(',', '')
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
        logger.info(u'请确保能够成功登陆百度，输入你的账号和密码，有验证码要手动输入一下')
        while self.browser.current_url == login_url:
            time.sleep(1)
        self.cookie = self.get_current_cookie_str()

    def close(self):
        self.browser.quit()

    def get_current_cookie_str(self):
        self.cookie_dict_list = self.browser.get_cookies()
        cookies = self.browser.get_cookies()
        return '; '.join(['%s=%s' % (item['name'], item['value'])
                          for item in cookies])

    def login_with_cookie(self):
        self.browser.get('https://www.baidu.com/')
        cookie_dict_list = self.cookie_dict_list
        for cookie_dict in cookie_dict_list:
            try:
                self.browser.add_cookie(cookie_dict)
            except:
                continue
