# This module serves as command line interface for power inverter project
import click
import RTU


@click.command()
@click.option("--mock", default=False, help="If true will use mocked objects")
def main(mock):
	factory = RTU.ModbusFactory()
	if not mock:
		rtu = factory.factory("mocked")


if __name__ == "__main__":
	main()
