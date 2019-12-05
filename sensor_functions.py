#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, smbus, RPi.GPIO as GPIO


VoRawCount = 0
dustDensityVoTotal = 0

# ADS1115 + PM Sensor + hardware constants
PMS_BUS = 2
DEVICE_ADDRESS = 0x48
POINTER_CONVERSION = 0x0
POINTER_CONFIGURATION = 0x1
POINTER_LOW_THRESHOLD = 0x2
POINTER_HIGH_THRESHOLD = 0x3

RESET_ADDRESS = 0b0000000
RESET_COMMAND = 0b00000110

ALERTPIN = 27

# Open I2C device - PM Sensor
BUS_PM = smbus.SMBus(PMS_BUS)

# Use BCM GPIO references
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALERTPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  ## read mode, pull up resistor

## PM Sensor functions

def swap2Bytes(c):
    '''Revert Byte order for Words (2 Bytes, 16 Bit).'''
    return (c >> 8 | c << 8) & 0xFFFF


def prepareLEconf(BEconf):
    '''Prepare LittleEndian Byte pattern from BigEndian configuration string, with separators.'''
    c = int(BEconf.replace('-', ''), base=2)
    return swap2Bytes(c)


def LEtoBE(c):
    '''Little Endian to BigEndian conversion for signed 2Byte integers (2 complement).'''
    c = swap2Bytes(c)
    if (c >= 2 ** 15):
        c = c - 2 ** 16
    return c


def BEtoLE(c):
    '''BigEndian to LittleEndian conversion for signed 2 Byte integers (2 complement).'''
    if (c < 0):
        c = 2 ** 16 + c
    return swap2Bytes(c)


def pmReadValue():
    BUS_PM.open(PMS_BUS)
    BUS_PM.write_byte(RESET_ADDRESS, RESET_COMMAND)
    # set GPIO mode
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ALERTPIN, GPIO.OUT)
    GPIO.output(ALERTPIN, GPIO.LOW)
    # compare with configuration settings from ADS115 datasheet
    # start single conversion - AIN2/GND - 4.096V - single shot - 8SPS - X - X - X - disable comparator
    conf = prepareLEconf('1-110-001-1-000-0-0-0-11')
    BUS_PM.write_word_data(DEVICE_ADDRESS, POINTER_CONFIGURATION, conf)
    # long enough to be safe that data acquisition (conversion) has completed
    # may be calculated from data rate + some extra time for safety. check accuracy in any case.
    time.sleep(0.2)
    value_raw = BUS_PM.read_word_data(DEVICE_ADDRESS, POINTER_CONVERSION)
    GPIO.output(ALERTPIN, GPIO.HIGH)
    BUS_PM.close()
    return value_raw

