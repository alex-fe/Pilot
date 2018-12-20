import argparse
import os

from upload import Uploader

path = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser(description='Test features')
parser.add_argument('-u', '--upload', action='store_true', help='Run uploader')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.upload:
        dummy_flight_id = 1
        u = Uploader(dummy_flight_id)
        u.upload(os.path.join(path, 'BOM.pdf'))
