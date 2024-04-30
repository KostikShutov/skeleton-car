import logging
import smbus2
import time
import math


class PWM(object):
    FREQUENCY: int = 60
    BUS_NUMBER: int = 1
    I2C_ADDRESS: int = 0x40

    MODE1: int = 0x00
    MODE2: int = 0x01
    SUBADR1: int = 0x02
    SUBADR2: int = 0x03
    SUBADR3: int = 0x04
    PRESCALE: int = 0xFE
    LED0_ON_L: int = 0x06
    LED0_ON_H: int = 0x07
    LED0_OFF_L: int = 0x08
    LED0_OFF_H: int = 0x09
    ALL_LED_ON_L: int = 0xFA
    ALL_LED_ON_H: int = 0xFB
    ALL_LED_OFF_L: int = 0xFC
    ALL_LED_OFF_H: int = 0xFD

    RESTART: int = 0x80
    SLEEP: int = 0x10
    ALLCALL: int = 0x01
    INVRT: int = 0x10
    OUTDRV: int = 0x04

    def __init__(self) -> None:
        self.bus = smbus2.SMBus(self.BUS_NUMBER)

    def setup(self) -> None:
        """Init the class with busNumber and address"""
        logging.info('[PWM] Resetting PCA9685 MODE1 (without SLEEP) and MODE2')
        self.writeAllValue(0, 0)
        self.writeByteData(self.MODE2, self.OUTDRV)
        self.writeByteData(self.MODE1, self.ALLCALL)
        time.sleep(0.005)

        mode1 = self.readByteData(self.MODE1)
        mode1 = mode1 & ~self.SLEEP
        self.writeByteData(self.MODE1, mode1)
        time.sleep(0.005)

        self.frequency = self.FREQUENCY

    def writeByteData(self, reg: int, value: int) -> None:
        """Write data to I2C with self.I2C_ADDRESS"""
        logging.info('[PWM] Writing value %2X to %2X', value, reg)
        try:
            self.bus.write_byte_data(self.I2C_ADDRESS, reg, value)
        except Exception as e:
            print('Run i2c.py for setting i2c:', e)

    def readByteData(self, reg: int) -> int:
        """Read data from I2C with self.I2C_ADDRESS"""
        logging.info('[PWM] Reading value from %2X' % reg)
        try:
            results = self.bus.read_byte_data(self.I2C_ADDRESS, reg)
            return results
        except Exception as e:
            print('Run i2c.py for setting i2c:', e)

    @property
    def frequency(self) -> int:
        return self.FREQUENCY

    @frequency.setter
    def frequency(self, freq: int) -> None:
        """Set PWM frequency"""
        logging.info('[PWM] Set frequency to %d', freq)
        preScaleValue = 25000000.0
        preScaleValue /= 4096.0
        preScaleValue /= float(freq)
        preScaleValue -= 1.0
        logging.info('[PWM] Setting PWM frequency to %d Hz', freq)
        logging.info('[PWM] Estimated pre-scale: %d', preScaleValue)
        preScale = math.floor(preScaleValue + 0.5)
        logging.info('[PWM] Final pre-scale: %d', preScale)

        oldMode = self.readByteData(self.MODE1)
        newMode = (oldMode & 0x7F) | 0x10
        self.writeByteData(self.MODE1, newMode)
        self.writeByteData(self.PRESCALE, int(math.floor(preScale)))
        self.writeByteData(self.MODE1, oldMode)
        time.sleep(0.005)
        self.writeByteData(self.MODE1, oldMode | 0x80)

    def write(self, channel: int, on: int, off: int) -> None:
        """Set on and off value on specific channel"""
        logging.info('[PWM] Set channel "%d" to value "%d"', channel, off)
        self.writeByteData(self.LED0_ON_L + 4 * channel, on & 0xFF)
        self.writeByteData(self.LED0_ON_H + 4 * channel, on >> 8)
        self.writeByteData(self.LED0_OFF_L + 4 * channel, off & 0xFF)
        self.writeByteData(self.LED0_OFF_H + 4 * channel, off >> 8)

    def writeAllValue(self, on: int, off: int) -> None:
        """Set on and off value on all channel"""
        logging.info('[PWM] Set all channel to value "%d"', off)
        self.writeByteData(self.ALL_LED_ON_L, on & 0xFF)
        self.writeByteData(self.ALL_LED_ON_H, on >> 8)
        self.writeByteData(self.ALL_LED_OFF_L, off & 0xFF)
        self.writeByteData(self.ALL_LED_OFF_H, off >> 8)

    def map(self, x: int, inMin: int, inMax: int, outMin: int, outMax: int):
        """To map the value from arange to another"""
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
