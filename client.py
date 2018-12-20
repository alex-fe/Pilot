import os
import socket

from av import Audio, Camera
from heartbeat import HeartBeat

path = os.path.dirname(os.path.realpath(__file__))
camera_path = os.path.join(path, 'cam2.h264')
audio_path = os.path.join(path, 'recording.wav')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345
s.connect((host, port))

hb = HeartBeat()
camera = Camera(camera_path)
mic = Audio(audio_path)
camera.start()
mic.start()
while True:
    bpm = hb.run()

print s.recv(1024)
s.close
camera.stop()
mic.stop()
