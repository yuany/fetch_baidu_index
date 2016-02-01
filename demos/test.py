#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

from baidu_index.browser import BaiduBrowser
from baidu_index.utils.log import logger


s = BaiduBrowser()

for keyword in [u'test', u'python']:
    try:
        baidu_index_dict = s.get_baidu_index(keyword)
        for date, value in baidu_index_dict.iteritems():
            logger.info(
                'keyword:%s date:%s, value:%s' % (keyword, date, value)
            )
    except:
        print traceback.format_exc()
