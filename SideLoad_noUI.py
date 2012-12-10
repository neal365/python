'''
Load Builds to Colt automatically!
1. get proper IP address;
2. use telnetlib to login and send commands;
3. use ftplib to transfer files;

Note: 
The only mandatory parameter you should set is 'localpath'!
You can optionally set 
'ubuntu_build_path' if you build on ubuntu.
'bugdisppath' if you need startup bugdisp.
Created on 2012-5-7
@author: njugui@gmail.com
'''

import socket
import struct 
import os
import ftplib
import telnetlib
import sys
import time

print '***********************************************************************'
print '**********Please edit me for some setting at the first time!***********'
print '***********************************************************************'
# You could set these three paths
localpath = r'C:\Code\guchen_BBBBBB\main'
ubuntu_build_path = r'\\192.168.203.131\guchen_BBBBBB_linu\main\BBBBBB\stage\armle-v7'
bugdisppath = r'C:\Code\guchen_Tools_20111114\BB_tools\BugdispToolSuite\wbugdisp.exe'


local_build_path = localpath + r'\BBBBBB\stage\armle-v7'
bin_path = localpath + r'\BBBBBB\stage\armle-v7\bin'
lib_path = localpath + r'\BBBBBB\stage\armle-v7\lib'
dll_path = localpath + r'\BBBBBB\stage\armle-v7\lib\dll'
script_path = localpath + r'\BBBBBB\ste\startup_scripts'
dir_list = [
              [bin_path,  '/radio/bin'],
              [lib_path,  '/radio/lib'],
              [dll_path,  '/radio/lib/dll'],
              [script_path,  '/radio/scripts'],
              ]       

BBBBBB_script_bakup = '''
import os
print 'Bakup start!'
command_list = ['mount -uw /radio',
                'mkdir /radio/bakup',
                'cp -R /radio/bin /radio/bakup',
               'cp -R /radio/lib /radio/bakup',
               'cp -R /radio/scripts /radio/bakup'
               ]
for command in command_list:
    os.system(command)
print 'Bakup complete!'
'''

BBBBBB_script_restore = '''
import os
print 'Restore start!'
command_list = ['mount -uw /radio',
                'rm -R /radio/bin',
                'rm -R /radio/lib',
                'rm -R /radio/scripts',
                'cp -R /radio/bakup/bin /radio',
               'cp -R /radio/bakup/lib /radio',
               'cp -R /radio/bakup/scripts /radio'
               ]
for command in command_list:
    os.system(command)
print 'Restore complete!'
'''

BBBBBB_script_empty = '''
import os
print 'Empty start!'
command_list = ['mount -uw /radio',
                'rm /radio/bin/*',
                'rm /radio/lib/*',
                'rm /radio/lib/dll/*',
                'rm /radio/scripts/*'
               ]
for command in command_list:
    os.system(command)
print 'Empty complete!'
'''


def str2uint(str):  
    return socket.ntohl(struct.unpack("I",socket.inet_aton(str))[0])  

def num2str(ip):  
    if ip < 0:  
        ip = struct.unpack("I", struct.pack('i', ip))[0]  
    return socket.inet_ntoa(struct.pack('I',socket.htonl(ip))) 

