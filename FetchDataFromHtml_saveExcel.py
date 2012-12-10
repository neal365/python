# coding=gbk
'''
Created on 2012-8-29
@author: Neal Chen (njugui@gmail.com)
'''

import urllib
import sys
import datetime
from xlwt import Workbook
import time

'if keywords in the line, get data from > to </'
def getdata(keywords, line): 
    data = ''
    if keywords in line:
        start = line.find('>',)
        end = line.find('</', start)
        data = line[start+1:end]    
        return data   
    return False 
        

def FetchData():
    book = Workbook(encoding='gbk')
    sheet1 = book.add_sheet('Sheet 2')

    i = 0
    theday = datetime.date(2009,12,31)
    while i < 100:
        i += 1
        theday = theday + datetime.timedelta(days = 1)
        print theday
        theday_str = str(theday)       
        sheet1.write(i,0,theday_str)
        check_url = r'http://www.88888.com/date=' + theday_str
        try:
            checkfile = urllib.urlopen(check_url)  
        except Exception,e:
            print e
            return   
                   
        type = sys.getfilesystemencoding()     
        for line in checkfile:
            line = line.decode("UTF-8").encode(type)        
            date_west = getdata('date_west', line)  
            if date_west != False:
                sheet1.write(i,1,date_west)
            

    book.save('simple.xls')
    print 'finish!' 
                                                                                                  
if __name__ == '__main__':
    FetchData()