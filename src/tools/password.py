import string
import random
import logging
import json
from src.tools import tools_bp


@tools_bp.route('/random_string', methods=['GET'])
def random_string():
    str = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(20)])
    logging.info('生成随机密码:{}'.format(str))
    return json.dumps({'random_string': str})
