import functools
import logging
from src.utils import textmyself

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

sms = Blueprint('sms', __name__, url_prefix='/sms')

@sms.route('/help', methods=['GET'])
def help():
    # return render_template('help.html')
    return '用来发送短信到自己的手机!'


@sms.route('/send_message', methods=['POST'])
@sms.route('/send_message/<message>', methods=['GET'])
def send_message(message=None):
    if request.method == 'POST':
        message = request.get_json().get('message')
    logging.info('发送短信: {}'.format(message))
    return_code = textmyself(message)
    return_code = 0
    if return_code == 0:
        return '短信发送成功,{}'.format(message)
    else:
        return '短信发送失败, 请确认'
