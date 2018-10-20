"""
This module will provide API regardless sensor hardware.
"""
import numpy as np
from time import sleep
from threading import Thread
import logging


logger = logging.getLogger(__name__)


class SensorNotifier(Thread):
    """
    Object responsible for notifying about new sensor measurements.
    """
    def __init__(self, sensor_object):
        Thread.__init__(self)
        self.sensor_object = sensor_object
        self.observers = []

    def register(self, observer):
        """
        Add new observer.

        :param observer: observer object with required 'feed_value' method
        """
        assert hasattr(observer, "feed_value"), "Given object: {} does not have 'feed_value' attribute".format(observer)
        self.observers.append(observer)
        logger.debug("SensorNotifier registered: {}".format(observer))

    def notify(self, reading):
        """
        Notifies registered object by executing 'feed_value'.

        :param reading: float, sensor value
        """
        for observer in self.observers:
            logger.debug("Notifying {} about new width: {}".format(observer, reading))
            observer.feed_value(reading)

    def run(self):
        """
        This will be run when thread is started.
        """
        while True:
            try:
                reading = self.sensor_object.get_width()
            except Exception:
                logger.warning("Unable to receive sensor readings.")
            else:
                self.notify(reading)
            sleep(0.05)


class MockedWidthSensor(object):
    """
    An example of Sensor with mocked value generation.
    """
    @staticmethod
    def get_width():
        """
        Generate random sensor readings

        :return: float from standard distribution N(50,1)
        """
        return np.random.randn() + 50.0
