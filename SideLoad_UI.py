'''
Load Builds to Device automatically!
1. get proper IP address;
2. use telnetlib to login and send commands;
3. use ftplib to transfer files;

Created on 2012-5-7
@author: njugui@gmail.com
'''
import socket
import struct 
import os
from threading import Thread   
import time
import ftplib
import telnetlib
import wx


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

def MsgDlg(window, string, caption='Warning', style=wx.YES_NO|wx.CANCEL):
    """Warning MessageDialog."""
    dlg = wx.MessageDialog(window, string, caption, style)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result
                
class TestFrame(wx.Frame):
    def __init__(self):
        self.deviceIP = ''
        self.bTelconn = False
        self.bFtpconn = False
        self.telnet_conn = None
        self.ftp_conn = None
        self.localpath = ''
        self.remotepath = ''
        self.bugdisppath = ''   
         
        self.ubuntu_ip = ''
        self.ubuntu_user = ''
        self.ubuntu_password = ''
        self.ubuntu_path = ''
        self.bTelconn_ubuntu = False
        self.telnet_ubuntu = None
        
        
        wx.Frame.__init__(self, None, title="BBBB side load utility", pos=wx.Point(50,50), size=wx.Size(800,788))
        panel = wx.Panel(self)
        
        'Telnet control'
        self.telnetCtrl = wx.TextCtrl(panel, -1, '', wx.Point(21, 100), wx.Size(338,25), wx.TE_PROCESS_ENTER)
        self.telnetCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnTelnetCtrl)
        
        'Log control'
        self.logCtrl = wx.TextCtrl(panel, -1, '', wx.Point(21, 125), wx.Size(338,525), wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2  )

        img1 = wx.Image('phone1.jpg', wx.BITMAP_TYPE_ANY)
        wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img1))
                
        Btn_conn = wx.Button(panel, -1, 'Connect Device', (535, 100))
        Btn_conn.Bind(wx.EVT_BUTTON, self.connect)

        Btn_sideload = wx.Button(panel, -1, 'Side load', (535, 150))
        Btn_sideload.Bind(wx.EVT_BUTTON, self.sideload)
        
        Btn_bugdisp = wx.Button(panel, -1, 'Start Bugdisp', (535, 200))
        Btn_bugdisp.Bind(wx.EVT_BUTTON, self.start_bugdisp)

        Btn_reboot = wx.Button(panel, -1, 'Reboot device', (535, 250))
        Btn_reboot.Bind(wx.EVT_BUTTON, self.reboot)

        Btn_buildfromWin = wx.Button(panel, -1, 'Build on Windows', (535, 300))
        Btn_buildfromWin.Bind(wx.EVT_BUTTON, self.buildfromWin)

        Btn_buildfromLinux = wx.Button(panel, -1, 'Build on Ubuntu', (535, 350))
        Btn_buildfromLinux.Bind(wx.EVT_BUTTON, self.buildfromLinux)            

        Btn_backup = wx.Button(panel, -1, 'Backup device', (535, 400))
        Btn_backup.Bind(wx.EVT_BUTTON, self.backup)  
        
        Btn_restore = wx.Button(panel, -1, 'Restore device', (535, 450))
        Btn_restore.Bind(wx.EVT_BUTTON, self.restore)      
                
        Btn_setting = wx.Button(panel, -1, 'Setting', (535, 500))
        Btn_setting.Bind(wx.EVT_BUTTON, self.setting)    
        
        Btn_help = wx.Button(panel, -1, 'Help', (535, 550))
        Btn_help.Bind(wx.EVT_BUTTON, self.help)   
        
        Btn_exit = wx.Button(panel, -1, 'Exit', (535, 600))
        Btn_exit.Bind(wx.EVT_BUTTON, self.exit)                                           
#        self.getIP()
        self.init_Setting()
        
    def getIP(self):
        bConn = False
        for clientIp in getIPAddresses():
            if '169.254.' in clientIp:
                self.log(  'client IP is ' + clientIp )
                BBBBBB_IP = str2uint(clientIp)
                BBBBBB_IP = num2str(BBBBBB_IP - 1)
                self.log( r'Client IP is ' + BBBBBB_IP )
                self.deviceIP = BBBBBB_IP
                bConn = True
        if not bConn:
            self.log( 'Your connection with Device was lost!' )

    def log(self, msg):
