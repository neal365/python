'''
Download builds from server automatically.
Neal : njugui@gmail.com
'''

import urllib
import os
import time
import Tkinter

class download_build(object):
    
    def __init__(self):       
        self.Latest_bundle_9788 = 3068
        self.Latest_os_9788 = 713
        self.log_file = open('download_build_log.txt', 'w')

    def Log2Text(self,str):
        print str
        str = str + '\n'
        self.log_file.write(str)
    
    def Copy_upzip(self, os_folder, bundleFolder, os_name, cp_name):
        if(os.path.exists(bundleFolder)):
            self.Log2Text( 'Bundle %s exist!' % bundleFolder)
            return
        else:
            cp_folder = os_folder + "UMP\\signed_jvms\\"
            os.system('MD '+ bundleFolder)  #Create bundle folder
            os.system('robocopy ' + cp_folder + ' ' + bundleFolder + ' ' + cp_name + ' /Z /NJH /NJS /NS /NC /NDL ')
            os.system('robocopy ' + os_folder + ' ' + bundleFolder + ' ' + os_name + ' /Z /NJH /NJS /NS /NC /NDL ')
            os.system(r'gzip -d -f -q ' + bundleFolder + cp_name)
            os.system(r'gzip -d -f -q ' + bundleFolder + os_name)
            self.create_bat_file(bundleFolder, os_name, cp_name)
            self.Log2Text('new build %s copied!' % bundleFolder)

    def create_bat_file(self, bundleFolder, os_name, cp_name):
        flash_bat = open(bundleFolder+'flash.bat', 'w')
        os_name_sfi = os_name.replace('.gz','')
        cp_name_sfi = cp_name.replace('.gz','')
        flash_bat.write('cfp -u wipe \n')
        flash_bat.write('cfp -u load ' + cp_name_sfi + ' ' + os_name_sfi + '\n')
        flash_bat.write('PAUSE')
                
    def check_url_exist(self, os_url):
        try:
            urllib.urlopen(os_url)
            return True    
        except Exception,e:
#            self.Log2Text(str(e))
            self.Log2Text('--%s not exist '% os_url)
            return False 
        
      
    def check_9788_ChinaMobile(self):
        os_name = '9788.sfi.gz'
        cp_name = '9788-signed.sfi.gz'     
        bundle = self.Latest_bundle_9788 -1   
        while bundle<self.Latest_bundle_9788+20:
            bundle += 1
            osVer = self.Latest_os_9788 -1
            while osVer < self.Latest_os_9788 + 10:
                osVer += 1  
#        for bundle in range(self.Latest_bundle_9788, self.Latest_bundle_9788+20, 1):        
#            for osVer in range(self.Latest_os_9788,self.Latest_os_9788+10, 1):
                url = r'\\serverpath'
                os_folder = url + str(osVer) + '_bundle' + str(bundle)+'\\'
                os_url = os_folder + os_name
                bundleFolder = '9788_ChinaMobile_Bundle'+str(bundle)+'\\'
                if self.check_url_exist(os_url):
                    self.Copy_upzip(os_folder, bundleFolder, os_name, cp_name)     
                    self.Latest_bundle_9788 = bundle
                    self.Latest_os_9788 = osVer
                    break                                
        self.Log2Text( 'Check 9788 ChinaMobile new bundle complete!')        
        self.Log2Text( time.strftime ("2011-%m-%d %H:%M:%S", time.localtime()))
        
if __name__ == '__main__':
    test = download_build()
#    while(1):
#        test.check_9788_ChinaMobile()
#        time.sleep(300)
        
            