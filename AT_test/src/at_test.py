# coding=gbk
"""-----------------------------------------------------------------------------
#  Module Name          :  AT Test
#
#  Description          :  Implement all test cases
#    
#  Author               :  
#
#  --------------------------  Revision History  -------------------------------
# 2011-8-1       njugui@gmail.com      created     
#                                       
#----------------------------------------------------------------------------"""

#import Skype4Py

from at_Serial import *
from at_SMS import *
from at_Log import *

"""------------Globe Configuration------------"""
g_testPhoneNumber = "+8615800770851"    #Your test phone number, used for terminal call
g_targetPhoneNumber = "+8615800770851"  #Target phone number for original call
g_SMScenterNumber = "+8613800210500"    #SMS center number
g_serialPort = "COM9"
g_serialBaudrate = 115200
g_SMS_content = "123hello"

 
"""------------AT Commands------------"""
AT_RADIOON = "AT+CFUN=1"
AT_RADIOOFF = "AT+CFUN=0"
AT_DIAL = "ATD"
AT_ANSWER = "ATA"
AT_HANGUP = "AT+CHUP"
AT_PDPACT_1 = "AT+CGACT=1,1"

        
class AT_test(object):
    """ implement all AT test functions"""     
    
    def __init__(self,
                 testPhoneNumber = g_testPhoneNumber,
                 targetPhoneNumber = g_targetPhoneNumber,
                 SMSC = g_SMScenterNumber
                 ):
        self.serial_c = AT_serial(port = g_serialPort,
                                  baudrate = g_serialBaudrate)
        self.serial = self.serial_c.serial
                
        self.testPhoneNumber = testPhoneNumber
        self.targetPhoneNumber = targetPhoneNumber
        self.SMSC = SMSC        
        self.SMS_c = AT_SMS(serial_c = self.serial_c,
                            target = self.targetPhoneNumber,
                            SMSC = self.SMSC,
                            content = g_SMS_content)
        self.UEisOn = False
    
    def sendSMS_PDU(self):
        self.SMS_c.SendSMS_Pdu()
        
    def sendSMS_text(self):
        self.SMS_c.SendSMS_text()
                                                    
    def callTestphone(self):
        skype = Skype4Py.Skype()
        skype.PlaceCall(g_testPhoneNumber)
    
    def radioOff(self):
        atCommand = AT_RADIOOFF
        self.serial_c.ATRun(atCommand) 
        time.sleep(10)
        if self.serial_c.verdictAT(atCommand):
            self.UEisOn = False

    def radioOn(self):
        atCommand = AT_RADIOON
        self.serial_c.ATRun(atCommand) 
        time.sleep(10)
        if self.serial_c.verdictAT(atCommand):
            self.UEisOn = True

    def MOC(self):
        atCommand = AT_DIAL + g_targetPhoneNumber + ";"
        self.serial_c.ATRun(atCommand) 
        time.sleep(15)
        self.serial_c.verdictAT(atCommand)

    def MTC(self):
        atCommand = AT_ANSWER
        self.callTestphone()
        time.sleep(30)  #wait 30 seconds for ring
        serialResult = self.serial.readall()
        if serialResult.find("RING")!= -1:
            self.serial_c.ATRun(atCommand) 
            time.sleep(15) 
            self.serial_c.verdictAT(atCommand)
        else:
            log(  "MTC Failed! Test phone didn't receive terminal call!")

    def Call_Hangup(self):
        atCommand = AT_HANGUP
        self.serial_c.ATRun(atCommand) 
        time.sleep(5)
        self.serial_c.verdictAT(atCommand)

                        
if __name__ == '__main__':   
    atTest = AT_test()
    
    log("<---- AT Test start ---->")
      
    atTest.sendSMS_PDU()   
#    atTest.MOC()
#    atTest.radioOn()
#    atTest.sendSMS_text()
       
    log("<---- AT Test finish ---->")


    
    
    