import os
import socket
import sys

from av import Audio, Camera
from heartbeat import HeartBeat
from settings import p2_hostname, socket_chunk_size, tablename
from sql_utils import create_connection, create_table, insert
from upload import Uploader


path = os.path.dirname(os.path.realpath(__file__))
camera_path = os.path.join(path, '{}_cam.h264'.format(p2_hostname))
audio_path = os.path.join(path, 'recording.wav')
sql_path = os.path.join(path, '{}.db'.format(p2_hostname))


column_type_dict = {'BPM': 'integer'}


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345
s.connect((host, port))
command = s.recv(socket_chunk_size).decode()

if command == 'start':
    hb = HeartBeat()
    camera = Camera(camera_path)
    mic = Audio(audio_path)
    camera.start()
    mic.start()
    conn = create_connection(sql_path)
    create_table(conn, tablename, column_type_dict)
elif command == 'run':
    bpm = hb.run()
    insert(conn, tablename, column_type_dict.keys(), [bpm])
elif command == 'stop':
    s.close
    camera.stop()
    mic.stop()
    u = Uploader(12)
    u.upload(sql_path)
    u.upload(camera_path)
else:
    sys.exit("Error! Wrong command '{}' sent.".format(command))
