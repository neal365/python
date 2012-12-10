#   -*-   coding:   cp936   -*-  
"""     Python Email Commander is powered by Python! 
        This application used Python2.5 standard library such as poplib,smtplib,email,Tkinter,Threading,subprocess.     
        Please sign up a free email account first, then prepare some batch files on your target PC. 
        After that, you can run this Application, and send commands to it anytime and anywhere!                            
Note: Command syntax should be [cmd]'command line'[/cmd]
------------------------------------
Author: Neal : njugui@gmail.com
Date:   2011-8-15
"""
import poplib
import smtplib
from email.mime.text import MIMEText
import time
import subprocess  
from threading import Thread   
import Queue 
from Tkinter import *  
    
class Email_Commander(object):

    def __init__(self, 
                POP3_server = 'pop.163.com',
                POP3_port = 110,
                SMTP_server = 'smtp.163.com',
                SMTP_port = 25,   
                USER_name = 'xxxx@163.com',
                USER_password = 'xxxx',
                RETRIEVE_interval = 60,
                LOG_file_path = 'email_command_log.txt',
                 ):
        self.POP3_server = POP3_server
        self.POP3_port = POP3_port
        self.SMTP_server = SMTP_server
        self.SMTP_port = SMTP_port
        self.USER_name = USER_name
        self.USER_password = USER_password
        self.RETRIEVE_interval = RETRIEVE_interval
        self.LOG_file_path = LOG_file_path
        self._runCommandResult = ""
        self.initialEmailCount = 0
        
    def startApp(self):
        self.POP3_server = self.entry_popServer.get()
        self.POP3_port = self.entry_popPort.get()
        self.SMTP_server = self.entry_smtpServer.get()
        self.SMTP_port = self.entry_smtpPort.get()
        self.USER_name = self.entry_userName.get()
        self.USER_password = self.entry_userPassword.get()
        self.RETRIEVE_interval = self.entry_retrieveInterval.get()
        
        self.log2Text('''Start listening your commands...\nPlease send [cmd] your command [/cmd] to me :) ''')
        
        thread_runApp = Thread(target=self._startApp,args=())
        thread_runApp.setDaemon(True)   
        thread_runApp.start()

    def _startApp(self):
        self.checkEmail_first()
        while True:
            time.sleep(float(self.RETRIEVE_interval))
            self.CheckEmailCommand()
            
    def quitApp(self):
        sys.exit()
                
    def checkLog(self):
        subprocess.call('notepad '+self.LOG_file_path)
        return

    def log2Text(self, str1):
        self.LOG_file = open(self.LOG_file_path, 'a')
        time_now = time.strftime("%b %d, %H:%M:%S", time.localtime())
        str1 = time_now + '-----' + str1 + '\n'
        self.LOG_file.write(str1)
        self.text_log.insert(END, str1)   
        self.LOG_file.close() 
    
    def generateCommand(self, str1):
        'Search [cmd] and [/cmd] from string, then return the command line'
        if (not r'[cmd]' in str1) or (not r'[/cmd]' in str1):
            self.log2Text( "No Command or bad command syntax!!")
            return ''
        str1 = str1.replace('[cmd]your command[/cmd]', '')
        startPoint = str1.find('[cmd]')+5
        endPoint = str1.find('[/cmd]')
        
        return str1[startPoint:endPoint]

    def runCommand(self, shellCommand):
        myQueue = Queue.Queue(1)
        myQueue.put(self._runCommandResult)
        thread_runCommand = Thread(target=self._runCommand, args=(shellCommand,))
        thread_runCommand.setDaemon(True)
        thread_runCommand.start()
        myQueue.get(self._runCommandResult)
    
    def _runCommand(self, shellCommand):
        try:
            result = subprocess.call(shellCommand)
            self._runCommandResult  = "Executed finished! result is %s"%result
        except Exception, e:
            self._runCommandResult  =  "Your Command cannot be execute! Error is : " + str(e)
        self.log2Text(self._runCommandResult)

    def getSender(self, str1):
        "Search sender from string, by searching 'From: <>' "
        if not 'From:' in str1:
            self.log2Text( "Cannot find sender!!")
        startPoint = str1.find(r"'From:")
        startPoint = str1.find('<',startPoint)
        endPoint = str1.find('>',startPoint)
        return str1[startPoint+1:endPoint]

    def checkEmail_first(self):
        try:
            pop_client = poplib.POP3(self.POP3_server, self.POP3_port)
            pop_client.user(self.USER_name)
            pop_client.pass_(self.USER_password)
        except Exception,e:
                self.log2Text( "POP client connect error: %s " % str(e))
                return
        
        self.initialEmailCount =  pop_client.stat()[0]   
        pop_client.quit()
                
    def CheckEmailCommand(self):
        try:
            pop_client = poplib.POP3(self.POP3_server, self.POP3_port)
            pop_client.user(self.USER_name)
            pop_client.pass_(self.USER_password)
        except Exception,e:
                self.log2Text( "POP client connect error: %s " % str(e))
                return
        
        email_count = pop_client.stat()[0]       
        if email_count == self.initialEmailCount or email_count < self.initialEmailCount:
            self.log2Text( "No new emails received!!")
            pop_client.quit()
            return
        newEmail_count = email_count-self.initialEmailCount   
        self.log2Text("Received %d new emails!" % newEmail_count)
        for index in range(0, newEmail_count):          
            mailContent = str(pop_client.retr(self.initialEmailCount + index + 1))
            sender = self.getSender(mailContent)    
            self.log2Text( "No %d new email is from [%s]"%(index+1,sender))              
            cmd = self.generateCommand(mailContent)          
            self.log2Text( "command is [%s] " % cmd)
            if cmd != '':
                self.SendEmail(sender, subject="Your command [%s] is executing!" % cmd)
                self.runCommand(cmd)
                print self._runCommandResult
                self.SendEmail(sender, subject="Your command [%s] has been executed!"%cmd, content=" result is ''%s''"%self._runCommandResult)
            else:
                self.SendEmail(sender, r"Please send [cmd]your command[/cmd] to me :)")        
        self.initialEmailCount = email_count
        pop_client.quit()

    def SendEmail(self, target, subject=None, content=None, attach=None):
        try:
            smtp_client = smtplib.SMTP(self.SMTP_server, self.SMTP_port)
            smtp_client.login(self.USER_name, self.USER_password)
        except Exception,e:
            self.log2Text( "SMTP client connect error: %s " % str(e))
            pass
            
        message = MIMEText(content)
        message['Subject'] = subject
        message['From'] = self.USER_name
        message['To'] = target
        
        try:
            smtp_client.sendmail(self.USER_name, target, message.as_string())
            self.log2Text( "Email sent success!")
        except Exception,e:
            self.log2Text( "Email sent error! Error code is : %s " % str(e))
            pass
        smtp_client.close()
   
    def sendFeedback(self):
        self.SendEmail('njugui@gmail.com', "EmailCommander Feedback", self.text_email.get(1.0,END))   

    def getUpdate(self):
        return
    
    def about(self):
        root = Tk()
        root.title('About: Python Email Commander')
        
        Label(root, text='About Python Email Commander').pack()
        text_about = Text(root,height=10, width=50,bg='gray')
        text_about.insert(END, "Python Email Commander is powered by Python! \n")
        text_about.insert(END, "This application used Python2.5 standard library such as poplib,smtplib,email,Tkinter,Threading,subprocess.\n")      
        text_about.insert(END, "Please sign up a free email account first, then prepare some batch files on your target PC. \n")
        text_about.insert(END, "After that, you can run this Application, and send commands to it anytime and anywhere!\n")                             
        text_about.pack()
        
        Label(root, text='Your feedback').pack()                  
        self.text_email = Text(root,height=10, width=50)
        self.text_email.insert(END, 'You can send feedback to me(njugui@gmail.com) if you like it or hate it +_+ :\n')
        self.text_email.pack()
        
        frame1 = Frame(root)
        Button(frame1, text='Send feedback', command=self.sendFeedback).pack(side='left')
        Button(frame1, text='Get update', command=self.getUpdate).pack(side='left')
        Button(frame1, text='Exit', command=root.destroy, fg='red').pack(side='left')
        frame1.pack()
                
        mainloop()        
        return
    
    def clientGUI(self):
        root = Tk()
        root.title('Python Email Commander')
    
        'frame 1'
        frame1 = Frame(root)
        Label(frame1, text='POP3 server').pack(side='left')
        e = StringVar()
        self.entry_popServer = Entry(frame1, textvariable=e)
        e.set(self.POP3_server)
        self.entry_popServer.pack(side='left')
    
        Label(frame1, text='POP3 port').pack(side='left')
        e = StringVar()
        self.entry_popPort = Entry(frame1, textvariable=e)
        e.set(self.POP3_port)
        self.entry_popPort.pack(side='left')
        frame1.pack()
    
        'frame 2'
        frame2 = Frame(root)
        Label(frame2, text='SMTP server').pack(side='left')
        e = StringVar()
        self.entry_smtpServer = Entry(frame2, textvariable=e)
        e.set(self.SMTP_server)
        self.entry_smtpServer.pack(side='left')
    
        Label(frame2, text='SMTP port').pack(side='left')
        e = StringVar()
        self.entry_smtpPort = Entry(frame2, textvariable=e)
        e.set(self.SMTP_port)
        self.entry_smtpPort.pack(side='left')
        frame2.pack()
    
        'frame 3'
        frame3 = Frame(root)
        Label(frame3, text='User Email').pack(side='left')
        e = StringVar()
        self.entry_userName = Entry(frame3, textvariable=e)
        e.set(self.USER_name)
        self.entry_userName.pack(side='left')
    
        Label(frame3, text='Password').pack(side='left')
        e = StringVar()
        self.entry_userPassword = Entry(frame3, textvariable=e)
        e.set(self.USER_password)
        self.entry_userPassword.pack(side='left')
        frame3.pack()
        
        'frame 4'
        frame4 = Frame(root)
        Label(frame4, text='Retrieve interval(second)').pack(side='left')
        e = StringVar()
        self.entry_retrieveInterval = Entry(frame4, textvariable=e)
        e.set(self.RETRIEVE_interval)
        self.entry_retrieveInterval.pack(side='left')
        frame4.pack()    
        
        'frame 5'    
        frame5 = Frame(root)
        button_quit = Button(frame5, text='Quit', command=self.quitApp, fg='red')
        button_quit.pack(side = 'left')
            
        button_run = Button(frame5, text='Start', command=self.startApp, fg='blue')
        button_run.pack(side = 'left')
        
        button_checkLog = Button(frame5, text='Log', command=self.checkLog)
        button_checkLog.pack(side = 'left')    
        
        button_about = Button(frame5, text='About', command=self.about)
        button_about.pack(side = 'left')            
        
        frame5.pack()
        
        'frame 6'    
        frame6 = Frame(root)
        self.text_log = Text(frame6)
        self.text_log.pack(side='left')
        
        scrollbar_log = Scrollbar(frame6)
        scrollbar_log.pack(side='left', fill=Y)
        self.text_log['yscrollcommand']=scrollbar_log.set
        scrollbar_log['command'] = self.text_log.yview()  
        frame6.pack()  
          
        mainloop()
    
    
if __name__ == '__main__':      
    emailCommander = Email_Commander()
    emailCommander.clientGUI()
    
    
    