#        timestamp = time.strftime("%b %d, %H:%M:%S", time.localtime())               
#        self.logCtrl.SetInsertionPoint(0)  
#        self.logCtrl.WriteText('\n ---------------------------------------- \n')  
#        self.logCtrl.WriteText(str(timestamp) + '\n')
        self.logCtrl.AppendText(str(msg))
        self.logCtrl.AppendText('\n')
        

    def start_bugdisp(self, event):
        if self.deviceIP == '':
            self.log('You have not connected the device yet!')
            return
        if 'bugdisp.exe' not in self.bugdisppath:
            MsgDlg(self, 'You have not set the right bugdisp path!', 'Warning!', wx.OK)
            self.setting(event)
            return
        command = self.bugdisppath + ' /tcp ' + self.deviceIP
        os.system(command)
            
    def OnTelnetCtrl(self, event):
        'Send telnet command to device'
        if self.bTelconn:
            self.sendCommand(self.telnetCtrl.GetValue())
        else:
            self.log('Telnet not connected!')
        
    def connect(self, event):
        'Step1: connect colt on telnet and ftp'
        self.getIP()
        if self.deviceIP == '':
            return
        try:
            self.telnet_conn = telnetlib.Telnet(self.deviceIP)
            self.telnet_conn.set_debuglevel(1)
            self.telnet_conn.read_until('login: ')
            self.telnet_conn.write('root')
            self.telnet_conn.write('\n')
            self.telnet_conn.read_until('Password:')
            self.telnet_conn.write('root')
            self.telnet_conn.write('\n')
            self.log('Telnet connection setup success!')
            self.bTelconn = True
                                    
            self.ftp_conn = ftplib.FTP(self.deviceIP,'root','root') # Connect
            self.ftp_conn.set_debuglevel(1)
            self.log('Ftp connection setup success!')
            self.bFtpconn = True
        except Exception,e:
            self.log('Connect to device failed! error code is:')
            self.log( e )
            return

    def sendCommand(self, cmd):
        cmd = str(cmd)
        self.log(cmd)
        self.telnet_conn.read_until('# ')
        self.telnet_conn.write(cmd)
        self.telnet_conn.write('\r')   
        self.telnet_conn.write('\n')    
         
    def setLocalPath(self):
        if 'main' not in self.localpath:
            MsgDlg(self, 'You did not set right workspace path yet!', wx.OK)
            self.setting(None)
            return
        
        self.bin_path = self.localpath + r'\BBBBBB\stage\armle-v7\bin'
        self.lib_path = self.localpath + r'\BBBBBB\stage\armle-v7\lib'
        self.dll_path = self.localpath + r'\BBBBBB\stage\armle-v7\lib\dll'
        self.script_path = self.localpath + r'\BBBBBB\ste\startup_scripts'
        self.files2copy = [
                      [self.bin_path, '/file_2_copy/bin_tmp', '/radio/bin'],
                      [self.lib_path, '/file_2_copy/lib_tmp', '/radio/lib'],
                      [self.dll_path, '/file_2_copy/dll_tmp', '/radio/lib/dll'],
                      [self.script_path, '/file_2_copy/scripts_tmp', '/radio/scripts'],
                      ]        
            
    def sideload(self, event):
        'Step2: create temp folder, because replace files directly often have error'
        if not self.bTelconn or not self.bFtpconn:
            self.log('You did not have proper telnet and ftp connection!')
            return
        
        self.log('side load may take some minutes.')
        self.setLocalPath()
        try:
            self.ftp_conn.mkd('/file_2_copy')
            for filelist in self.files2copy:
                self.ftp_conn.mkd(filelist[1])
        except Exception, e:
            self.log( e )
    
        'step3: copy local files to temp folder'  
        self.log('******start to copy files from local to device temp folder*******' )  
        for filelist in self.files2copy: 
            filenames = os.listdir(filelist[0]) 
            for filename in filenames: 
                local_file = filelist[0] + '/' + filename
                if os.path.isfile(local_file):             
                    temp_file = filelist[1] + '/' + filename
#                    target_file = filelist[2] + '/' + filename
                    self.sendCommand('slay ' + filename)
                    self.sendCommand('chmod 777 ' + temp_file)
