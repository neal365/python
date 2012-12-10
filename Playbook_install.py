'''
Install bars automatically one or batch
njugui@gmail.com
'''

import os
print "***Playbook Installation tool***"


pb_ip = '169.254.0.1'
pb_pwd = 'qqww'


def Install_all_bars():
    applist = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if '.bar' in file:
                barfile = root + '\\' + file
                applist.append(barfile)
    print applist
    i = 0    
    for app in applist:
        i = i+1 
        print 'Ready to install No.%d(in %d) app: \n' % (i,len(applist))
        shellCommand = 'blackberry-deploy -installApp -password '
        shellCommand = shellCommand + pb_pwd
        shellCommand = shellCommand + ' -device '
        shellCommand = shellCommand + pb_ip
        shellCommand = shellCommand + ' -package '
        shellCommand = shellCommand + '\"' + app +'\"'
        print shellCommand
        os.system(shellCommand)
    print 'Install finish!'       
 
   
def install_bar(bar):
    shellCommand = r'blackberry-deploy -installApp -password '
    shellCommand = shellCommand + pb_pwd + r' -device '
    shellCommand = shellCommand + pb_ip + r' -package '
    shellCommand = shellCommand + '\"' + bar +'\"'
    print shellCommand  
    os.system(shellCommand) 
    
            
if __name__ == '__main__':
    command_type = ''
    while command_type != 'quit' :
        print 'Please input command type: \n'
        print ''' 
        (1) Install 1 bar; 
        (2) Install all bars;
        'quit' to quit
             '''
        command_type = raw_input()        
        if command_type == '1':
            bar_name = raw_input('Please input the bar name(not include .bar)\n')
            while not os.path.exists(bar_name+'.bar'):
                bar_name = raw_input('no %s ' % bar_name + 'found! please input again(not include .bar)\n')
            install_bar(bar_name+'.bar')   
        elif command_type == '2':
            Install_all_bars()

    
    
            
        