import datetime
import os
import socket
import sqlite3
import time

from accelerometer import (
    Accelerometer, accelerometer_columns, accelerometer_columns_dict
)
from av import Camera
from gps import GPS, gps_columns, gps_columns_dict
from keys import tablename
from upload import Uploader


path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    datetime.datetime.now().strftime('%Y-%m-%d')
)
sql_path = os.path.join(path, 'data.db')
camera_path = os.path.join(path, 'cam1.h264')

column_type_dict = {**accelerometer_columns_dict, **gps_columns_dict}


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    else:
        return conn


def create_table(conn, tablename, column_type_dict):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        create_table_sql = 'CREATE TABLE {}('.format(tablename)
        for column, type_ in column_type_dict.items():
            create_table_sql += '{} {},\n'.format(column, type_)
        create_table_sql += ');'
        print(create_table_sql)
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def insert(conn, tablename, columns, values):
    """
    Create a new project into the tablename table
    :param conn:
    :param project:
    :return: project id
    """
    cur = conn.cursor()
    sql = (
        'INSERT INTO {}({}) VALUES({})'
        .format(tablename, ', '.join(columns), '?' * len(columns))
    )
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid


if __name__ == '__main__':
    conn = create_connection(sql_path)
    create_table(conn, tablename, column_type_dict)

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = socket.gethostname()
    # port = 12345
    # s.bind((host, port))
    # s.listen(5)

    gps_ = GPS()
    ac = Accelerometer()
    camera = Camera(camera_path)
    camera.start()
    try:
        while True:
            ac_vals = ac.run()
            gps_vals = gps_.run()
            columns = accelerometer_columns + gps_columns
            values = ac_vals + gps_vals
            insert(conn, tablename, columns, values)
            # c, addr = s.accept()
            # print 'got connection from', addr
            # c.send('Thank you for connecting')
            time.sleep(1)
    except(KeyboardInterrupt, SystemExit):
        # c.close()
        gps_.close()
        camera.stop()
        conn.close()
        u = Uploader(12)
        u.upload(sql_path)
        u.upload(camera_path)