#                    self.sendCommand('chmod 777 ' + target_file)
                    f = open(local_file,'rb')                # file to send
                    self.ftp_conn.storbinary(r'STOR ' + temp_file, f)         # Send the file
#                    self.log('*****' + temp_file + ' uploaded.*****', )
                    f.close()          
    
        'step4: copy the script that should run on BBBBBB to remote folder, then run it'
        f = open('samecopy_BBBBBB.sh','rb')                # file to send
        self.ftp_conn.storbinary(r'STOR /file_2_copy/samecopy_BBBBBB.sh', f)         # Send the file
        self.sendCommand('chmod 777 /file_2_copy/samecopy_BBBBBB.sh')
        self.sendCommand('/file_2_copy/samecopy_BBBBBB.sh')
        self.sendCommand('ls')
     
#        ftp_conn.quit()
    #    telnet_conn.read_until('\r\n# ')
        self.log('Sideload success!')  

#        telnet_conn.close()        

    def reboot(self, event):
        if not self.bTelconn:
            self.log('You do not have proper telnet connection!')
            return
        self.sendCommand('shutdown /r')
        self.sendCommand('ls')
        self.log( 'rebooting...' )   
        
    def buildfromWin(self, event):
        if 'main' not in self.localpath:
            MsgDlg(self, 'You did not set right workspace path yet!','Error', wx.OK)
            self.setting(None)
            return        
          
        self.log('Please copy these 3 commands to cmd.exe:\n')
        command1 = 'cd ' + self.localpath + r'\BBBBBB' 
        self.log(command1)
        command2 = self.localpath + r'\BBBBBB\setupbuildenv.bat arm'
        self.log(command2)         
        command3 = self.localpath + r'\BBBBBB\build.bat arm'
        self.log(command3)         
        
    def connect_ubuntu(self):
        'Step1: connect colt on telnet and ftp'
        if self.ubuntu_ip == '':
            MsgDlg(self, 'You did not set ubuntu IP  yet!', 'Error',wx.OK)
            self.setting(None)
            return   
        try:
            self.telnet_ubuntu = telnetlib.Telnet(self.ubuntu_ip)
            self.telnet_ubuntu.set_debuglevel(1)
            self.telnet_ubuntu.read_until('login: ')
            self.telnet_ubuntu.write(self.ubuntu_user)
            self.telnet_ubuntu.write('\n')
            self.telnet_ubuntu.read_until('Password:')
            self.telnet_ubuntu.write(self.ubuntu_password)
            self.telnet_conn.write('\n')
            self.log('Ubuntu telnet connection setup success!')
            self.bTelconn_ubuntu = True
        except Exception,e:
            self.log('Connect to ubuntu failed! error code is:')
            self.log( e )
            return

    def sendCommand_ubuntu(self, cmd):
        
        self.log('connecting to ubuntu ')
        
    def buildfromLinux(self, event):
        self.log('buildfromLinux ')
        'Step1: copy source files from windows to ubuntu'
        
        '1. change writable property first'
        source_windows = self.localpath + r'\BBBBBB\ste\services\BBBBBB'
        source_ubuntu = self.remotepath + r'\BBBBBB\ste\services\BBBBBB'        
        self.connect_ubuntu()
