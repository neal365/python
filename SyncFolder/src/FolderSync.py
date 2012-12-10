# FolderSync.py
#-*- coding: cp936 -*-
'''
Author: Neal  njugui@gmail.com
Date: 2011-7-12
The module is for synchronizing mobileHDD folder and local folder.
This module is run from mobileHDD folder.
'''

import os
import time
import filecmp
import shutil

g_mobileFolder = (
                  R"J:\A\B\Contacts",#1
                  R"J:\A\B\Favorites",#2
                  R"J:\A\B\workspace"
                  )
g_localFolder = (
                 R"C:\Users\Administrator\Contacts",#1
                 R"C:\Users\Administrator\Favorites",#2
                 R"C:\Users\Administrator\workspace"
                 )


def syncFolders(mobileFolder, localFolder, skipFolder = None):
    if os.path.exists(mobileFolder) == False:
        print mobileFolder + "dose not exists!!!"
        return -1
    if os.path.exists(localFolder) == False:
        print localFolder + "dose not exists!!!"
        return -1    
    skip_path = os.path.join(localFolder, skipFolder)
    for root, dirs, files in os.walk(localFolder):    
        if root == skip_path: #do nothing with skip folder
            break     
        local_path = root;
        relative_path = os.path.relpath(root, localFolder)
        if relative_path == ".":
            mobile_path = mobileFolder
        else:
            mobile_path = os.path.join(mobileFolder, relative_path)
        #print "relative_path = " + relative_path
        #print "---mobile_path = " + mobile_path
        """ If Moblie folder has the same sub-folder, compare their files;
            Else, just copy sub-folder to Mobile folder;
        """        
        if os.path.exists(mobile_path):#mobile has the folder with same name
            for f in files:
                local_file = os.path.join(local_path, f)
                mobile_file = os.path.join(mobile_path,f) 
                """ If Mobile folder has the same file name, compare the file attribute;
                    If the files are same, do nothing; 
                    Else, replace with local file;
                """
                if os.path.exists(mobile_file)== True:#mobile has the file with same name                 
                    if filecmp.cmp(local_file, mobile_file) == False:#same file with different version
                        if os.stat(local_file).st_mtime > os.stat(mobile_file).st_mtime:#local file is newer        
                            #Use shell command to replace the file
                            shellCommand = "REPLACE \"" + local_file + "\" \"" + mobile_path + "\" /U /R"
                            print "Command: " + shellCommand
                            os.system(shellCommand)                          
                            #shutil.copy(local_file, mobile_path)
                            print "[==========updated==========] The file " + mobile_file + " has updated!!! "
                        elif os.stat(local_file).st_mtime < os.stat(mobile_file).st_mtime:#mobile file is newer        
                            #Use shell command to replace the file
                            shellCommand = "REPLACE \"" + mobile_file + "\" \"" + local_path + "\" /U /R"
                            print "Command: " + shellCommand
                            os.system(shellCommand)                          
                            #shutil.copy(mobile_file, local_path)
                            print "[==========updated==========] The file " + local_file + " has updated!!! "                          
                else:#mobile doesn't have the file
                    #Use shell command to copy the file
                    shellCommand = "REPLACE \"" + local_file + "\" \"" + mobile_path + "\" /A /R"
                    print "Command: " + shellCommand
                    os.system(shellCommand)                    
                    #shutil.copy(local_file, mobile_path)
                    print "[++++++++++newFile++++++++++] The file " + mobile_file + " has added!!! "
        else:#mobile doesn't have the folder
            #Use shell command to copy the folder
            shellCommand = "XCOPY \"" + local_path + "\" \"" + mobile_path + "\" /E /I /C /H /R"
            os.system(shellCommand)
            print "Command: " + shellCommand
            #shutil.copytree(local_path, mobile_path,symlinks=False)
            print "[++++++++++newFolder++++++++++] The Folder " + mobile_path + " has added!!! "
    return 0

"""----------------------------Main-----------------------------------"""
print "~~~~~~~~~~~~~~~~~~~~~~Synchronization begins~~~~~~~~~~~~~~~~~~~~~~~~~~" 
print time.strftime("%b %d, %H:%M:%S", time.localtime())

for i in range(len(g_mobileFolder)):   
    if syncFolders(g_mobileFolder[i], g_localFolder[i]) == 0:
        print g_mobileFolder[i] + "Synchronization from LOCAL to MOBILE has complete!!!"
        print time.strftime("%b %d, %H:%M:%S", time.localtime())
    if syncFolders(g_localFolder[i], g_mobileFolder[i]) == 0:
        print g_localFolder[i] + "Synchronization from MOBILE to LOCAL has complete!!!"
        print time.strftime("%b %d, %H:%M:%S", time.localtime())    
        
"""----------------------------End-----------------------------------"""
    
    




