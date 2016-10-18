"""
This module will provide API regardless sensor hardware.
"""
import numpy.random as np


class WidthSensor(object):
    """
    Mocked sensor class.
    """
    def __init__(self, sensor_type, debug=False):
        self.sensor_handler = sensor_type
        self.debug = debug
        self.working = True
        self.current_width = self.get_width()
        if self.debug:
            print "[Sensor] Object " + str(self.sensor_handler) + " initialized."

    def __del__(self):
        self.working = False
        if self.debug:
            print "[Sensor] Object " + str(self.sensor_handler) + " closed."

    # Test connection with sensor
    def connection_test(self):
        if self.debug:
            print "[Sensor] Test: " + str(self.sensor_handler) + " connection test passed."

    # Get data from sensor
    def get_data(self):
        if self.working:
            return np.normal(100, 0.5)
        else:
            print "[Sensor] Can't receive current width."
            return None

    # Return width based on the data returned by get_data() method
    def get_width(self):
        return self.get_data()
