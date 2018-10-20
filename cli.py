""" This module serves as command line interface for power inverter project"""
from modbus import MockedRtuSlave
from sensor import MockedWidthSensor, SensorNotifier
import gui
import sys


def main():
    """
    Run environment with all objects.
    ToDo: cleaning up all threads
    """
    app = gui.QtWidgets.QApplication(sys.argv)
    window = gui.QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(window)
    ui.setup_signals()
    window.show()

    modbus_mock = MockedRtuSlave()
    sensor_mock = MockedWidthSensor()
    sensor_thread = SensorNotifier(sensor_mock)
    sensor_thread.register(ui.sensor_widget)

    sensor_thread.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    from logging.config import fileConfig
    fileConfig('logging_config.ini', disable_existing_loggers=False)
    main()
