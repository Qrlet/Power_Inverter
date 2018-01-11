"""
This module contain class which controls I/O between power inverter and width sensor. Logic should be in otoher module.
"""
import Modbus.RTU
import Sensor.sensor_api
from serial.tools.list_ports_windows import comports
from PyQt4 import QtGui, QtCore
import sys


# TODO: Algorithm for starting
# TODO: Shape validation
# TODO: Algorithm adjusting frequency based on width
# TODO: Stop condition
# TODO: Class processing image

# List of active com ports
HITACHI_PORT = [port[0] for port in comports()]
COM_PORT = HITACHI_PORT[0]
# Hardcoded parameters
DEVICE_ADDRESS = 1
DEBUG = True
SENSOR_TYPE = "TYPE_1"
# 1 is lowest possible value which power inverter is sensitive to
ERROR = 1


class Controller(object):
    """
    Controller object crates two instances of classes that will communicate with themselves
    """
    def __init__(self):
        self._width = 0.0
        try:
            self.modbus_object = Modbus.RTU.HitachiSlave(DEVICE_ADDRESS, COM_PORT, False, False)
            self.sensor_object = Sensor.sensor_api.WidthSensor(SENSOR_TYPE, True)
        except Exception as e:
            print e
            print "[Controller] Can't create modbus or sensor objects."
            exit(1)
        else:
            if DEBUG:
                print "[Controller] Modbus and sensor objects created."

    def test_handlers(self):
        self.modbus_object.modbus_test()
        self.sensor_object.connection_test()
        if DEBUG:
            print "[Controller] Power inverter and " + str(self.sensor_object) + " tested."

    # This method stores width value which is baseline for algorithms
    def set_width(self, width):
        self._width = width
        if DEBUG:
            print "[Controller] Width value set to: " + str(self._width)

    def get_sensor_width(self):
        return self.sensor_object.get_width()

    # This method should be called periodic via some timer in order to change frequency
    def calculate_velocity(self):
        current_width = self.get_sensor_width()
        if DEBUG:
            print "[Controller] Current width: " + str(current_width)
        difference = self._width - current_width
        if abs(difference) < ERROR:
            if DEBUG:
                print "[Controller] Width OK."
        else:
            if DEBUG:
                print "[Controller] Width difference: " + str(difference)
            self.adjust_frequency(difference)

    # This method adjust frequency depending on width
    def adjust_frequency(self, width_difference):
        # Get current frequency
        current_frequency = self.modbus_object.get_frequency()
        if DEBUG:
            print "[Controller] Current frequency " + str(current_frequency)
        # Calculate target frequency
        target_frequency = current_frequency + width_difference
        self.modbus_object.set_frequency(target_frequency)
        if DEBUG:
            print "[Controller] Set frequency to " + str(target_frequency) + "\n"


if __name__ == "__main__":
    controller_test = Controller()
    controller_test.test_handlers()
    controller_test.set_width(100.0)
    controller_test.modbus_object.turn_on_device()
    controller_test.modbus_object.set_frequency(100.0)
    app = QtGui.QApplication(sys.argv)
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: controller_test.calculate_velocity())
    timer.start(100)
    sys.exit(app.exec_())

