import os
print "***batch change file name ***"

for files in os.walk(os.getcwd()):
    for file_list in files:
        i = 1
        for file_name in file_list:
            if '.avi' in file_name:
                os.system('rename ' + file_name + ' ' + str(i) + '.avi')
                i += 1
