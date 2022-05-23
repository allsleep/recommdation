# -*- coding: utf-8 -*-
from logging import getLogger, Formatter, StreamHandler, handlers, INFO, DEBUG, WARN
import time
import os

from data.gobledefine import LOG_DIR

"""
日志模块
传入mess写入日志文件(每天生成一个日志文件)
共warning,info,error三个等级
"""
# Service、EDST、SRT
# NAMEHEADER = 'Service'
def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton

@singleton
class Log:
    def __init__(self):
        self.logger = getLogger()
        name = LOG_DIR + '\collect_movie_log' + time.strftime('_%Y-%m-%d', time.localtime(time.time())) + '.log'
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        self.logger.setLevel(INFO)
        formatter = Formatter(
            '%(asctime)s - [%(process)d-%(threadName)s]-%(filename)s[line:%(lineno)d]-[%(levelname)s]: %(message)s')
        if not self.logger.handlers:
            console_handler = StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(WARN)
            self.logger.addHandler(console_handler)
            file_handler = handlers.RotatingFileHandler(name, maxBytes=10*1024*1024, backupCount=5,
                                                                encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def get_logger(self):
        return self.logger

LOG = Log().get_logger()

if __name__ == '__main__':
    log = Log()
    log.info('test')



