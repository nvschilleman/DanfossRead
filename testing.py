#!/usr/bin/python

# Read temperature from Danfoss EKC202 and publish it on MQTT.
# Eirik Haustveit, 2016

import serial
import time

import crc16
import struct
#import paho.mqtt.client as mqtt


ser = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 9600, timeout=1, rtscts=False)

ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_EVEN #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
ser.xonxoff = False    #disable software flow control
ser.rtscts = False    #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 0.1 #timeout for write
ser.readTimeout = 0.1

#print ser

#address = '\x09'
#command = '\x11'
#
#data = address + command
#data = data + compute_crc(data)
#
#print('Transmitting: ' + str(data))
#ser.rts = True
#
#ser.dtr = True
#time.sleep(0.1)
#ser.write(data)
#
#ser.write(':010310010001EA\r\n')
#print repr(ser.read(1000)) # Read 1000 bytes, or wait for timeout


def read_input_register(dev, reg):
    command = chr(dev) + '\x03' + struct.pack('>H',reg) + '\x00\x01'
    crc =  crc16.calcString(command, 0xFFFF)
    command = command + struct.pack('<H',crc) 

    #print 'Register: ' +  str(reg)
    #print ":".join("{:02x}".format(ord(c)) for c in command)
    
    ser.rts = True
    ser.write(command)
    time.sleep(0.008)
    ser.rts = False

    time.sleep(1)        
 
    response = ser.readline()


    #TODO: Implement check of checksum(CRC), and handle any modbus error messages
    #checksum = ord(response[5:7])
    #comp_checksum = struct.pack('<H',crc16.calcString(response[1:5], 0xFFFF))
    #print 'chk: ' + str(comp_checksum) 
    return response 
  
def main():

#    mqttc = mqtt.Client()

#    mqttc.connect("localhost")
#    mqttc.loop_start()

 #   while True:
    
    bits = [535, 538, 923, 924, 926, 1012, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026]
    
    for bit in bits:       

        response = read_input_register(1, bit)
        if response:    
            print ":".join("{:02x}".format(ord(c)) for c in response)
    
            val = ord(response[4:5])/10.0
        print 'Value: ' + str(val)
      #  mqttc.publish("ekc2021/temperature", temperature) 
    else:
        print "No data"
 



if __name__ == '__main__':
    main()
