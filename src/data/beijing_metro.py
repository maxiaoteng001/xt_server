import string
import random
import logging
import json
from flask import jsonify
from flask import request
from flask import render_template
from src.data import data_bp
from src.utils import *
from src.utils.mysql_utils import MysqlHelper


@data_bp.route('/beijing_metro', methods=['GET'])
def beijing_metro():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '2999')
    client = MysqlHelper(dbconfig)
    sql = '''
    select * from spider.weibo_info where data_date>'{}' and data_date<'{}' order by data_date
    '''.format(start_date, end_date)
    data = client.query(sql)
    passenger_flow = [float(d.get('passenger_flow', '0'))/10000 for d in data]
    date = [d.get('data_date') for d in data]
    all_year = client.query('select distinct left(data_date, 4) as year from spider.weibo_info')
    all_year_data = [y.get('year') for y in all_year] 
    all_month = client.query('select distinct right(left(data_date, 7), 2) as month from spider.weibo_info')
    all_month_data = [m.get('month') for m in all_month]
    return render_template('beijing_metro.html', passenger_flow=passenger_flow, date=date, all_year_data=all_year_data, all_month_data=all_month_data)


@data_bp.route('/setData/') #路由
def setData():
    client = MysqlHelper(dbconfig)
    sql = '''
    select * from spider.weibo_info
    '''
    data = client.query(sql)
    return jsonify(data) #将数据以字典的形式传回
