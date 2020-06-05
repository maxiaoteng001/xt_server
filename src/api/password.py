import string
import random
import logging
from flask_restful import Resource


class PasswordItem(Resource):
    def get(self, length=20):
        str = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length)])
        logging.info('生成随机密码:{}'.format(str))

        return {'random_string': str}