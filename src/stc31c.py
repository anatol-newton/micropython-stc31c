__version__ = "0.0.1"

from enum import Enum

from uio import AnyReadableBuf

try:
    from machine import I2C
except:
    print("no I2C module, system probably doesn't support it")


from micropython import const

# for i2c specifications see datasheet of the STC31-C
CMD_SET_DISABLE_CRC: int = const(0x3768)
CMD_SET_MEASUREMENT_MODE: int = const(0x3615)
CMD_SET_RELATIVE_HUMIDITY: int = const(0x3624)
CMD_SET_TEMPERATURE: int = const(0x361E)
CMD_SET_PRESSURE: int = const(0x362F)
CMD_GET_MEASURE_GAS_CONCENTRATION: int = const(0x3639)
CMD_SET_FORCE_RECALIBRATION: int = const(0x3661)
CMD_SET_ENABLE_AUTOMATIC_SELF_CALIBRATION: int = const(0x3FEF)
CMD_SET_DISABLE_AUTOMATIC_SELF_CALIBRATION: int = const(0x3F6E)
CMD_SET_ENABLE_WEAK_NOISE_FILTER: int = const(0x3FC8)
CMD_SET_DISABLE_WEAK_NOISE_FILTER: int = const(0x3F49)
CMD_SET_ENABLE_STRONG_NOISE_FILTER: int = const(0x3FD5)
CMD_SET_DISABLE_STRONG_NOISE_FILTER: int = const(0x3F54)
CMD_GET_SELF_TEST: int = const(0x365B)
CMD_GENERAL_CALL_RESET: int = const(0x06)
CMD_GET_PREPARE_READ_SENSOR_STATE: int = const(0x3752)
CMD_GET_READ_SENSOR_STATE: int = const(0xE133)
CMD_SET_SENSOR_WRITE_STATE: int = const(0xE133)
CMD_SET_SENSOR_APPLY_STATE: int = const(0x3650)
CMD_GET_READ_OFFSET_VALUE: int = const(0x370A)
CMD_SET_WRITE_OFFSET_VALUE: int = const(0x3608)
CMD_SET_ENTER_SLEEP_MODE: int = const(0x3677)
CMD_GET_READ_PRODUCT_IDENTIFIER0: int = const(0x367C)
CMD_GET_READ_PRODUCT_IDENTIFIER1: int = const(0xE102)

LOWNOISE_CO2_N2_100: int = const(0x0000)
LOWNOISE_CO2_AIR_100: int = const(0x0001)
LOWNOISE_CO2_N2_25: int = const(0x0002)
LOWNOISE_CO2_AIR_25: int = const(0x0003)
STANDARD_CO2_N2_100: int = const(0x0010)
STANDARD_CO2_AIR_100: int = const(0x0011)
STANDARD_CO2_N2_40: int = const(0x0012)
STANDARD_CO2_AIR_40: int = const(0x0013)

class STC31C:
    def __init__(self, i2c: I2C, address: int = 0x29):
        self.address = address
        self.i2c = i2c

    def start(self) -> int:
        # check for the device on the given i2c address
        if self.i2c.write(self.address.to_bytes()) != 1:
            # device did not send ack
            print(f"stc32-c not found at address {self.address}!")
            return -1

        # disable CRC, as I (TODO) have not yet implemented CRC calculation
        self.i2c.writeto(self.address, CMD_SET_DISABLE_CRC.to_bytes(2))

        # everything fine, no error
        return 0

    def measurement_mode(self, mode: int) -> int:
        if self.i2c.writeto(self.address, CMD_SET_MEASUREMENT_MODE.to_bytes(2) + mode.to_bytes(2)) != 5:
            # not every message received an ack
            return -1
        # everything fine, no error
        return 0

    def measure_gas_concentration(self):
        # TODO implement error check
        buf: bytes = bytes(4)
        self.i2c.writeto(self.address, CMD_GET_MEASURE_GAS_CONCENTRATION.to_bytes(2))
        self.i2c.readfrom_into(self.address, buf)
        # TODO convert data into usable format
        return buf

    # TODO implement other sensor functionality

    @staticmethod
    def crc8(data: AnyReadableBuf, poly: int, init: int, final_xor: int = 0x00):
        # TODO implement crc8
        pass
