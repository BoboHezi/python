#!/usr/bin/python3
from os import path
import datetime
import matplotlib
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import time
import utils


DEV_OPS_DB = None


def query_data(table='devops_compile', keys='id, compile_build_time, compile_build_finish_time', condition=None, order=None):
    global DEV_OPS_DB
    if not DEV_OPS_DB:
        DEV_OPS_DB = mysql.connector.connect(
            host=utils.DB_HOST,
            port=utils.DB_PORT,
            user=utils.DB_USER,
            passwd=utils.DB_PASSWORD,
            database=utils.DB_DATABASE
        )
    cursor = DEV_OPS_DB.cursor()
    sql = 'select %s from %s ;' % (keys, table)
    if not utils.isempty(condition):
        sql = sql.replace(';', ' where %s;' % condition)
    if not utils.isempty(order):
        sql = sql.replace(';', ' order by %s;' % order)
    cursor.execute(sql)
    return cursor.fetchall()


def on_key_press(event):
    print(event.key)


def main():
    compile_rst = query_data(keys='id, create_time, compile_platform_id, compile_build_id, compile_server_ip', \
        condition='create_time > "2021-07-31 17:19:38"', order='create_time ASC')
    # print(compile_rst)

    first_item = compile_rst[0]
    last_item = compile_rst[-1]
    start_date = first_item[1].date()
    end_date = last_item[1].date()

    sundays = []
    sunday = start_date - datetime.timedelta(days=(start_date.weekday() + 1))
    while sunday <= end_date:
        sundays.append(sunday)
        sunday += datetime.timedelta(days=7)

    print('from %s to %s' % (start_date, end_date))

    data_map = {}
    for compile in compile_rst:
        platform = compile[2]
        create_time = compile[1]
        # get or creat platform map
        platform_map = data_map[platform] if platform in data_map else {}

        # get this sunday
        this_sun = create_time.date() - datetime.timedelta(days=(create_time.weekday() + 1))

        # get or creat date map
        date_count = platform_map[this_sun] if this_sun in platform_map else 0
        date_count += 1

        # save date_count_map
        platform_map[this_sun] = date_count
        # save platform_date_map
        data_map[platform] = platform_map

    x_date = [str(x) for x in sundays]

    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    plt.xticks(rotation=0)
    plt.xlabel('日期')
    plt.ylabel('数量')
    plt.title('编译统计')

    # genrate y & tag on diag
    lines = {}
    for platform, date_count in data_map.items():
        print('%s:' % platform)
        for date, count in date_count.items():
            print('  in week %s: %s' % (date, count))
        y = []
        for sunday in sundays:
            count = date_count[sunday] if sunday in date_count else 0
            y.append(count)
        lines[platform] = y
    # draw
    for label, y_data in lines.items():
        plt.plot(x_date, y_data, marker='o', label=label)
    plt.legend(loc="upper left")
    # while True:
    #     pos = plt.ginput(1)
    #     print(pos)
    plt.show()


if __name__ == '__main__':
    main()
