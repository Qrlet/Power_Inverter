# This module serves as command line interface for power inverter project
import click
import RTU
import sensor_api


@click.command()
@click.option("--mock", default=False, help="If true will use mocked objects", type=bool)
def main(mock):
	factory = RTU.ModbusFactory()
	if not mock:
		modbus = factory.factory("mocked")
	else:
		modbus = factory.factory("rtu")

	sensor = sensor_api.MockedWidthSensor()
	sensor_thread = sensor_api.SensorThread(sensor)
	regulator_thread = sensor_api.RegulatorThread()
	sensor_thread.register(regulator_thread)
	regulator_thread.register(modbus)

	sensor_thread.start()
	regulator_thread.start()

if __name__ == "__main__":
	from logging.config import fileConfig
	fileConfig('logging_config.ini', disable_existing_loggers=False)
	main()
