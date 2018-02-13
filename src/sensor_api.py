"""
This module will provide API regardless sensor hardware.
"""
import numpy as np
from time import sleep
from threading import Thread
from multiprocessing import Queue
import logging


logger = logging.getLogger(__name__)


class SensorThread(Thread):
    """
    Class handling sensor readings in thread
    Requires sensor object 
    """
    def __init__(self, sensor_object):
        Thread.__init__(self)
        self.sensor_object = sensor_object
        self.observers = []

    def register(self, observer):
        assert hasattr(observer, "feed_value"), "Given object: {} does not have 'feed_value' attribute".format(observer)
        self.observers.append(observer)
        logger.debug("SensorThread regsitered: {}".format(observer))

    def notify(self, reading):
        """
        Notifies registered object by executing 'feed_value'

        :param reading, float, sensor value
        """
        for observer in self.observers:
            logger.debug("Notifing {} about new width: {}".format(observer, reading))
            observer.feed_value(reading)

    def run(self):
        while True:
            try:
                reading = self.sensor_object.get_width()
            except:
                pass
            else:
                self.notify(reading)
            sleep(0.05)


class MockedWidthSensor(object):
    def get_width(self):
        return np.random.randn() + 50.0


class RegulatorThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.observers = []
        self.raported_width = Queue()

    def register(self, observer):
        self.observers.append(observer)
        logger.debug("RegulatorThread regsitered: {}".format(observer))

    def feed_value(self, value):
        pass

    def notify(self, freq):
        for observer in self.observers:
            logger.debug("Setting: {} new freq to: {}".format(observer, freq))
            observer.set_frequency(freq)

    def run(self):
        while True:
            self.notify(2.0 * np.random.randn() + 10.0)
            sleep(0.5)