#!/usr/bin/env python
"""
================================================
ABElectronics ADCDAC Pi 2-Channel ADC, 2-Channel DAC | DAC Write Demo

run with: python demo_dacwrite.py
================================================

this demo will generate a 1.5V p-p square wave at 1Hz
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import time
import RPi.GPIO as GPIO

import turtle
import math

try:
    from ADCDACPi import ADCDACPi
except ImportError:
    print("Failed to import ADCDACPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCDACPi import ADCDACPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
    
penpin = 17
# The lowest we can go, without deforming the Character is 0.23
sleepVariable = 0.25

GPIO.setup(penpin,GPIO.OUT) #pin down
    

def origin():
    print("Origin")
    adcdac = ADCDACPi(2)
    adcdac.set_dac_raw(1, 0)  # set the voltage on channel 1 to 1.5V
    adcdac.set_dac_raw(2, 0)   # set the voltage on channel 1 to 1.5V
    time.sleep(sleepVariable)

def drawLine(vxFrom, vxTo, vyFrom, vyTo):
    vSteps=1000
    vxStep = int(vxTo/vSteps)
    vyStep = int(vyTo/vSteps)
    time.sleep(sleepVariable)
    for i in range(1,1000):
        adcdac = ADCDACPi(2)
        adcdac.set_dac_raw(1, i*vxStep)  
        adcdac.set_dac_raw(2, i*vyStep)  
        
        print("X: ", i*vxStep)
        print("Y: ", i*vyStep)
        time.sleep(.001)

def p_StringValue(ValueAsString):
    
    for i in range(0,len(ValueAsString)):
        #p_Box(i)
        #p_A(i)
        p_O(i)
        time.sleep(sleepVariable)
        
    #origin()

def p_Box(gridOffset):
    adcdac = ADCDACPi(2)
    
    print ("Box ", gridOffset)

    gridValue=(gridOffset*120)
    
    print ("VALUE ", gridValue)
    
    # move to POINT 1 X
    adcdac.set_dac_raw(2, gridValue) 
    time.sleep(sleepVariable)
    
    # move to POINT 1 Y
    adcdac.set_dac_raw(1, 0) 
    time.sleep(sleepVariable)
    
    penDown()
    
    # Point 1 to 2
    adcdac.set_dac_raw(1, 200) 
    time.sleep(sleepVariable)
    
    # Point 2 to 3
    adcdac.set_dac_raw(2, 100+gridValue)
    time.sleep(sleepVariable)
    
    # Point 3 to 4
    adcdac.set_dac_raw(1, 0)
    time.sleep(sleepVariable)
    
    # Point 4 to 5
    adcdac.set_dac_raw(2, 0+gridValue)
    time.sleep(sleepVariable)
    
    penUp()
    

def PointsInCircum(r,n=100):
    pi=math.pi
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]
    
def p_O(gridOffset):
    print("O")
    penUp()
    gridValue=(gridOffset*120)
    adcdac = ADCDACPi(2)
    #adcdac.set_dac_raw(1, 100) 
    #adcdac.set_dac_raw(2, 50+gridValue) 
    time.sleep(sleepVariable)
    penDown()
    time.sleep(sleepVariable)
    
    zeroX = 100
    zeroY = 200
    r=100
    #adcdac.set_dac_raw(1, 100) 
    #adcdac.set_dac_raw(2, zeroY-r) 
    penDown()
    pointArr = PointsInCircum(r,n=100)
    for i in range(0, len(pointArr)):
        adcdac.set_dac_raw(1, int(pointArr[i][0])+r+10) 
        adcdac.set_dac_raw(2, int(pointArr[i][1])+r+10) 
        print(int(pointArr[i][0])+r, int(pointArr[i][1])+r) 
        time.sleep(.02)
    time.sleep(1)
    penUp()
    #origin()
        
    

    
    

def p_A(gridOffset):
    print("A")
    
    gridValue=(gridOffset*120)
    
    print ("VALUE ", gridValue)
    
    
    adcdac = ADCDACPi(2)
    adcdac.set_dac_raw(1, 0) 
    adcdac.set_dac_raw(2, 0+gridValue) 
    time.sleep(sleepVariable)
    
    penDown()
    # line from 1 to 2
    adcdac.set_dac_raw(1, 200)  
    adcdac.set_dac_raw(2, 50+gridValue)   
    time.sleep(sleepVariable)
    
    # line from 2 to 3
    adcdac.set_dac_raw(1, 0)  
    adcdac.set_dac_raw(2, 100+gridValue)  
    time.sleep(sleepVariable)
    penUp()
    adcdac.set_dac_raw(1, 100)  
    adcdac.set_dac_raw(2, 20+gridValue)   
    time.sleep(sleepVariable)
    penDown()
    adcdac.set_dac_raw(1, 100)  
    adcdac.set_dac_raw(2, 80+gridValue)   
    time.sleep(sleepVariable)
    penUp()
    
def penDown():
    GPIO.output(penpin, 1)
    time.sleep(sleepVariable)
    
def penUp():
    GPIO.output(penpin,0)
    time.sleep(sleepVariable)

def moveToGrid(gridNumber):
    adcdac = ADCDACPi(2)
    #adcdac.set_dac_raw(1, (gridNumber*1010))
    adcdac.set_dac_raw(1, 2000)
    print(gridNumber*1000)
    adcdac.set_dac_raw(2, 1000)
    
    time.sleep(sleepVariable)
    


def main():
    '''
    Main program function
    '''

    # create an instance of the ADCDAC Pi with a DAC gain set to 1
    
    
    #origin()
    #p_A()
    while True:
        p_StringValue("O")
    
    
    

if __name__ == "__main__":
    main()

    
 