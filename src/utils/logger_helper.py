import json
import logging
import logging.handlers
import datetime
import os
import sys
from logging.config import dictConfig


def logger_config(enable_console_handler=False, 
                    enable_file_handler=True, 
                    log_name='app', 
                    log_level='INFO',
                    log_file_max_count=5,
                    by_day=True,
                    always=False):
    '''
    日志配置, 默认按天命名

    :param boolean by_day: 按天切分日志, 按天命名
    :param boolean always: 按天切分日志, always
    '''
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # 因为有多个进程，所以用时间戳做id, 延迟2s启动，日志名以分钟结尾
    if always:
        datetime_str = 'always'
    elif by_day:
        datetime_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    else:
        datetime_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H:%M:%S')

    log_path = os.path.join(log_dir, '{}_{}.log'.format(log_name, datetime_str))
    
    console_handler = {
        'class': 'logging.StreamHandler',
        'formatter': 'default',
        'level': log_level,
        # 'stream': 'ext://flask.logging.wsgi_errors_stream'
    }
    file_handler = {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'formatter': 'detail',
        'filename': log_path,
        'level': log_level,
        'when': 'midnight',
        'backupCount': log_file_max_count
    }
    default_formatter = {
        'format': "%(asctime)s %(name)-10s %(filename)-15s %(lineno)-3s %(levelname)-8s %(message)s"
    }
    detail_formatter = {
        'format': "%(asctime)s %(name)-10s %(filename)-15s %(lineno)-3s %(levelname)-8s %(message)s"
    }
    handlers = []
    if enable_console_handler:
        handlers.append('console')
    if enable_file_handler:
        handlers.append('file')
    d = {
        'version': 1,
        'formatters': {
            'default': default_formatter,
            'detail': detail_formatter
        },
        'handlers': {
            'console': console_handler,
            'file': file_handler
        },
        'root': {
            'level': log_level,
            'handlers': handlers
        }
    }
    dictConfig(d)

if __name__ == '__main__':
    logger_config()
    logger = logging.getLogger()
    logger.info('哈哈')