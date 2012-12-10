# coding=gbk
"""-----------------------------------------------------------------------------
#  Module Name          :  AT Log
#
#  Description          :  Implement logging function
#    
#  Author               :  
#
#  --------------------------  Revision History  -------------------------------
# 2011-8-1       njugui@gmail.com      created     
#                                       
#----------------------------------------------------------------------------"""
import logging
import os
import time

logger=logging.getLogger()
logFile = os.getcwd()+'\\at_test_log.txt'
if os.path.exists(logFile):
    os.remove(logFile)
handler=logging.FileHandler(logFile)    #use present root as logging root
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

def log(message, level='INFO'):
    print message
    message ='\n [LOG_' + level + ']' + time.strftime("%b %d, %H:%M:%S", time.localtime()) + '\n' + message          
    if level == 'INFO':
        logger.info(message)
    elif level == 'ERROR':
        logger.error(message)
    elif level == 'CRITICAL':
        logger.critical(message)
    elif level == 'WARNING':
        logger.warning(message)    
    elif level == 'DEBUG':
        logger.debug(message)     
    else:
        logger.info(message)   
        
    
    
    
    
    