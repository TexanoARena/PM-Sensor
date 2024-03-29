#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, smbus, RPi.GPIO as GPIO


# LCD + hardware constants
LCD_BUS = 1
I2C_ADDR_LCD  = 0x27
I2C_ADDR = I2C_ADDR_LCD
LCD_WIDTH = 20   # Maximum characters per line
LCD_POS = 80   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface - LCD Display
BUS_LCD = smbus.SMBus(LCD_BUS)

## LCD Functions

def lcd_init():
  BUS_LCD.open(LCD_BUS)
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
  # High bits
  BUS_LCD.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)
  # Low bits
  BUS_LCD.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  BUS_LCD.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  BUS_LCD.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_print(line, message):
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]), LCD_CHR)

def lcd_string(msg):
  # Send string to display
  msglen = len(msg)
  if msglen >= 20 or msglen <=20:
    message = msg[0:20].ljust(LCD_WIDTH," ")
    #print "1:",message
    lcd_print(LCD_LINE_1, message)
  if msglen >= 40 or msglen <= 40:
    message = msg[20:40].ljust(LCD_WIDTH," ")
    #print "2:",message
    lcd_print(LCD_LINE_2, message)
  if msglen >= 60 or msglen <= 60:
    message = msg[40:60].ljust(LCD_WIDTH," ")
    #print "3:",message
    lcd_print(LCD_LINE_3, message)
  if msglen >= 80 or msglen <= 80:
    message = msg[60:80].ljust(LCD_WIDTH," ")
    #print "4:",message
    lcd_print(LCD_LINE_4, message)
