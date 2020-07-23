from flask import Blueprint

data_bp = Blueprint('data', __name__, url_prefix='/data')

from . import beijing_metro

@data_bp.route('/help', methods=['GET'])
def help():
    # return render_template('help.html')
    return '用于展示数据可视化demo'