import os

path = r'D:\HOME\Music\iMusic'

''' use command ren *.tm3 *.mp3'''

for root, dirs, files in os.walk(path):
    for file in files:
        if '.tm3' in file:
            mp3_name = file.replace('.tm3', '.mp3')
            command = 'RENAME ' + root + '\\' + file + ' ' + mp3_name
            print command
            os.system(command)
            

        