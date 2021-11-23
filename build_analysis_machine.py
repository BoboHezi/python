#!/usr/bin/python3

import sys
import mysql.connector
import time
import datetime

import matplotlib
import matplotlib.pyplot as plt


def isempty(obj):
    return True if not (obj and len(obj)) else False


def query_data(table='devops_compile', keys='id, compile_build_time, compile_build_finish_time', condition=None, order=None):
    dev_ops_db = mysql.connector.connect(
        host='192.168.1.23',
        port=3306,
        user='root',
        passwd='root',
        database='jeecg-boot242'
    )
    cursor = dev_ops_db.cursor()
    sql = 'select %s from %s ;' % (keys, table)
    if not isempty(condition):
        sql = sql.replace(';', ' where %s;' % condition)
    if not isempty(order):
        sql = sql.replace(';', ' order by %s;' % order)
    # print('sql: %s' % sql)
    cursor.execute(sql)

    return cursor.fetchall()


def main(argv):
    HOST_IP = '192.168.1.23' if len(argv) < 1 else argv[0]

    # query host booted time
    # if HOST_IP == '192.168.1.23':
    #     update_time = '2021-07-07 09:33:09'
    #     update_time_stamp = datetime.datetime.strptime(update_time, '%Y-%m-%d  %H:%M:%S').timestamp()
    # else:
    #     result = query_data('devops_server', 'update_time', 'server_ip = "%s"' % HOST_IP)
    #     update_time = result[0][0].strftime('%Y-%m-%d %H:%M:%S')
    #     update_time_stamp = result[0][0].timestamp()

    # print('%s update_time: %s' % (HOST_IP, update_time))

    # query all the success build after host booted
    result = query_data('devops_compile', \
        'id, compile_build_time, compile_build_finish_time, compile_platform_id, compile_jenkins_job_id', \
        'compile_server_ip = "%s" and compile_build_time > 0 and \
        compile_build_finish_time > compile_build_time and \
        compile_is_sign = "Y" and compile_is_verify = "Y" and \
        compile_action = "ota" and compile_status = 0' % (HOST_IP), 'compile_build_time ASC')

    update_time_stamp = result[0][1].timestamp() - 60 * 10
    update_time = result[0][1].strftime('%Y-%m-%d %H:%M:%S')
    print(update_time)
    # return

    # processing data
    raw_data = {}
    before_row = None
    for row in result:
        item = {}
        item['start'] = row[1]
        item['end'] = row[2]
        item['duration'] = item['end'] - item['start']
        item['code'] = row[3]
        item['jenkins'] = row[4]

        if before_row != None and row[1] < before_row[2]:
            print('dirty data: %s' % row[1])
            continue
        before_row = row

        if item['duration'].seconds > 30000:
            print('dirty data seconds: %s' % item['duration'].seconds)
            continue
        # print('%s  duration: %s(%s seconds), jenkins id: %s' % (item['code'], item['duration'], item['duration'].seconds, item['jenkins']))

        code_list = raw_data[item['code']] if item['code'] in raw_data else []
        raw_data[item['code']] = code_list
        code_list.append(item)

    # 用黑体显示中文
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    plt.xticks(rotation=45)
    plt.xlabel('开机时间')
    plt.ylabel('编译用时')
    plt.title('%s(since %s)' % (HOST_IP, update_time))

    table_data = {}
    for code, li in raw_data.items():
        x, y = [], []
        table_data[code] = (x, y)
        for l in li:
            x.append(l['start'].timestamp() - update_time_stamp)
            y.append(l['duration'].seconds)

    for label, data in table_data.items():
        print('label: %s' % label)
        print('\tx: %s\n\ty: %s\n' % (data[0], data[1]))

    # "r" 表示红色，ms用来设置*的大小
    # plt.plot(x, y, "r", ms=10, label="a")
    for label, data in table_data.items():
        # plt.plot(data[0], data[1], marker='o', ms=5, label=label)
        plt.scatter(data[0], data[1], marker='o', s=15, label=label)
    # upper left 将图例a显示到左上角
    plt.legend(loc="upper left")
    plt.savefig('%s.jpg' % HOST_IP)
    plt.show()


if __name__ == '__main__':
    main(sys.argv[1:])
