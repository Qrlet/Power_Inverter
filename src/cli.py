# This module serves as command line interface for power inverter project
import click
import RTU
from sensor_api import *


@click.command()
@click.option("--mock", default=False, help="If true will use mocked objects", type=bool)
def main(mock):
	factory = RTU.ModbusFactory()
	if not mock:
		rtu = factory.factory("mocked")

	sensor = MockedWidthSensor()
	sensor_thread = SensorThread(sensor)
	regulator_thread = RegulatorThread()
	sensor_thread.register(regulator_thread)
	regulator_thread.register(rtu)

	sensor_thread.start()
	regulator_thread.start()

if __name__ == "__main__":
	main()
