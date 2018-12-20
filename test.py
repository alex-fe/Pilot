import argparse

from upload import Uploader


parser = argparse.ArgumentParser(description='Test features')
parser.add_argument('-u', '--upload', type='store_true', help='Run uploader')





if __name__ == '__main__':
    args = parser.parse_args()
    if args.upload:
        print('called')
    main()
