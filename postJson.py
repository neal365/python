'''
Created on 2013-7-10

@author: Administrator
'''
import httplib
import json
import serial
import sys
serial = serial.Serial()
serial.baudrate = 9600
serial.port = 24
serial.timeout = 2
try:
    serial.open()
    print "Serial open successful."
except:
    print  "Serial cannot open!!!"
    sys.exit()       
result = serial.readall()
print result

'''     
conn = httplib.HTTPConnection("api.yeelink.net")
headers = {"Content-type":"application/json", "U-ApiKey":"34f75e8c7646cf1ef5cfa6e421822d31"} #application/x-www-form-urlencoded

params = ({"timestamp":"2013-07-10T20:55:14", 
           "value":50})
conn.request("POST", "/v1.0/device/3836/sensor/5430/datapoints", json.JSONEncoder().encode(params), headers)
response = conn.getresponse()
data = response.read()
if response.status == 200:
    print 'success'
    print data
else:
    print 'fail'
conn.close() 
'''
serial.close()    