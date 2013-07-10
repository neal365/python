'''
Created on 2013-7-10

@author: Administrator
'''
import httplib
import json
import serial
import sys
import time
from datetime import datetime  

def postResult(year,month,day,hour,minute,second,humidity,temp):
    conn = httplib.HTTPConnection("api.yeelink.net")
    headers = {"Content-type":"application/json", "U-ApiKey":"34f75e8c7646cf1ef5cfa6e421822d31"} #application/x-www-form-urlencoded
    
    params = ({"timestamp":str(year) + "-" + str(month) + "-" + str(day) + "T" +
               str(hour) + ":" + str(minute) + ":" + str(second), 
               "value":str(humidity)})
    print "post:"
    print params
    conn.request("POST", "/v1.0/device/3836/sensor/5430/datapoints", json.JSONEncoder().encode(params), headers)
    response = conn.getresponse()
    data = response.read()
    if response.status == 200:
        print 'humdity success'
        print data
    else:
        print 'humdity fail'
        
    params = ({"timestamp":str(year) + "-" + str(month) + "-" + str(day) + "T" +
               str(hour) + ":" + str(minute) + ":" + str(second), 
               "value":str(temp)})
    print "post:"
    print params
    conn.request("POST", "/v1.0/device/3836/sensor/5429/datapoints", json.JSONEncoder().encode(params), headers)
    response = conn.getresponse()
    data = response.read()
    if response.status == 200:
        print 'temp success'
        print data
    else:
        print 'temp fail'
    conn.close() 

ser = serial.Serial()
ser.port = "com24"
ser.baudrate = 9600
ser.stopbits = 1
try:
    ser.close() 
    ser.open()
    print "Serial open successful."
except:
    print  "Serial cannot open!!!"
    sys.exit()
while(1):
    result = ser.read(ser.inWaiting())
    print result
    humidity = ""
    temp = ""
    if "%" in result:
        h1 = result.find("humdity = ") + 10
        h2 = result.find("%") - 1
        humidity = result[h1:h2+1]
        t1 = result.find("temperature = ") + 14
        temp = result[t1:t1+2]
        print "humidity="
        print humidity
        print "temp="
        temp.replace("C", "")
        print temp        
        now = datetime.now()  
        year = now.year  
        month = now.month  
        day = now.day  
        hour = now.hour  
        minute = now.minute  
        second = now.second  
        postResult(year,month,day,hour,minute,second,humidity,temp)
        
    time.sleep(1)
ser.close() 



   