#        cmd = 'chmod 777 ' + source_ubuntu + ' *'
#        self.sendCommand_ubuntu(cmd)
#        '2. robocopy from windows to ubuntu'
#        copy_command = 'ROBOCOPY ' + source_windows + ' ' + source_ubuntu + ' /R:0 /NOCOPY'
#        self.log( os.popen(copy_command).readlines())
        
        'step2: build from ubuntu'
        
        'step3: copy build files from ubuntu to windows'

    def backup(self, event):
        self.log('backup ')
        
    def restore(self, event):
        self.log('restore ')  

    def init_Setting(self):
        setting_path = 'colt_setting.ini'
        if not os.path.exists(setting_path):
            input = open(setting_path, 'w')
            input.write('local_workspace_path:\n')
            input.write('ubuntu_workspace_path:\n')   
            input.write('bugdisp_path:\n')               
            input.close()   
        else:
            input = open(setting_path, 'r')
            localpath = input.readline()
            if 'local_workspace_path:' in localpath:
                localpath = localpath.replace('local_workspace_path:','')
                localpath = localpath.replace('\n','')
                self.localpath = str(localpath)
            ubuntupath = input.readline()
            if 'ubuntu_workspace_path:' in ubuntupath:
                ubuntupath = ubuntupath.replace('ubuntu_workspace_path:','')
                ubuntupath = ubuntupath.replace('\n','')
                self.remotepath = str(ubuntupath)  
            bugdisppath = input.readline()
            if 'bugdisp_path:' in bugdisppath:
                bugdisppath = bugdisppath.replace('bugdisp_path:','')
                bugdisppath = bugdisppath.replace('\n','')
                self.bugdisppath = str(bugdisppath)     
            input.close() 
                                        
    def setting(self, event):
        self.log('setting')  
        dlg = settingDialog(self.localpath, self.remotepath, self.bugdisppath, self.ubuntu_ip,
                            self.ubuntu_user, self.ubuntu_password, self.ubuntu_path)              
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.localpath = str(dlg.textCtrl_localpath.GetValue())
            self.remotepath = str(dlg.textCtrl_ubuntupath.GetValue())
            self.bugdisppath = str(dlg.textCtrl_bugdisppath.GetValue())
            self.ubuntu_ip = str(dlg.TextCtrl_ubuntuIP.GetValue())
            self.ubuntu_user = str(dlg.TextCtrl_username.GetValue())
            self.ubuntu_password = str(dlg.TextCtrl_password.GetValue())
            self.ubuntu_path = str(dlg.TextCtrl_workspace.GetValue())
            
            setting_path = 'colt_setting.ini'
            input = open(setting_path, 'w')

            input.write('local_workspace_path:' + self.localpath + '\n')
            input.write('remote_workspace_path:' + self.remotepath + '\n')   
            input.write('bugdisp_path:' + self.bugdisppath + '\n')   
            input.write('ubuntuIP:' + self.ubuntu_ip + '\n')   
            input.write('ubuntu_user:' + self.ubuntu_user + '\n')   
            input.write('ubuntu_password:' + self.ubuntu_password + '\n')   
            input.write('ubuntu_path:' + self.ubuntu_path + '\n')                                                               
            input.close()                
        dlg.Destroy()  
          
    def help(self, event):
        self.log('help ')                   

    def exit(self, event):
        self.log('exit ')  
        
[wxID_DIALOG1, wxID_DIALOG1BTN_BUGDISP, wxID_DIALOG1BTN_LOCALPATH, 
 wxID_DIALOG1BTN_UBUNTU, wxID_DIALOG1BUTTON3, wxID_DIALOG1BUTTON5, 
 wxID_DIALOG1STATICTEXT1, wxID_DIALOG1STATICTEXT2, wxID_DIALOG1STATICTEXT3, 
 wxID_DIALOG1TEXTCTRL_BUGDISPPATH, wxID_DIALOG1TEXTCTRL_LOCALPATH, 
 wxID_DIALOG1TEXTCTRL_UBUNTUPATH, 
] = [wx.NewId() for _init_ctrls in range(12)]

