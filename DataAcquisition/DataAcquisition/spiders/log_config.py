# -*- coding: utf-8 -*-

import sys
from scrapy.utils.log import configure_logging
from FxtDataAcquisition.utils import logs

configure_logging(install_root_handler=False)
args = sys.argv
logfile = 'scrapy.log'
for arg in args:
    if arg.__contains__('logfile'):
        logfile = arg.split('=')[1]
        break
logs.logger(logfile)
