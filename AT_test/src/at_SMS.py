# coding=gbk
"""-----------------------------------------------------------------------------
#  Module Name          :  SMS mudule
#
#  Description          :  Implement SMS sending/receiving function
#    
#  Author               :  
#
#  --------------------------  Revision History  -------------------------------
# 2011-8-1       njugui@gmail.com      created     
#                                       
#----------------------------------------------------------------------------"""

import time
from at_Log import *

"""------------AT Commands------------"""
AT_SMSFORMAT_PDU = "AT+CMGF=0"
AT_SMSFORMAT_TEXT = "AT+CMGF=1"
AT_SMS_PDU = "AT+CMGS="
AT_SMS_TEXT = "AT+CMGS=" 


class AT_SMS(object):
    """  take care of SMS sending or receiving   """
    def __init__(self,
                 serial_c,
                 target = "+10086",
                 content = "1",
                 SMSC = "+8613800210500"            
                 ):
        self.SMS_content = content
        self.SMS_cn = False      #True means SMS contains Chinese, use unicode coding; or use 7-bit
        self.SMS_center = SMSC
        self.SMS_target = target
        self.serial_c = serial_c
        self.serial = self.serial_c.serial
        self.CheckCn()
    
    def CheckCn(self):
        for char in self.SMS_content:
            if ord(char) > 127:
                self.SMS_cn = True
                log(  "SMS content contains Chinese!" )
                return 0
        
    def SendSMS_Pdu(self):
        atCommand = AT_SMSFORMAT_PDU
        self.serial_c.ATRun(atCommand) 
        time.sleep(2)
        self.serial_c.verdictAT(atCommand)   
           
        TargetPhoneNumber_Pdu = self.GetTargetPhoneNumber_Pdu()
        log( "TargetPhoneNumber_Pdu = %s" % TargetPhoneNumber_Pdu)
        SMSCenterNumber_Pdu = self.GetSMSCenterNumber_Pdu()
        log(  "SMSCenterNumber_Pdu = %s" % SMSCenterNumber_Pdu )
        SMSContent_Pdu = self.GetSMSContent_Pdu()
        log(  "SMSContent_Pdu = %s" % SMSContent_Pdu)
        
        if self.SMS_cn: #If SMS content contains Chinese, use 8 bit ; or use 7 bit coding
            SMSCombine_Pdu = SMSCenterNumber_Pdu + TargetPhoneNumber_Pdu + "000800" + SMSContent_Pdu 
        else:
            SMSCombine_Pdu = SMSCenterNumber_Pdu + TargetPhoneNumber_Pdu + "000700" + SMSContent_Pdu 
        pduLength = len(SMSCombine_Pdu)/2
    
        atCommand = AT_SMS_PDU + str(pduLength)
        self.serial_c.ATRun(atCommand) 
        time.sleep(2)
        self.serial_c.verdictAT(atCommand) 
            
        atCommand = SMSCombine_Pdu + chr(26)  #ctrl+Z
        self.serial_c.ATRun(atCommand) 
        time.sleep(10)
        self.serial_c.verdictAT(atCommand)       
    
    
    def GetTargetPhoneNumber_Pdu(self):
        targetPhoneNumber = self.SMS_target
        if targetPhoneNumber.find("+") == 0:
            targetPhoneNumber = targetPhoneNumber.replace("+","")
        if len(targetPhoneNumber) % 2 == 1:
            targetPhoneNumber += "F" 
         
        newAddr = ""
        for i in range(0, len(targetPhoneNumber)/2):
            newAddr += targetPhoneNumber[i*2 + 1]
            newAddr += targetPhoneNumber[i*2]
        newAddr = "11000D91" + newAddr
    
        return newAddr
    
    def GetUnicodeFromString(self, str):
        str = unicode(str)
        str_uni = ""
        for char in str:
            char_uni = str(hex(ord(char)))
            char_uni = char_uni.replace("0x", "")
            str_uni += char_uni
            
    def GetSMSContent_Pdu(self):
        SMScontent = unicode(self.SMS_content)
        SMScontent_unicode = ""
        for char in SMScontent:
            char_unicode = str(hex(ord(char)))    
            char_unicode = char_unicode.replace("0x", "")
            if len(char_unicode) == 2 and self.SMS_cn:   #English add 2 code
                char_unicode = "00" + char_unicode
            SMScontent_unicode += char_unicode
        
        newLength = hex(len(SMScontent_unicode)/2)
        newLength = newLength.replace("0x","")    
        if len(newLength) == 1:
            newLength = "0" + newLength
            
        SMScontent_unicode = newLength + SMScontent_unicode    
        return SMScontent_unicode
    
                
    def GetSMSCenterNumber_Pdu(self):    
        smsCenterNumber = self.SMS_center
        if smsCenterNumber.find("+") == 0:
            smsCenterNumber = smsCenterNumber.replace("+", "")
        if len(smsCenterNumber) % 2 == 1:
            smsCenterNumber += "F"
            
        newAddr = ""
        for i in range(0, len(smsCenterNumber)/2):
            newAddr += smsCenterNumber[i*2 + 1]
            newAddr += smsCenterNumber[i*2 ]
        newAddr = "91" + newAddr
        
        newLength = hex(len(newAddr)/2)
        newLength = newLength.replace("0x","")    
        if len(newLength) == 1:
            newLength = "0" + newLength
        newAddr = newLength + newAddr
        
        return newAddr
                        
    def SendSMS_text(self):
        atCommand = AT_SMSFORMAT_TEXT
        self.serial_c.ATRun(atCommand) 
        time.sleep(2)
        self.serial_c.verdictAT(atCommand)   
           
    
        atCommand = AT_SMS_TEXT + '\"' + self.SMS_target + '\"'
        self.serial_c.ATRun(atCommand) 
        time.sleep(2)
        self.serial_c.verdictAT(atCommand) 
            
        atCommand = self.SMS_content + chr(26)  #ctrl+Z as end of SMS
        self.serial_c.ATRun(atCommand) 
        time.sleep(10)
        self.serial_c.verdictAT(atCommand)         

    
    
    