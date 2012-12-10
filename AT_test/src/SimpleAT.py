from Tkinter import *
import time
import serial


class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.atSerial = serial.Serial()
        self.atSerial.port = "COM4"
        self.atSerial.baudrate = 115200
        self.atSerial.timeout = 2        
        self.createWidgets()
        self.title="Simple AT commands"
        self.isSerialOpen = False
        self.pack()        
                                 
    def OpenSerial(self):
        if not self.isSerialOpen:
            try:
                self.atSerial.port = self.entry_port.get()
                self.atSerial.open()
                self.isSerialOpen = True
                self.text_log.delete(1.0,END)
                self.text_log.insert(END, 'Serial Open success!')
                self.btnRadionON.config(state = NORMAL)
                self.btnRadioOFF.config(state = NORMAL)
                self.btnCsCall.config(state = NORMAL)
                self.btnPsAct.config(state = NORMAL)
                self.btnPsDea.config(state = NORMAL)
                self.btnManuPlmn.config(state = NORMAL)
                self.btnATA.config(state = NORMAL)
                self.btnATH.config(state = NORMAL)
                self.btnCloseSerial.config(state = NORMAL)
                self.textAT.config(state = NORMAL)
                self.textAT.insert(END, 'Input your other AT Commands here') 
                self.btnOpenSerial.config(state = DISABLED)
            except Exception, e:
                self.printLogs(  'Serial Open Fail!')
                self.printLogs(str(e))
                self.isSerialOpen = False            
        else:
            self.printLogs(  'Serial is opening!')
            
    def RadioOn(self):
        self.atSerial.write("at+cfun=1 \r")
        time.sleep(5)
        self.printLogs(  "at+cfun=1 sent!")
                
    def RadioOff(self):
        self.atSerial.write("at+cfun=0 \r")
        time.sleep(5)
        self.printLogs(  "at+cfun=0 sent!")

    def callNum(self):
        self.atSerial.write("atd123456; \r")
        time.sleep(5)
        self.printLogs(  "atd123456; sent!")
        
    def pdpActivate(self):
        self.atSerial.write("at+cgdcont=1,\"ip\",\"ghijk\",\"200.1.1.90\",0,0 \r")

        self.atSerial.write("at+cgeqreq=1,2,64,64,,,320,\"ie4\",\"ie5\",1,,3 \r")

        self.atSerial.write("at+cgact=1,1 \r")
        time.sleep(5)
        self.printLogs(  "at+cgact=1,1 sent!")
 
    def cManualPLMN(self):
        self.atSerial.write("at+cops=1,2,\"%s\",2 \r" % self.entry_plmn.get())
        self.printLogs(  'AT+COPS=1,2,\"%s\",2 sent!'%self.entry_plmn.get())

    def cPSdeactivate(self):
        self.atSerial.write("at+cgact=0,1 \r")
        self.printLogs(  'at+cgact=0,1 sent!')

    def cATA(self):
        self.atSerial.write("ata \r")
        self.printLogs(  'ATA sent!')
    def cATH(self):
        self.atSerial.write("ath \r")
        self.printLogs(  'ATH sent!')
                
    def CloseSerial(self):
        try:
            self.atSerial.close()
            self.isSerialOpen = False
            self.printLogs('Serial close success!')
            self.btnOpenSerial.config(state = NORMAL)
            self.btnRadionON.config(state = DISABLED)
            self.btnRadioOFF.config(state = DISABLED)
            self.btnCsCall.config(state = DISABLED)
            self.btnPsAct.config(state = DISABLED)
            self.btnPsDea.config(state = DISABLED)
            self.btnManuPlmn.config(state = DISABLED)
            self.btnATA.config(state = DISABLED)
            self.btnATH.config(state = DISABLED)
            self.textAT.config(state = DISABLED)
            self.btnCloseSerial.config(state = DISABLED)
        except Exception, e:
            self.printLogs(str(e))  
            
    def printLogs(self, log):
        log = log + '\n' 
        self.text_log.delete(1.0,END)
        self.text_log.insert(END, log)
        if self.atSerial.isOpen():
            serialLog = self.atSerial.readall()
        if self.atSerial.isOpen():
            if serialLog == '':
                self.text_log.insert(END, 'No response! Maybe you didnot start RimSerial!') 
            self.text_log.insert(END, serialLog) 
        self.text_log.yview_moveto(100.0)
        print log
        
    def AtButton1(self, event):
        self.textAT.delete(1.0,END)
        
    def Atkeypress(self, event):
#        print "pressed", repr(event.char)    
        if event.char=='\r':
            self.atSerial.write(self.textAT.get(1.0,END))
            self.printLogs(self.textAT.get(1.0,END)+'Sent!') 
            self.textAT.insert(END, 'Input your other AT Commands here, then press Enter to send')             
              
    def createWidgets(self):
        Label(width=21, wraplength=200, fg='red', text="Please open Rimserial first, then press OpenSerial").pack()
        frame0 = Frame(width=21)
        e = StringVar()
        self.entry_port = Entry(master=frame0, textvariable=e, width=5)
        e.set('COM4')
        self.btnOpenSerial = Button(master=frame0, width=15, text='OpenSerial',  command=self.OpenSerial)
        self.btnRadionON = Button(state=DISABLED, width=21, text='RadioOn',  command=self.RadioOn)       
        self.btnRadioOFF = Button(state=DISABLED, width=21, text='RadioOff',  command=self.RadioOff)        
        self.btnCsCall = Button(state=DISABLED, width=21, text='CS call',  command=self.callNum)
        self.btnPsAct = Button(state=DISABLED, width=21, text='PS pdpActivate',  command=self.pdpActivate)
        frame1 = Frame(width=21)
        e = StringVar()
        self.entry_plmn = Entry(master=frame1, textvariable=e, width=5)
        e.set("00101")        
        self.btnManuPlmn = Button(state=DISABLED, master=frame1, text='ManualPLMNSearch',  command=self.cManualPLMN)   
        self.btnPsDea = Button(state=DISABLED, width=21, text='PDP deactivate',  command=self.cPSdeactivate) 
        self.btnATA = Button(state=DISABLED, width=21, text='ATA',  command=self.cATA)
        self.btnATH = Button(state=DISABLED, width=21, text='ATH',  command=self.cATH)
        self.textAT = Text(state=DISABLED, width=20, height=3)
        self.textAT.bind('<Key>', self.Atkeypress)
        self.textAT.bind('<Button-1>', self.AtButton1)
        self.btnCloseSerial = Button(state=DISABLED, width=21, text='CloseSerial',  command=self.CloseSerial)
        self.text_log = Text(width=20, height=5, bg='GRAY')
        self.text_log.insert(END, 'Check logs here!')
     
        
        self.entry_port.pack(side='right')
        self.btnOpenSerial.pack(side='left')
        frame0.pack()
        self.btnRadionON.pack()
        self.btnManuPlmn.pack(side='left')
        self.entry_plmn.pack(side='right')
        frame1.pack()
        self.btnRadioOFF.pack()
        self.btnCsCall.pack()
        self.btnATH.pack()
        self.btnATA.pack()
        self.btnPsAct.pack()
        self.btnPsDea.pack()
        self.textAT.pack() 
        self.btnCloseSerial.pack()
        self.text_log.pack()   
                        
root = Tk()
root.title ('AT Commands')
app = Application(master=root)
mainloop()
