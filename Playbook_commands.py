'''
PlayBook common commands
njugui@gmail.com
'''

import os
print "***Playbook commands***"


pb_ip = '169.254.0.1'
Simulator_IP = '1.1.1.1'
pb_pwd = 'pb_pwd'
csk_pwd = 'Playbook123'
store_pwd = 'Playbook123'
csj_name = 'client-RDK-1724868941.csj'
app_pin = 'nealchen'
p12_name = 'nealchen.p12'
android_sdk = r'"C:\Program Files\Android\android-sdk"'

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
 
def create_csk():
    shellCommand = r'blackberry-signer -cskdelete'
    if raw_input('Are you sure to delete old csk?') == 'y':
        os.system(shellCommand)
    shellCommand = r'blackberry-signer -csksetup -cskpass ' + csk_pwd
    os.system(shellCommand)

def register_csj():
    shellCommand = r'blackberry-signer -register -csjpin ' + app_pin
    shellCommand = shellCommand + r' -cskpass ' + csk_pwd + ' '
    shellCommand = shellCommand +  csj_name
    print shellCommand
    os.system(shellCommand)
            
def Create_p12():
    shellCommand = r'blackberry-keytool -genkeypair -keystore ' + p12_name
    shellCommand = shellCommand + r' -storepass ' + csk_pwd
    shellCommand = shellCommand +  r' -dname  "cn=' + app_pin + r'" -alias author'
    print shellCommand
    os.system(shellCommand)    
    
def apk2bar(apk):
#    shellCommand = 'apk2barVerifier ' + apk + ' ' + android_sdk
#    print shellCommand  
#    os.system(shellCommand)    
    shellCommand = 'apk2bar ' + apk + ' ' + android_sdk
    print shellCommand  
    os.system(shellCommand)    
    
def sign_bar(bar):
    shellCommand = r'blackberry-signer -cskpass ' + csk_pwd + r' -keystore ' + p12_name 
    shellCommand = shellCommand + r' -storepass ' + store_pwd + ' ' + bar + ' RDK'
    print shellCommand  
    os.system(shellCommand)
    shellCommand = r'blackberry-signer -keystore ' + p12_name + ' -storepass ' + store_pwd + ' ' +  bar + ' author'
    print shellCommand  
    os.system(shellCommand)    
    
def Create_apk_sign():
    shellCommand = r'keytool -genkey -v -keystore android.keystore -alias android -keyalg RSA -validity 20000'
    os.system(shellCommand)
#pwd 111111
 
def sign_apk(apk):
    signed_apk = apk.replace('.apk', '') + '_signed.apk'
    shellCommand = r'jarsigner -verbose -keystore android.keystore -signedjar '
    shellCommand = shellCommand + signed_apk + apk + ' android'
    os.system(shellCommand)    
        
def install_bar(bar):
    shellCommand = r'blackberry-deploy -installApp -password '
    shellCommand = shellCommand + pb_pwd + r' -device '
    shellCommand = shellCommand + pb_ip + r' -package '
    shellCommand = shellCommand + '\"' + bar +'\"'
    print shellCommand  
    os.system(shellCommand) 
    
def install_bar_simulator(bar):
    shellCommand = r'blackberry-deploy -installApp -password '
    shellCommand = shellCommand + 'playbook' + r' -device '
    shellCommand = shellCommand + Simulator_IP + r' -package '
    shellCommand = shellCommand + '\"' + bar +'\"'
    print shellCommand  
    os.system(shellCommand) 
            
if __name__ == '__main__':
    command_type = ''
    while command_type != 'quit' :
        print 'Please input command type: \n'
        print ''' 
        (1) apk to bar and sign and install 
        (2) install bar to Playbook
        (3) re-sign apk
        (4) create p12
        (5) install bar to simulator
        (6) apk to bar
        (7) Sign bar and install
        'quit' to quit
             '''
        command_type = raw_input()        
        if command_type == '1':
            apk_name = raw_input('Please input the apk name(not include .apk)\n')
            while not os.path.exists(apk_name+'.apk'):
                apk_name = raw_input('no %s ' % apk_name + 'found! please input again(not include .apk)\n')
            apk2bar(apk_name+'.apk')
            sign_bar(apk_name+'.bar')
            install_bar(apk_name+'.bar')
        elif command_type == '2':
            bar_name = raw_input('Please input the bar name(not include .bar)\n')
            while not os.path.exists(bar_name+'.bar'):
                bar_name = raw_input('no %s ' % bar_name + 'found! please input again(not include .bar)\n')
            install_bar(bar_name+'.bar')   
        elif command_type == '3':
            apk_name = raw_input('Please input the apk name(not include .apk)\n')
            while not os.path.exists(apk_name+'.apk'):
                apk_name = raw_input('no %s ' % apk_name + 'found! please input again(not include .apk)\n')
            sign_apk(apk_name+'.apk')           
        elif command_type == '4':
            create_csk()
            register_csj()
            Create_p12()
        elif command_type == '5':
            bar_name = raw_input('Please input the bar name(not include .bar)\n')
            while not os.path.exists(bar_name+'.bar'):
                bar_name = raw_input('no %s ' % bar_name + 'found! please input again(not include .bar)\n')
            install_bar_simulator(bar_name+'.bar')           
        elif command_type == '6':
            apk_name = raw_input('Please input the apk name(not include .apk)\n')
            while not os.path.exists(apk_name+'.apk'):
                apk_name = raw_input('no %s ' % apk_name + 'found! please input again(not include .apk)\n')
            apk2bar(apk_name+'.apk')
        elif command_type == '7':
            bar_name = raw_input('Please input the bar name(not include .bar)\n')
            while not os.path.exists(bar_name+'.bar'):
                bar_name = raw_input('no %s ' % bar_name + 'found! please input again(not include .bar)\n')
            sign_bar(apk_name+'.bar')
            install_bar(apk_name+'.bar')

    
    
            
        