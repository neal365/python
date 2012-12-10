# coding=gbk
"""-----------------------------------------------------------------------------
#  Module Name          :  AT Serial
#
#  Description          :  Implement serial input/output and at command function
#    
#  Author               :  
#
#  --------------------------  Revision History  -------------------------------
# 2011-8-1       njugui@gmail.com      created     
#                                       
#----------------------------------------------------------------------------"""
import serial
import sys
from at_Log import *

"""------------Globe Configuration------------"""
 
 
class AT_serial(object):
    """ Implement AT commands by serial """
    def __init__(self,
                port,                 
                baudrate,
                timeout = 2):
        self.serial = serial.Serial()
        self.serial.baudrate = baudrate
        self.serial.port = port
        self.serial.timeout = timeout
        self.openSerial()
        
    def __del__(self):
        self.closeSerial()
            
    def openSerial(self):
        try:
            self.serial.open()
            log(  "Serial open successful.")
        except:
            log(  "Serial port %s cannot open!!!" % self.serial.port)
            sys.exit()
        
    def closeSerial(self):
        self.serial.close()      
        
    def ATRun(self, atCommand):
        self.serial.write(atCommand + "\r")   
      
    def verdictAT(self, atCommand):
        atResult = self.serial.readall()
        resultLength = len(atResult)
        if "OK" in atResult:#verdict by the last "OK" that phone returned
            log(  "atCommand(%s) Pass " % atCommand)
            return True
        else:
            log(  "atCommand(%s) Fail, result is:(length=%d) %s" % (atCommand, resultLength, atResult))
            return False

    
    
    