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
import time

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
            print "Serial open successful."
        except:
            print  "Serial port %s cannot open!!!" 
            sys.exit()
        
    def closeSerial(self):
        self.serial.close()      
        
    def ATRun(self, atCommand):
        self.serial.write(atCommand + "\r")   
      
    def verdictAT(self, atCommand):
        atResult = self.serial.read(100)  
        resultLength = len(atResult)
        if "OK" in atResult:#verdict by the last "OK" that phone returned
            print  "atCommand(%s) Pass " % atCommand
            return True
        else:
            print  "atCommand(%s) Fail, result is:(length=%d) %s" % (atCommand, resultLength, atResult)
            return False

if __name__ == '__main__':      
    at = AT_serial(port='com9', baudrate=115200)
    while 1:
        time.sleep(5)
        at.ATRun('at+off') 
        at.verdictAT('at+off') 
    
    