def getIPAddresses():
    from ctypes import Structure, windll, sizeof
    from ctypes import POINTER, byref
    from ctypes import c_ulong, c_uint, c_ubyte, c_char
    MAX_ADAPTER_DESCRIPTION_LENGTH = 128
    MAX_ADAPTER_NAME_LENGTH = 256
    MAX_ADAPTER_ADDRESS_LENGTH = 8
    class IP_ADDR_STRING(Structure):
        pass
    LP_IP_ADDR_STRING = POINTER(IP_ADDR_STRING)
    IP_ADDR_STRING._fields_ = [
        ("next", LP_IP_ADDR_STRING),
        ("ipAddress", c_char * 16),
        ("ipMask", c_char * 16),
        ("context", c_ulong)]
    class IP_ADAPTER_INFO (Structure):
        pass
    LP_IP_ADAPTER_INFO = POINTER(IP_ADAPTER_INFO)
    IP_ADAPTER_INFO._fields_ = [
        ("next", LP_IP_ADAPTER_INFO),
        ("comboIndex", c_ulong),
        ("adapterName", c_char * (MAX_ADAPTER_NAME_LENGTH + 4)),
        ("description", c_char * (MAX_ADAPTER_DESCRIPTION_LENGTH + 4)),
        ("addressLength", c_uint),
        ("address", c_ubyte * MAX_ADAPTER_ADDRESS_LENGTH),
        ("index", c_ulong),
        ("type", c_uint),
        ("dhcpEnabled", c_uint),
        ("currentIpAddress", LP_IP_ADDR_STRING),
        ("ipAddressList", IP_ADDR_STRING),
        ("gatewayList", IP_ADDR_STRING),
        ("dhcpServer", IP_ADDR_STRING),
        ("haveWins", c_uint),
        ("primaryWinsServer", IP_ADDR_STRING),
        ("secondaryWinsServer", IP_ADDR_STRING),
        ("leaseObtained", c_ulong),
        ("leaseExpires", c_ulong)]
    GetAdaptersInfo = windll.iphlpapi.GetAdaptersInfo
    GetAdaptersInfo.restype = c_ulong
    GetAdaptersInfo.argtypes = [LP_IP_ADAPTER_INFO, POINTER(c_ulong)]
    adapterList = (IP_ADAPTER_INFO * 10)()
    buflen = c_ulong(sizeof(adapterList))
    rc = GetAdaptersInfo(byref(adapterList[0]), byref(buflen))
    if rc == 0:
        for a in adapterList:
            adNode = a.ipAddressList
            while True:
                ipAddr = adNode.ipAddress
                if ipAddr:
                    yield ipAddr
                adNode = adNode.next
                if not adNode:
                    break        
        
def getIP():
    for clientIp in getIPAddresses():
        if '169.254.' in clientIp:
            print 'Client IP is ' + clientIp 
            BBBBBB_IP = str2uint(clientIp)
            BBBBBB_IP = num2str(BBBBBB_IP - 1)
            print 'Device IP is ' + BBBBBB_IP 
            return BBBBBB_IP          
    print 'Your connection with Colt was lost!' 
    return ''

def sendCommand(telnet_conn, cmd):
    cmd = str(cmd)
    telnet_conn.read_until('# ')
    telnet_conn.write(cmd)
    telnet_conn.write('\r')   
    telnet_conn.write('\n')  
    telnet_conn.write('pwd')
    telnet_conn.write('\r')   
    telnet_conn.write('\n')                    

def  copyFromUbuntu():
    print '******Do you want to copy build from ubuntu?(y/n)******'
    if raw_input() == 'y':    
        command = 'ROBOCOPY ' + ubuntu_build_path + ' ' + local_build_path + ' /R:0 /MIR'
        if os.system(command) != 0:
            print 'Copy build from ubuntu to Windows failed, Please check your ubuntu setting!'

def uploadFile2Radio(ftp_conn, filename, filecontent):
    print 'uploaded ' + filename + ' to device: /radio '
    file = open(filename, 'w')
    file.write(filecontent)
    file.close()  
    file = open(filename,'rb') 
    ftp_result = ftp_conn.storbinary(r'STOR /radio/' + filename, file)
    if not 'complete' in ftp_result:
        print filename + ' transfer failed! Please check you device connection! '
        return
    file.close()
    os.remove(filename)
                    
