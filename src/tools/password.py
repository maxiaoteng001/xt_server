import string
import random
import logging
import json
from flask import request
from src.tools import tools_bp


@tools_bp.route('/random_string', methods=['GET'])
def random_string():
    # 默认密码只包含字母和数字
    level = request.args.get('level', '4')
    if level == '5':
        str = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(20)])
    else:
        str = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
    logging.info('生成随机密码:{}'.format(str))
    return json.dumps({'random_string': str})
