from flask import Blueprint

tools_bp = Blueprint('tools', __name__, url_prefix='/tools')

from . import sms
from . import password

@tools_bp.route('/help', methods=['GET'])
def help():
    # return render_template('help.html')
    return '随机密码和短信报警等小工具!'