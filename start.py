#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd, time, logging
from lcd_functions import *
from sensor_functions import *

def do_single_read():
    global VoRawCount
    global dustDensityVoTotal
    value_raw = pmReadValue()
    voMeasured = LEtoBE(value_raw)
    calcVoltage = voMeasured * (5.0 / 1024.0)
    #Vo = voMeasured / 65536.0 * 2.5;
    #Vo = voMeasured / 65536.0 * 3.3;
    Vo = voMeasured / 65536.0 * 5.0;
    #Vo = voMeasured / 1024.0 * 2.5
    #Voltage = value_raw*1000.0
    Voltage = Vo*100000.0
    dV = ((Vo*100.0) - 0.6)
    dustDensityVo = (dV / 0.5) * 100.0
    dustDensityVo = int(dustDensityVo)
    voDust = 0
    # calculate average
    dustDensityVoTotal += dustDensityVo
    if VoRawCount >= 50:
        voDust = (1 * dustDensityVoTotal) / 50
        msg_row_1="Stato sensore: ON   "
        msg_row_2="                    "
        msg_row_3="PM 2.5 Density: " + str(int(voDust))
        msg_row_4="                    "
        messaggio = msg_row_1+msg_row_2+msg_row_3+msg_row_4
        print messaggio
        lcd_string(messaggio.decode('utf-8'))
        VoRawCount = 0
        dustDensityVoTotal = 0
    else:
        VoRawCount = VoRawCount + 1
    return

if __name__ == "__main__":
    lcd_init()
    LINE_1="Stato sensore: ON   "
    LINE_2="                    "
    LINE_3="Acquisizione valori "
    LINE_4="PM 2.5 in corso     "
    start_msg = LINE_1 + LINE_2 + LINE_3 + LINE_4
    lcd_string(start_msg.decode('utf-8'))
    try:
        while True:
            do_single_read()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Spegnimento sensore ".decode('utf-8'))
        time.sleep(3)
        lcd_string("Spegnimento sensore                     Stato sensore: OFF  ".decode('utf-8'))
        time.sleep(3)
        lcd_byte(0x01, LCD_CMD)
        BUS_LCD.close()


