#!/usr/bin/python3
from datetime import datetime
import RPi.GPIO as GPIO
import time
import os
import glob
import argparse
import time
import datetime
import sys
from influxdb import InfluxDBClient
import RPi.GPIO as GPIO
import subprocess



#28-0316610970ff  28-3c01f09511a5  28-3c01f0951a36  28-3c01f0951e42  28-3c01f095b159  28-3c01f095c703

dev_path = '/sys/bus/w1/devices/'
dev_Aussentemp = glob.glob(dev_path + '28-3c01f09511a5')[0]
dev_Oben = glob.glob(dev_path + '28-3c01f095b159')[0]
dev_Mitte = glob.glob(dev_path + '28-3c01f0951e42')[0]
dev_Frischwasser = glob.glob(dev_path + '28-0316610970ff')[0]
dev_Vorlauf = glob.glob(dev_path + '28-3c01f0951a36')[0]
dev_Nachlauf = glob.glob(dev_path + '28-3c01f095c703')[0]
Aussentemp = dev_Aussentemp + '/w1_slave'
Oben = dev_Oben + '/w1_slave'
Mitte = dev_Mitte + '/w1_slave'
Frischwasser = dev_Frischwasser  + '/w1_slave'
Vorlauf = dev_Vorlauf + '/w1_slave'
Nachlauf = dev_Nachlauf + '/w1_slave'
host = 'xxx.xxx.xxx.xxx'
port = 8086
user = '[user]'
password = '[password]'
dbname= 'water'
session='boilertemp'


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)



#print(count_work)
def get_temp():
    
    temp_Aussentemp = 0
    temp_Oben = 0
    temp_Mitte = 0
    temp_Frischwasser = 0
    temp_Vorlauf = 0
    temp_Nachlauf = 0

    for t in range(1):
        tempfile_Aussentemp = open(Aussentemp)
        tempfile_Oben = open(Oben)
        tempfile_Mitte = open(Mitte)
        tempfile_Frischwasser = open(Frischwasser)
        tempfile_Vorlauf = open(Vorlauf)
        tempfile_Nachlauf = open(Nachlauf)


        text_Aussentemp = tempfile_Aussentemp.read()
        text_Oben = tempfile_Oben.read()
        text_Mitte = tempfile_Mitte.read()
        text_Frischwasser = tempfile_Frischwasser.read()
        text_Vorlauf = tempfile_Vorlauf.read() 
        text_Nachlauf = tempfile_Nachlauf.read()  
        tempfile_Aussentemp.close() 
        tempfile_Oben.close() 
        tempfile_Mitte.close() 
        tempfile_Frischwasser.close()
        tempfile_Vorlauf.close()
        tempfile_Nachlauf.close()

        tline_Aussentemp = text_Aussentemp.split("\n")[1] # the second line contains temperature
        tline_Oben = text_Oben.split("\n")[1] # the second line contains temperature
        tline_Mitte = text_Mitte.split("\n")[1] # the second line contains temperature
        tline_Frischwasser = text_Frischwasser.split("\n")[1] # the second line contains temperature
        tline_Vorlauf = text_Vorlauf.split("\n")[1] # the second line contains temperature
        tline_Nachlauf = text_Nachlauf.split("\n")[1] # the second line contains temperature
        
        tdata_Aussentemp= tline_Aussentemp.split(" ")[9] # position 9 contains temparature value
        tdata_Oben= tline_Oben.split(" ")[9] # position 9 contains temparature value
        tdata_Mitte= tline_Mitte.split(" ")[9] # position 9 contains temparature value
        tdata_Frischwasser= tline_Frischwasser.split(" ")[9] # position 9 contains temparature value
        tdata_Vorlauf = tline_Vorlauf.split(" ")[9] # position 9 contains temparature value
        tdata_Nachlauf = tline_Nachlauf.split(" ")[9] # position 9 contains temparature value
        
        temp_Aussentemp  += float(tdata_Aussentemp[2:])/1000
        temp_Oben  += float(tdata_Oben[2:])/1000
        temp_Mitte  += float(tdata_Mitte[2:])/1000
        temp_Frischwasser  += float(tdata_Frischwasser[2:])/1000
        temp_Vorlauf  += float(tdata_Vorlauf[2:])/1000
        temp_Nachlauf  += float(tdata_Nachlauf[2:])/1000
   
   

        timestamp=datetime.datetime.utcnow().isoformat()
        datapoints = [
            {
                "measurement": session,
                "time": timestamp,
                "fields": {"temp_Aussentemp":temp_Aussentemp, "temp_Oben":temp_Oben, "temp_Mitte":temp_Mitte, "temp_Frischwasser":temp_Frischwasser, "temp_Vorlauf":temp_Vorlauf, "temp_Nachlauf":temp_Nachlauf}
                }

            ]
        return datapoints



    else: 
        return (temp_Aussentemp / 1000)

client = InfluxDBClient(host, port, user, password, dbname)


while True:
    datapoints=get_temp()
    try:
        client.write_points(datapoints)
    except Exception as exc:
        print(exc)
    time.sleep(10)
