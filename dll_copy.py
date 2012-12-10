import os

for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if '.dll' in file:
            dllfile = root + '\\' + file
            command = 'XCOPY ' + dllfile + ' dll'
            os.system(command)

for files in os.walk(os.getcwd()):
    for ff in files:
        for f in ff:
            if '.dll' in f:
                folder = f.replace('.dll','')
                folderpath = 'dll\\' + folder + '\\Debug'
                command = 'MD ' + folderpath + ' /D'
                os.system(command)
                command = 'XCOPY ' + f + ' ' + folderpath + ' /D'
                os.system(command)        
            
        