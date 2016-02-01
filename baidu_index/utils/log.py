#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)
channel = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(channel)
