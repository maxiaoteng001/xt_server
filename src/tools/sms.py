import logging
from src.utils import textmyself
from src.tools import tools_bp

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

@tools_bp.route('/sms/help', methods=['GET'])
def sms_help():
    # return render_template('help.html')
    return '用来发送短信到自己的手机!'


@tools_bp.route('/sms/send_message', methods=['POST'])
@tools_bp.route('/sms/send_message/<message>', methods=['GET'])
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
