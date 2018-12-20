import threading
from gps import gps, WATCH_ENABLE


gpsd = None
gps_columns = [
    'latitude', 'longitude', 'time utc', 'altitude (m)', 'eps', 'epx', 'epv',
    'ept', 'speed (m/s)', 'climb', 'track', 'mode', 'satellites',
]
gps_columns_dict = dict.fromkeys(gps_columns, 'real')
gps_columns_dict['time utc'] = 'text'


class GpsPoller(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

    def run(self):
        global gpsd
        while self.gpsp.running:
            gpsd.next()


class GPS(object):

    def __init__(self):
        self.gpsp = GpsPoller()
        self.gpsp.start()
        # flight_id = uuid.uuid4()
        # counter = 0

    def run(self):
        return (
            gpsd.fix.latitude, gpsd.fix.longitude,
            '{} + {}'.format(gpsd.utc, gpsd.fix.time), gpsd.fix.altitude,
            gpsd.fix.eps, gpsd.fix.epx, gpsd.fix.epv, gpsd.fix.ept, gpsd.fix.speed,
            gpsd.fix.climb, gpsd.fix.track, gpsd.fix.mode, gpsd.satellites
        )

    def close(self):
        self.gpsp.running = False
        self.gpsp.join()
