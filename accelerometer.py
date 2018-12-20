"""
https://github.com/adafruit/Adafruit_Python_BNO055/blob/master/examples/simpletest.py
"""
from Adafruit_BNO055 import BNO055

accelerometer_columns = [
    'quaternion_x', 'quaternion_y', 'quaternion_z', 'quaternion_w',
    'temperature (celcius)', 'magnetometer_x (micro-Teslas)',
    'magnetometer_y (micro-Teslas)',
    'magnetometer_z (micro-Teslas)',
    'gyroscope_x (degrees/sec)', 'gyroscope_y (degrees/sec)',
    'gyroscope_z (degrees/sec)', 'accelerometer_x (m/sec^2)',
    'accelerometer_y (m/sec^2)', 'accelerometer_z (m/sec^2)',
    'linear_acceleration_x (m/sec^2)', 'linear_acceleration_y (m/sec^2)',
    'linear_acceleration_z (m/sec^2)', 'gravity_acceleration_x',
    'gravity_acceleration_y', 'gravity_acceleration_z',
]
accelerometer_columns_dict = dict.fromkeys(accelerometer_columns, 'real')


class Accelerometer(object):

    def __init__(self):
        self.bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
        if not self.bno.begin():
            raise RuntimeError('Failed to initialize BNO055.')
        self.values = []

    def diagnostics(self):
        sw, bl, accel, mag, gyro = self.bno.get_revision()
        print('Software version:   {0}'.format(sw))
        print('Bootloader version: {0}'.format(bl))
        print('Accelerometer ID:   0x{0:02X}'.format(accel))
        print('Magnetometer ID:    0x{0:02X}'.format(mag))
        print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

    def run(self):
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        heading, roll, pitch = self.bno.read_euler()
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        sys, gyro, accel, mag = self.bno.get_calibration_status()
        # Print everything out.
        print(
            """
            Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}
            Sys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}
            """.format(heading, roll, pitch, sys, gyro, accel, mag)
        )
        # Other values you can optionally read:
        # Orientation as a quaternion:
        qx, qy, qz, qw = self.bno.read_quaterion()
        # Sensor temperature in degrees Celsius:
        temp_c = self.bno.read_temp()
        # Magnetometer data (in micro-Teslas):
        mx, my, mz = self.bno.read_magnetometer()
        # Gyroscope data (in degrees per second):
        gx, gy, gz = self.bno.read_gyroscope()
        # Accelerometer data (in meters per second squared):
        ax, ay, az = self.bno.read_accelerometer()
        # Linear acceleration data (i.e. acceleration from movement, not gravity--
        # returned in meters per second squared):
        lax, lay, laz = self.bno.read_linear_acceleration()
        # Gravity acceleration data (i.e. acceleration just from gravity--returned
        # in meters per second squared):
        gravx, gravy, gravz = self.bno.read_gravity()
        self.values.append([
            qx, qy, qz, qw,
            temp_c,
            mx, my, mz,
            gx, gy, gz,
            ax, ay, az,
            lax, lay, laz,
            gravx, gravy, gravz
        ])