def sideload():
    'Step1: connect colt on telnet and ftp'
    BBBBBB_IP = getIP()
    if BBBBBB_IP == '':
        print 'Your connection with Colt was lost! I will exit at 10 seconds!'
        time.sleep(10)
        return
    try:
        print '******Try connecting to device on telnet and ftp, please wait a moment!******'
        telnet_conn = telnetlib.Telnet(BBBBBB_IP)
        telnet_conn.set_debuglevel(1)
        telnet_conn.read_until('login: ')
        telnet_conn.write('root')
        telnet_conn.write('\n')
        telnet_conn.read_until('Password:')
        telnet_conn.write('root')
        telnet_conn.write('\n')
        print '******Telnet connection setup success!******'
                                
        ftp_conn = ftplib.FTP(BBBBBB_IP,'root','root') # Connect
        ftp_conn.set_debuglevel(1)
        print '******Ftp connection setup success!******'
    except Exception,e:
        print 'Connect to device failed! error code is:'
        print  e
        print 'I will exit at 10 seconds!'
        time.sleep(10)      
        return
 
    'step2: mount /radio'      
    sendCommand(telnet_conn,'mount -uw /radio')
    
    'upload bakup and restore scripts to device'
    uploadFile2Radio(ftp_conn, 'BBBBBB_bakup_radio.py', BBBBBB_script_bakup)
    uploadFile2Radio(ftp_conn, 'BBBBBB_restore_radio.py', BBBBBB_script_restore)
    uploadFile2Radio(ftp_conn, 'BBBBBB_empty_radio.py', BBBBBB_script_empty)
    

    cmd_text = '''
    ******You can input number for command:******
    1. Bakup Radio
    2. Start side load
    3. Reboot the device 
    4. Start Bugdisp(make sure no VPN)
    5. Restore Radio
    6. Exit
    '''
    cmd = raw_input(cmd_text)
    while cmd != '6':
        if cmd == '1':     
            if os.path.exists('bak_flag'):
                print 'You had bakup before! You can delete bak_flag file to bakup again!'
            else:       
                open('bak_flag','w')
                sendCommand(telnet_conn,'python2.7 /radio/BBBBBB_bakup_radio.py')        
        if cmd == '3':
            sendCommand(telnet_conn,'shutdown /r')
            print 'I will exit at 5 seconds, you can restart me manually. Bye!'
            time.sleep(5)
            return
        if cmd == '4':
            os.system ( bugdisppath + ' /tcp ' + BBBBBB_IP )
        if cmd == '5':
            sendCommand(telnet_conn,'python2.7 /radio/BBBBBB_restore_radio.py')        
        if cmd == '2':       
            'step3: copy local files destination'  
            print '******start to side load*******'  
            for dir in dir_list: 
                file_list = os.listdir(dir[0]) 
                try:
                    file_list_device = ftp_conn.nlst(dir[1])
                except Exception,e:
                    print e
                    file_list_device = ''                   
                for filename in file_list: 
                    local_file = dir[0] + '/' + filename
                    target_file = dir[1] + '/' + filename
                    #if (os.path.isfile(local_file)) and (target_file in file_list_device) :
                    sendCommand(telnet_conn,'python2.7 /radio/BBBBBB_empty_radio.py')
                    if os.path.isfile(local_file) :
                        if dir[1] == '/radio/bin':
                            sendCommand(telnet_conn,'slay ' + filename)
                        sendCommand(telnet_conn,'chmod 777 ' + target_file)                                        
                        f = open(local_file,'rb')   
                        print 'Start to transfer ' + target_file 
                        try:            
                            ftp_result = ftp_conn.storbinary(r'STOR ' + target_file, f) 
                        except Exception, e: 
                            ftp_result = ''
                            while 'complete' not in ftp_result:
                                try:            
                                    ftp_result = ftp_conn.storbinary(r'STOR ' + target_file, f)                            
                                except Exception, e:
                                    print 'ftp error: ' 
                                    print e
                                    print 'try again!'  
                                    sendCommand(telnet_conn,'rm ' + target_file) 
                                    time.sleep(1)                                        
                        print target_file + ' transfered complete! ' 
                        f.close()          
            print '******Side load complete!******'                 
          
        cmd = raw_input(cmd_text)
    

if __name__ == '__main__':
    copyFromUbuntu()
    sideload()

    




