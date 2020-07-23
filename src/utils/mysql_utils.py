import datetime
import os
import pymysql
import logging
import traceback
import uuid

"""
1. 要保证有数据库
2. 可以自动创建不存在的表

"""


class MysqlHelper(object):

    # 初始化
    def __init__(self, dbconfig):
        self.host = dbconfig.get('host')
        self.port = dbconfig.get('port')
        self.user = dbconfig.get('user')
        self.password = dbconfig.get('password')
        self.database = dbconfig.get('database')
        self.charset = dbconfig.get('charset', 'utf8mb4')
        self._conn = None
        self._connect()
        self._cursor = self._conn.cursor(cursor=pymysql.cursors.DictCursor)

        self.db_info = {
            '106.75.26.184': '10.10.46.167'
        }
        # 根据uuid识别是否用内网连接
        self.uuid_this_machine = uuid.getnode()
        if self.uuid_this_machine in [90520747197197, 90520730968297, 79454117535344, 90520735714953, 90520737028857]:
            # ucloud 服务器, 如果没配置过db_info, 默认使用原来地址
            host = self.db_info.get(self.host)
            if host is None:
                pass
            else:
                self.host=host
        else:
            # 若环境为其他环境，则使用外网地址
            pass

    @property
    def logger(self):
        return logging.getLogger()

    # 链接数据库
    def _connect(self):
        try:
            self._conn = pymysql.connect(host=self.host, port=self.port,
                                         user=self.user, password=self.password,
                                         database=self.database, charset=self.charset
                                         )
        except pymysql.Error as e:
            self.logger.error(e)

    # 执行查询
    def query(self, sql):
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchall()
            self._conn.commit()
        except pymysql.Error as e:
            result = None
            self.logger.error(e)
        return result

    # 选择
    def select(self, table, column='*', condition=''):
        try:
            if condition != '':
                condition = 'where {}'.format(condition)
            sql = 'select {} from {} {}'.format(column, table, condition)
            self.logger.debug(sql)
            self._cursor.execute(sql)
            return self._cursor.fetchall()
        except Exception as e:
            self.logger.exception("{}, {}".format(e, traceback.format_exc()))

    # 插入
    def insert(self, table, data):
        placeholders = ', '.join(['%s']* len(data))  ##按照dict长度返回如：%s, %s 的占位符
        columns = ', '.join(data.keys())    ##按照dict返回列名，如：age, name
        param =  tuple(data.values())
        try:
            insert_sql =  "INSERT IGNORE INTO {} ({}) VALUES ( {} )".format(table, columns, placeholders) #INSERT INTO mytable ( age, name ) VALUES ( %s, %s )
            self._cursor.execute(insert_sql, param)
            self._conn.commit()
        except Exception as e:
            self.logger.exception("{}, {}, {}".format(data, e, traceback.format_exc()))
            self.rollback()	

    # 批量插入
    def insert_many(self, table, datas):
        if datas == []:
            return
        placeholders = ', '.join(['%s']* len(datas[0]))  ##按照dict长度返回如：%s, %s 的占位符
        columns = ', '.join(datas[0].keys())    ##按照dict返回列名，如：age, name
        param=[]
        for data in datas:
            param.append(tuple(data.values()))
        try:
            insert_sql =  "INSERT IGNORE INTO {} ({}) VALUES ( {} )".format(table, columns, placeholders) #INSERT INTO mytable ( age, name ) VALUES ( %s, %s )
            # 批量插入
            self._cursor.executemany(insert_sql, param)
            self._conn.commit()
        except Exception as e:
            self.logger.exception("{}, {}, {}".format(datas[0], e, traceback.format_exc()))
            self.rollback()	


    # 修改
    def update(self, table, data, condition=''):
        if condition == '':
            self.logger.debug('更改时错误, 没有提供condition')
        else:
            condition = 'where {}'.format(condition)
        value = ''
        for k, v in data.items():
            value += ',{}="{}"'.format(k, v)
        value = value[1:]
        sql = 'update {} set {} {}'.format(table, value, condition)
        self.logger.debug(sql)
        self._cursor.execute(sql)
        self._conn.commit()
        return self._cursor.rowcount  # 返回更新的行数

    # 删除
    def delete(self, table, condition=''):
        if condition != '':
            condition = 'where {}'.format(condition)
        sql = 'delete from {} {}'.format(table, condition)
        self._cursor.execute(sql)
        self._conn.commit()
        return self._cursor.rowcount

    # rollback 回滚
    def rollback(self):
        self._conn.rollback()

    def __del__(self):
        try:
            self._cursor.close()
            self._conn.close()
        except pymysql.Error as e:
            self.logger.error(e)

    def close(self):
        self.__del__()


def test():
    dbconfig = {
        'host': 'localhost',
        "port": 3306,
        'user': 'root',
        'password': 'root',
        'database': 'cetc32',
        'charset': 'utf-8',
    }

    db = Mysql(dbconfig)
    # result = db.select('weapon01', '*', '')
    # # result type: tuple
    # # 返回的是一个tuple, 内部也是tuple
    # for row in result:
    #     print(row)
    #     # (1, 'AS34/鸬鹚', 'missile', '导弹武器', '舰舰导弹', 'http://weapon.huanqiu.com/as34', '1532437411')
    #     print(type(row))
    #     # <class 'tuple'>
    #     print(row[0])
    #     # 1
    #     break


if __name__ == '__main__':
    test()
