# This module serves as command line interface for power inverter project
import click
import RTU
import sensor_api


@click.command()
@click.option("--mock", default=False, help="If true will use mocked objects", type=bool)
@click.option("--mode", default="auto", help="Mode of operation: auto or manual")
def main(mock, mode):
	factory = RTU.ModbusFactory()
	if not mock:
		modbus = factory.create_modbus("mocked")
	else:
		modbus = factory.create_modbus("rtu")

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
