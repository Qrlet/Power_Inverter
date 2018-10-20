""" This module serves as command line interface for power inverter project"""
import click
from modbus import ModbusFactory
from sensor import MockedWidthSensor, SensorNotifier
import gui
import sys


@click.command()
@click.option("--mock", default=False, help="If true will use mocked objects", type=bool)
@click.option("--mode", default="auto", help="Mode of operation: auto or manual")
def main(mock, mode):
    app = gui.QtWidgets.QApplication(sys.argv)
    window = gui.QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(window)
    ui.setup_signals()
    window.show()

    factory = ModbusFactory()
    if not mock:
        factory.create_modbus("mocked")
    else:
        factory.create_modbus("rtu")

    mocked_sensor = MockedWidthSensor()
    sensor_thread = SensorNotifier(mocked_sensor)
    sensor_thread.register(ui.sensor_widget)

    sensor_thread.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    from logging.config import fileConfig
    fileConfig('logging_config.ini', disable_existing_loggers=False)
    main()
