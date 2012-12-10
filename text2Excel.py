'''
Put numbers of text to excel!

Created on Dec 10, 2012

@author: njugui@gmail.com

'''
from xlwt import Workbook

def readFile2Excel():
    fileInput = open('wisdom.txt','r')
    content = fileInput.read()
    book = Workbook(encoding='utf-8')
    sheet1 = book.add_sheet('Sheet1')
    
    start_pos = 0
    end_pos = -1    
    for i in range(2, 301):
        i_str = str(i)
        if len(i_str) == 1:
            i_str = '00' + i_str
        if len(i_str) == 2:
            i_str = '0' + i_str        
        print i_str
        end_pos = content.find(i_str, start_pos)
        str1 = content[start_pos : end_pos]
        sheet1.write(i,1,str1)
        start_pos = end_pos
    book.save('simple.xls')
    fileInput.close()

if __name__ == '__main__':
    readFile2Excel()