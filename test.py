import argparse
import os
import time

path = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser(description='Test features')
parser.add_argument('-u', '--upload', action='store_true', help='Run uploader')
parser.add_argument('-c', '--camera', action='store_true', help='Test Camera')
parser.add_argument('-a', '--audio', action='store_true', help='Test Audio record')
parser.add_argument('-g', '--gps', action='store_true', help='Test GPS')
parser.add_argument('-g', '--gps', action='store_true', help='Test GPS')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.upload:
        from upload import Uploader
        dummy_flight_id = 1
        u = Uploader(dummy_flight_id)
        u.upload(os.path.join(path, 'BOM.pdf'))

    if args.camera:
        from av import Camera
        camera = Camera(os.path.join(path, 'cam1.h264'))
        camera.start()
        time.sleep(10)
        camera.stop()

    if args.audio:
        from av import Audio
        audio = Audio(os.path.join(path, 'recording.wav'))
        audio.setup()
        audio.start()
        time.sleep(10)
        audio.stop()

    if args.gps:
        from gps import GPS
        g = GPS()
        try:
            while True:
                gps_vals = g.run()
                print(gps_vals)
                time.sleep(1)
        except(KeyboardInterrupt, SystemExit):
            print('GPS stopped')
