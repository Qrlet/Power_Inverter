import minimalmodbus
import time
import numpy as np
import serial
import serial.tools.list_ports
import logging
from logging.config import fileConfig


fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

# Adjust properly
minimalmodbus.TIMEOUT = 0.07

# TODO: Update coils and registers
# TODO: print set/get frames <- SOLVED. Look at modbus_test
# TODO: Configuration of serial port
# TODO: Handle wrong frequency

# Maximum and minimum frequency of power inverter. 500 = 50 Hz
HITACHI_FRQUENCY_MAX = 500
HITACHI_FRQUENCY_MIN = 0

READ_WRITE_COILS = {
    "on_off": 0x0001
}

READ_WRITE_REGISTERS = {
    "inverter_frequency": 0x0001
}

# Make it FROZEN SET
FUNCTION_CODES = {
    "read coil": 0x01,
    "write coil": 0x05,
    "read register": 0x03,
    "write register": 0x06
}


class ModbusFactory():
    def factory(self, modbus_type):
        if modbus_type.lower()=="mocked":
            return MockedRtuSlave()
        if modbus_type.lower()=="rtu":
            return HitachiSlave()


class MockedRtuSlave():
    """
    This class is used to mock communication over modbus rtu
    """
    def __init__(self):
        logger.debug("Mocked rtu created")


    def set_frequency(self, freq):
        logger.debug("Frequency set to: {}".format(freq))


    def get_frequency(self):
        freq = 10.0 * np.random.randn() + 50.0
        logger.debug("Current frequency is: {}".format(freq))
        return freq


class HitachiSlave(minimalmodbus.Instrument):
    """ Slave class inheriting from minimalmodbus instrument class. Designed for Hitachi power inverter.
    """
    def __init__(self, device_address, com_port, debug_modbus=False):
        self.port = com_port
        self._set_up_port()
        self.device_address = device_address
        assert isinstance(debug_class, bool), "Expected bool type as debug argument."
        self.debug_class = debug_class
        minimalmodbus.Instrument.__init__(self, port=com_port, slaveaddress=device_address, mode='rtu')
        self.debug = debug_modbus
        self.handle_local_echo = False
        logger.debug("Hitachi object initialized at port " + str(self.port) + ".")


    def __del__(self):
        self.serial.close()
        if self.debug_class:
            logger.debug("Deleting Hitachi slave: " + str(self.device_address) + " at port " + str(self.port))

    def _set_up_port(self):
        ser = serial.Serial(
            port=str(self.port),
            baudrate=19200,
            timeout=None,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )
        ser.close()

    # This function test modbus connection by sending random value
    def modbus_test(self, code="00"):
        test_data = str(randint(0, 9)) + str(randint(0, 9))
        if self.debug_class:
            logger.debug("Testing modbus.")
        # Frame format:  address, function_code=08, code=00, test_data=xx, crc
        try:
            test_response = self._performCommand(8, code + test_data)
        except IOError as e:
            logger.debug("Error: " + str(e))
            exit(1)
        else:
            if str(test_response) == code + test_data:
                logger.debug("Test of connection passed." + " Request: " + code + test_data + " response: " + str(test_response))
                return 1
            else:
                logger.debug("Test of connection failed. " + "Request: " + code + test_data + " response: " + str(test_response))
                return 0


    def get_status(self):
        if self.debug_class:
            logger.debug("Checking device status.")
        return self.read_bit(READ_WRITE_COILS["on_off"], functioncode=FUNCTION_CODES["read coil"])


    def turn_on_device(self):
        if self.debug_class:
            logger.debug("Turning ON device.")
        self.write_bit(READ_WRITE_COILS["on_off"], value=1, functioncode=FUNCTION_CODES["write coil"])


    def turn_off_device(self):
        if self.debug_class:
            logger.debug("Turning OFF device.")
        self.set_frequency(HITACHI_FRQUENCY_MIN)
        self.write_bit(READ_WRITE_COILS["on_off"], value=0, functioncode=FUNCTION_CODES["write coil"])


    def set_frequency(self, frequency):
        assert HITACHI_FRQUENCY_MIN <= frequency <= HITACHI_FRQUENCY_MAX, "Wrong frequency value."
        if self.debug_class:
            logger.debug("Set frequency to " + str(frequency))
        self.write_register(READ_WRITE_REGISTERS["inverter_frequency"], frequency, functioncode=FUNCTION_CODES["write register"])


    def get_frequency(self):
        if self.debug_class:
            logger.debug("Getting frequency from register: " + str(READ_WRITE_REGISTERS["inverter_frequency"]))
        return self.read_register(READ_WRITE_REGISTERS["inverter_frequency"], functioncode=FUNCTION_CODES["read register"])
