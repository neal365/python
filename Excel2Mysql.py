# coding=gbk
'''
Created on 2012-8-29

@author: neal
'''
import MySQLdb
from xlrd import open_workbook,cellname

try:
    book = open_workbook('360data.xls')
    sheet = book.sheet_by_index(0)
except Exception,e:
    print 'Open excel failed!!!'
 
try:
    conn=MySQLdb.connect(host='localhost',user='user',passwd='password',port=3306, charset='gb2312')
    conn.select_db('db')
    cur=conn.cursor()

    for row_index in range(0, sheet.nrows):
        value = ''
        for i in range(0,8):
            value = value + '\'' + str(sheet.cell(row_index, i).value) + '\',' 
        value += '\'' + str(sheet.cell(row_index, 8).value) + '\')'
        print value
        cur.execute('INSERT INTO  `data1` VALUES (' + value)
        print 'insert %d complete!\n' % row_index
    conn.commit()
    cur.close()
    conn.close()
    print 'mysql finish!'

except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])