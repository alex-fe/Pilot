import datetime
import os
import socket
import time

from accelerometer import (
    Accelerometer, accelerometer_columns, accelerometer_columns_dict
)
from av import Camera
from gps import GPS, gps_columns, gps_columns_dict
from settings import tablename, p1_hostname
from sql_utils import create_connection, create_table, insert
from upload import Uploader


path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    datetime.datetime.now().strftime('%Y-%m-%d')
)
sql_path = os.path.join(path, '{}.db'.format(p1_hostname))
camera_path = os.path.join(path, '{}_cam.h264'.format(p1_hostname))

column_type_dict = {**accelerometer_columns_dict, **gps_columns_dict}


if __name__ == '__main__':
    conn = create_connection(sql_path)
    create_table(conn, tablename, column_type_dict)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)

    gps_ = GPS()
    ac = Accelerometer()
    camera = Camera(camera_path)
    camera.start()
    try:
        client_socket, address = server_socket.accept()
        client_socket.send('start')
        while True:
            client_socket.send('run')

            ac_vals = ac.run()
            gps_vals = gps_.run()
            columns = accelerometer_columns + gps_columns
            values = ac_vals + gps_vals
            insert(conn, tablename, columns, values)
            time.sleep(1)
    except(KeyboardInterrupt, SystemExit):
        client_socket.send('stop')
        client_socket.close()
        gps_.close()
        camera.stop()
        conn.close()
        u = Uploader(12)
        u.upload(sql_path)
        u.upload(camera_path)
