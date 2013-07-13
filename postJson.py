'''
Created on 2013-7-10

@author: njugui@gmail.com
'''
import httplib
import json
import serial
import sys
import time
from datetime import datetime  

def postResult(year,month,day,hour,minute,second,humidity,temp):
    conn = httplib.HTTPConnection("api.yeelink.net")
    headers = {"Content-type":"application/json", "U-ApiKey":"your_yeelink_key"} 
    
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
ser.port = "com23"
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
    humidity = ""
    temp = ""
    if "%%" in result and "##" in result and "\n" in result:
        print result
        h1 = result.find("%%") + 2
        h2 = result.find("%%",h1)
        humidity = result[h1:h2]
        t1 = result.find("##") + 2
        t2 = result.find("##",t1)
        temp = result[t1:t2]
        print "humidity="
        print humidity
        print "temp="
        print temp        
        now = datetime.now()  
        year = now.year  
        month = now.month  
        day = now.day  
        hour = now.hour  
        minute = now.minute  
        second = now.second  
        print now
        postResult(year,month,day,hour,minute,second,humidity,temp)
    time.sleep(0.1)



   