class settingDialog(wx.Dialog):
    def _init_ctrls(self):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=None,
              pos=wx.Point(489, 296), size=wx.Size(802, 441),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Setting')
        self.SetClientSize(wx.Size(784, 396))

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label=u'Local workspace path(main):', name='staticText2', parent=self,
              pos=wx.Point(32, 48),  style=0)
        self.textCtrl_localpath = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL_LOCALPATH,
              name=u'textCtrl_localpath', parent=self, pos=wx.Point(240, 56),
              size=wx.Size(400, 24), style=0, value=self.localpath)
        self.btn_localpath = wx.Button(id=wxID_DIALOG1BTN_LOCALPATH,
              label=u'Browse', name=u'btn_localpath', parent=self,
              pos=wx.Point(672, 56), size=wx.Size(87, 28), style=0)
        self.btn_localpath.Bind(wx.EVT_BUTTON, self.OnBtn_localpathButton,
              id=wxID_DIALOG1BTN_LOCALPATH)

        self.staticText3 = wx.StaticText(id=wxID_DIALOG1STATICTEXT3,
              label=u'Ubuntu workspace path(main):', name='staticText3', parent=self,
              pos=wx.Point(28, 120),  style=0)
        self.textCtrl_ubuntupath = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL_UBUNTUPATH,
              name=u'textCtrl_ubuntupath', parent=self, pos=wx.Point(240, 120),
              size=wx.Size(400, 24), style=0, value=self.remotepath)
        self.btn_ubuntu = wx.Button(id=wxID_DIALOG1BTN_UBUNTU, label=u'Browse',
              name=u'btn_ubuntu', parent=self, pos=wx.Point(672, 120),
              size=wx.Size(87, 28), style=0)        
        self.btn_ubuntu.Bind(wx.EVT_BUTTON, self.OnBtn_ubuntuButton,
              id=wxID_DIALOG1BTN_UBUNTU)
        
        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=u'Bugdisp path(wbugdisp.exe):', name='staticText1', parent=self,
              pos=wx.Point(40, 184),  style=0)
        self.textCtrl_bugdisppath = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL_BUGDISPPATH,
              name=u'textCtrl_bugdisppath', parent=self, pos=wx.Point(240, 184),
              size=wx.Size(400, 24), style=0, value=self.bugdisppath)
        self.btn_bugdisp = wx.Button(id=wxID_DIALOG1BTN_BUGDISP,
              label=u'Browse', name=u'btn_bugdisp', parent=self,
              pos=wx.Point(672, 184), size=wx.Size(87, 28), style=0)
        self.btn_bugdisp.Bind(wx.EVT_BUTTON, self.OnBtn_bugdispButton,
              id=wxID_DIALOG1BTN_BUGDISP)

        ubuntu_x = 20
        ubuntu_y = 250
        wx.StaticText(self,-1, 'Ubuntu IP', (ubuntu_x, ubuntu_y))
        self.TextCtrl_ubuntuIP = wx.TextCtrl(self, -1, self.ubuntuIP, (ubuntu_x+60, ubuntu_y), (100,25))
        wx.StaticText(self,-1, 'username', (ubuntu_x+180, ubuntu_y))
        self.TextCtrl_username = wx.TextCtrl(self, -1, self.ubuntuUser, (ubuntu_x+240, ubuntu_y), (100,25))
        wx.StaticText(self,-1, 'password', (ubuntu_x+360, ubuntu_y))
        self.TextCtrl_password = wx.TextCtrl(self, -1, self.ubunbuPass, (ubuntu_x+420, ubuntu_y), (100,25))
        wx.StaticText(self,-1, 'build.pl path', (ubuntu_x+540, ubuntu_y))
        self.TextCtrl_workspace = wx.TextCtrl(self, -1, self.ubuntu_path, (ubuntu_x+630, ubuntu_y), (100,25))
                                
        self.button5 = wx.Button(id=wx.ID_OK, label=u'OK', name='button5',
              parent=self, pos=wx.Point(136, 320), size=wx.Size(160, 28),
              style=0)
        self.button3 = wx.Button(id=wx.ID_CANCEL, label=u'Cancel',
              name='button3', parent=self, pos=wx.Point(512, 320),
              size=wx.Size(160, 28), style=0)        

    def __init__(self, localpath, ubuntupath, bugdisppath, ubuntuIP, ubuntuUser, ubunbuPass, ubuntu_path):
        self.localpath = localpath
        self.remotepath = ubuntupath
        self.bugdisppath = bugdisppath
        self.ubuntuIP = ubuntuIP
        self.ubuntuUser = ubuntuUser
        self.ubunbuPass = ubunbuPass
        self.ubuntu_path = ubuntu_path
        
        self._init_ctrls()

         
            
    def OnBtn_localpathButton(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.localpath = dlg.GetPath()
            self.textCtrl_localpath.Value = str(self.localpath)
        dlg.Destroy()        

    def OnBtn_ubuntuButton(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.remotepath = dlg.GetPath()
            self.textCtrl_ubuntupath.Value = str(self.remotepath)
        dlg.Destroy()        

    def OnBtn_bugdispButton(self, event):
        dlg = wx.FileDialog(self, "Choose bugdisp file:",
                            defaultFile="wbugdisp.exe",
                          style=wx.FD_DEFAULT_STYLE
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.bugdisppath = dlg.GetPath()
            self.textCtrl_bugdisppath.Value = str(self.bugdisppath)
        dlg.Destroy()     

            
if __name__ == '__main__':
#    startSSH()
#    transfer_files()
#    start_bugdisp()



    app = wx.PySimpleApp()
    frm = TestFrame()
    frm.Show()
    app.MainLoop()
    




