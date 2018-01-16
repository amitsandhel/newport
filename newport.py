#!/usr/bin/python
# encoding: utf-8
from serial import Serial, PARITY_NONE
#import msvcrt
import time
import logging


"""newport.py
Created by Amit Sandhel on May 6 2016 

This software script is able to run the api comands to run the newport ARC LAMP POWER SUPPLY MODEL 69907 commands
to extract machine infromation as a text file which is saved in an excel file for graphing purposes.

Note: this script requires:
        1) Python 2.7
        2) PySerial (Python library that you will need to install separately via pip install)
        #http://pythonhosted.org/pyserial/
"""

'''REFERENCES 
#http://stackoverflow.com/questions/3850531/convert-python-string-to-its-ascii-representants
#http://pythonhosted.org/pyserial
'''

#logging setup files
logging.basicConfig(filename='testlog.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")
mylog2= logging.getLogger('testlog')
mylog2.info("**********info******")



class Probe(object):
    '''Class to run the machine commands using rs232 command protocols
    prototocol
    '''
    def __init__(self):
        self.s = None
        
        self.DP = []
        self.temp=[]
        self.RH=[]
        self.ser = None
        self.cycle = 0
        self.elapsed_time = None
        #self.counter = []
        self.dp = ''
        self.t = ''
        self.rh = ''
        self.data = []
        
        self.starttime = time.time()
        
    def open_port(self, port="COM3", baudrate=9600, bytesize=8, parity='N', 
                        stopbits=1, timeout = 1, rtscts=False):
        '''open port functions to open the serial port.
           This one is windows based 
        '''
        self.s = Serial(port, baudrate, bytesize, parity, stopbits,
                   timeout, rtscts) #, dsrdtr)  
        return self.s 

    def read_port(self):
        '''read the port data
        '''
        data_string = ""
        start_time = time.time()
        data = []
        MAXRECEIVETIMEOUT = 1  # is this in seconds or milli seconds?  Look up time.now()
        while True:
            b = self.s.inWaiting()
            if b > 0:
                new_char = self.s.read(1)
                #break at end character \n of command
                if new_char == "\n":
                    break
                else:
                    data_string = data_string + new_char
            if time.time() - start_time > MAXRECEIVETIMEOUT:
                break
        #time.sleep(0.1) #initallyo 0.01 was set to 0.5        
        
        self.data.append([data_string])
        
    def record_data(self):
        '''save the data to a csv file
        '''
        myfile = open(FILENAME, "a")
        newrow = time.strftime('%Y-%m-%d, %H:%M:%S, ') #+ ", "
        newrow += str(self.elapsed_time) + ','
        newrow += str(self.cycle) + ','
        newrow += str(self.dp) + ", " 
        newrow += str(self.t) + ", " 
        newrow += str(self.rh) + ", " 
        newrow += NEWLINE
        myfile.write(newrow)
        myfile.close()
        
    def run2(self):
        '''automatically run all the newport commands'''
        print 'running'
        #a = self.s.read("AMPS?\n")
        self.s.write("AMPS?\r\n")
        self.read_port()
        
        x1 = self.s.write("VOLTS?\r\n")
        a= self.read_port()
        
        self.s.write("WATTS?\r\n")
        b = self.read_port()
        
        x2 = self.s.write("LAMP HRS?\r\n")
        c = self.read_port()
        
        self.s.write("A-PRESET?\r\n")
        d = self.read_port()
        
        self.s.write("P-PRESET?\r\n")
        e = self.read_port()
        
        self.s.write("A-LIM?\r\n")
        f = self.read_port()
        
        self.s.write("P-LIM?\r\n")
        g = self.read_port()
        mylog2.debug('answer: ' + repr((a,b,c,d,e,f,g)))
    
    def x(self):
        '''x function to run the run2() function which will auto
        run the code
        '''
        print 'beginning'
        #run the open_port() function
        self.open_port()
        self.s.write("START\r\n")
        for x in range(5):
            print 'cycle: ', x
            self.run2()
            print self.data
            #self.s.close()
        #run the stop command
        self.s.write("STOP\r\n")
        #close the serial port
        self.s.close()
        print 'shutting down'

def main():
    '''function to run class above
    '''
    program = Probe()
    #program.run2()
    program.x()
    
################################################################################
if __name__== '__main__':
    print 'Morning user, NewPort Software is Running'
    #run the main() function
    main()
    
