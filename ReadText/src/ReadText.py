#-*- coding: gbk -*-
'''
Created on Nov 2, 2011

@author: Neal : njugui@gmail.com
'''
import Tkinter
import os
import winsound
import pyaudio
import wave

if (os.path.exists("not_check_list.txt")):
    NotCheckList = open("not_check_list.txt", "a+")
else:
    NotCheckList = open("not_check_list.txt", "w+")
    
words_not_check = NotCheckList.readlines()


class cReadText(object):
    def __init__(self):
        self.Sound_path = r'C:\chenguichun\workspace\ReadText\sound' 
        self.wav = 'sound.wav'
        self.flag_dualword = True
        
        self.UI()
        
    def UI(self):
        self.root = Tkinter.Tk()
        self.root.title('Text Reader')
        self.text_input = Tkinter.Text(master=self.root, width=30, height=10)
        self.text_input.pack()
        self.text_input.insert(Tkinter.END, u"我是谁")
        button_input = Tkinter.Button(master=self.root, text='Read them!', width=30, height=3, command=self.ReadText)
        button_input.pack()
        
        self.status  = Tkinter.StringVar()
        self.label_status = Tkinter.Label(master=self.root, width=30,textvariable=self.status, height=3, fg='red')
        self.label_status.pack()
        frame0 = Tkinter.Frame(master=self.root)
        self.newword  = Tkinter.StringVar()
        self.label_word = Tkinter.Label(master=frame0, textvariable=self.newword, width=2, height=3, font=("Helvetica", 40), wraplength=1)
        self.label_word.pack(side='left')
        self.button_record = Tkinter.Button(master=frame0, state=Tkinter.DISABLED, text='Record NewWord', width=20, height=1, command=lambda:self.RecordNewword(self.NewwordPath))
        self.button_record.pack()
        self.button_change = Tkinter.Button(master=frame0, state=Tkinter.DISABLED, text='Change NewWord', width=20, height=1, command=self.ChangeNewword)
        self.button_change.pack(side='right')
        frame0.pack()
        
        self.root.mainloop()
    
    def wordExist(self, word):
        path = self.Sound_path + '\\' + word +'.wav'
        if os.path.exists(path):
            self.wordPath = path
            print path + ' Exists!'
            return True
        else:
            self.NewwordPath = path
            return False
        
    def ReadText(self):
        text = self.text_input.get(1.0, Tkinter.END)        
        self.RecordNewword(self.wav)
        self.wavfiles = []
        
        i = 0
        while( i <= len(text)-2):
            if(self.flag_dualword and i!=len(text)-2):  #Try dual words first
                word = text[i]+text[i+1]
                wordCode = word +'\n'
                if (wordCode in words_not_check):
                    print 'word not check'
                    self.flag_dualword=False
                while(1):        
                    if(self.wordExist(word)): #Read word existed
                        self.wavfiles.append(self.wordPath)
                        i=i+2
                        break
                    else:                   #Record new word
                        self.status.set('New word found!')
                        self.newword.set(word)
                        self.button_change.config(state = Tkinter.NORMAL)
                        self.button_record.config(state = Tkinter.NORMAL)
                        self.label_word.update() 
                        if(not self.flag_dualword):
                            break
            else:    
                word = text[i]                 
                while(1):             
                    if(self.wordExist(word)): #Read word existed
                        self.wavfiles.append(self.wordPath)
                        i=i+1
                        self.flag_dualword = True
                        break
                    else:                   #Record new word
                        self.status.set('New word found!')
                        self.newword.set(word)
                        self.button_change.config(state = Tkinter.NORMAL)
                        self.button_record.config(state = Tkinter.NORMAL)                        
                        self.label_word.update() 
        print self.wavfiles
        self.CombineWavs(self.wavfiles)
        self.PlayWav()
        self.status.set('Read complete!')
        self.newword.set('')

#        self.label_word.update()
   
    def PlayWav(self):
        winsound.PlaySound(self.wav, winsound.SND_FILENAME) 
        
    def ReadWord(self):
        winsound.PlaySound(self.wordPath, winsound.SND_FILENAME) 
         
    def CombineWavs(self, wavfiles):
        for infile in wavfiles:
            self.Combine2wav(self.wav, infile)        

    def Combine2wav(self, wav1, wav2):
        outfile = self.wav 
        data= []
        w = wave.open(wav1, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()          
        w = wave.open(wav2, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()     
        output = wave.open(outfile, 'wb')
        output.setparams(data[0][0])
        output.writeframes(data[0][1])
        output.writeframes(data[1][1])
        output.close()
                
        
    def RecordNewword(self, FilePath):
        self.button_change.config(state = Tkinter.DISABLED)
        self.button_record.config(state = Tkinter.DISABLED)        
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 10000
        RECORD_SECONDS = 1
        WAVE_OUTPUT_FILENAME = FilePath 
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)
        
        print "* recording"
        all = []
        for i in range(0, RATE / chunk * RECORD_SECONDS):
            data = stream.read(chunk)
            all.append(data)
        print "* done recording"
        
        stream.close()
        p.terminate()
        
        # write data to WAVE file
        data = ''.join(all)
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()      

    def ChangeNewword(self):
        self.button_change.config(state = Tkinter.DISABLED)
        self.button_record.config(state = Tkinter.DISABLED)  
        self.flag_dualword = False
        newline = str(self.newword.get())+'\n'
        print newline
        NotCheckList.write(newline)
        print 'Change to one word only'
        
if __name__ == '__main__':
    app = cReadText()
    
