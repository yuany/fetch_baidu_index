#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

from baidu_index.browser import BaiduBrowser
from baidu_index.utils.log import logger


logger.info(u'请确保你填写的账号密码能够成功登陆百度')

# s = BaiduBrowser(cookie_json='{"name": "1"}')
# cookie_json = s.cookie_json
# s.close()

s = BaiduBrowser()
with open('result.txt', 'ab') as f:
    for keyword in [u'python']:
        try_num = 0
        try_max_num = 10
        while try_num < try_max_num:
            try:
                try_num += 1
                baidu_index_dict = s.get_baidu_index(keyword)
                for date, value in baidu_index_dict.iteritems():
                    logger.info(
                        'keyword:%s date:%s, value:%s' % (keyword, date, value)
                    )
                    f.write('keyword:%s date:%s, value:%s' % (keyword, date, value))
                    f.write('\r\n')
                break
            except:
                logger.error(traceback.format_exc())
                logger.info('retry start')
