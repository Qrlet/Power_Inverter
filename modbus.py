import click
import minimalmodbus
import numpy as np
import serial
import logging
from random import randint

logger = logging.getLogger(__name__)

# Communication timeout in seconds. Value depends on circuit length
minimalmodbus.TIMEOUT = 0.07


class HitachiSlave(minimalmodbus.Instrument):
    """Controls Hitachi power inverter"""
    # Maximum and minimum frequency of power inverter: 500 = 50 Hz
    HITACHI_FREQUENCY_MAX = 500
    HITACHI_FREQUENCY_MIN = 0

    READ_WRITE_COILS = {
        "on_off": 0x0001
    }

    READ_WRITE_REGISTERS = {
        "inverter_frequency": 0x0001
    }

    FUNCTION_CODES = {
        "read coil": 0x01,
        "write coil": 0x05,
        "read register": 0x03,
        "write register": 0x06
    }

    def __init__(self, port, slave_address):
        """
        :param port: str, port of USB - RS485 adapter
        :param slave_address: int, address of hitachi slave
        """
        self.port = port
        self._set_up_port()
        self.slave_address = slave_address
        minimalmodbus.Instrument.__init__(self, port=self.port, slaveaddress=slave_address, mode="rtu")
        self.handle_local_echo = False
        logger.debug("Hitachi slave with address {} initialized at port {}".format(self.slave_address, self.port))

    def disconnect(self):
        """Disconnect device"""
        self.serial.close()
        logger.debug("Hitachi slave with address {} disconnected".format(self.slave_address))

    def _set_up_port(self):
        """
        Prepare serial port for communication with Hitachi.
        """
        ser = serial.Serial(
            port=str(self.port),
            baudrate=19200,
            timeout=None,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )
        ser.close()

    def modbus_selftest(self, code="00"):
        """
        Test modbus connection sending random data.
        :param code: code used for test purpose. Please refer to Hitachi documentation for more details.
        :return: bool, True - test passed else failed
        """
        test_data = str(randint(0, 9)) + str(randint(0, 9))
        logger.debug("Testing modbus connection with function code: {}".format(code))
        # Frame format:  address, function_code=08, code=00, test_data=xx, crc
        try:
            test_response = self._performCommand(8, code + test_data)
        except IOError as e:
            logger.debug(str(e))
            exit(1)
        else:
            if str(test_response) == code + test_data:
                logger.debug("Test of connection passed.")
                return 1
            else:
                logger.debug("Test of connection failed.")
                return 0

    def get_status(self):
        """
        Check if device is turned on / off.
        """
        return self.read_bit(self.READ_WRITE_COILS["on_off"],
                             functioncode=self.FUNCTION_CODES["read coil"])

    def turn_onoff_device(self, turn_on):
        """
        Turn on / off device
        :param turn_on: bool, True for 'on' else 'off'
        """
        logger.debug("Turning {} device.".format("On" if turn_on is True else "Off"))
        self.write_bit(self.READ_WRITE_COILS["on_off"],
                       value=1 if turn_on is True else 0,
                       functioncode=self.FUNCTION_CODES["write coil"])

    def set_frequency(self, frequency):
        """
        Set power inverter frequency.
        :param frequency: float frequency of power inverter.
        """
        assert self.HITACHI_FREQUENCY_MIN <= frequency <= self.HITACHI_FREQUENCY_MAX, "Wrong frequency value: {}"\
            .format(frequency)
        logger.debug("Set frequency to " + str(frequency))
        self.write_register(self.READ_WRITE_REGISTERS["inverter_frequency"],
                            frequency,
                            functioncode=self.FUNCTION_CODES["write register"])

    def get_frequency(self):
        """
        Read power inverter frequency
        :return: float, frequency.
        """
        logger.debug("Getting frequency from {} register".format(self.READ_WRITE_REGISTERS["inverter_frequency"]))
        return self.read_register(self.READ_WRITE_REGISTERS["inverter_frequency"],
                                  functioncode=self.FUNCTION_CODES["read register"])


class MockedRtuSlave:
    """
    Mocked modbus rtu slave. This object can be modified for test purpose.
    """
    def __init__(self):
        logger.debug("Mocked rtu created")

    @staticmethod
    def disconnect():
        logger.debug("Device disconnected")

    @staticmethod
    def set_frequency(freq):
        """
        Set mock frequency
        :param freq: float, freq to be printed
        """
        logger.debug("Frequency set to: {}".format(freq))

    @staticmethod
    def get_frequency():
        """
        Generate random frequency
        :return: float, frequency
        """
        freq = 10.0 * np.random.randn() + 50.0
        logger.debug("Current frequency is: {}".format(freq))
        return freq


@click.command()
@click.option("--port", required=True, help="USB adapter serial port")
@click.option("--addr", required=True, help="SLave address of hitachi power inverter", type=int)
def run_hitachi_slave(port, addr):
    """
    Interact with Hitachi power inverter.
    """
    slave = HitachiSlave(port, addr)
    slave.turn_onoff_device(True)
    try:
        while True:
            freq = float(input("\nProvide frequency: "))
            slave.set_frequency(freq)
    except KeyboardInterrupt:
        print("Script interrupted!")
    finally:
        slave.turn_onoff_device(False)
        slave.disconnect()


if __name__ == "__main__":
    run_hitachi_slave()

