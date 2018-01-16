#!/usr/bin/python
# encoding: utf-8

from serial import Serial, PARITY_NONE
#import msvcrt
import time

"""
humidity.py

Created by Amit Sandhel on May 12 2015  

This software script is able to run the api comands to run Omegas HX90A humidity sensor
this is a read only sensor with a built in temperature, humidity, relatively humidity and dewpoint values
all at once. 

Note: this script requires:
        1) Python 2.7
        2) PySerial (Python library that you will need to install separately via pip install)
        #http://pythonhosted.org/pyserial/

REFERENCES 
#http://stackoverflow.com/questions/3850531/convert-python-string-to-its-ascii-representants
#http://pythonhosted.org/pyserial
"""



#Local variables for csv filename convention
b = time.strftime('%Y-%m-%d-%H-%M-%S')
FILENAME = "%sHUMIDITY_PROBE.csv"%b
NEWLINE = "\n"

class Probe(object):
    '''class to extract data from the humidity probe
    '''
    def __init__(self):
        '''initalization function to initalize variables which will save data
        '''
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
        self.data = ''
        
    def open_port(self, port="COM8", baudrate=19200, bytesize=8, parity='N', 
                        stopbits=1, timeout = 1, rtscts=False):
        '''open_port() function which uses the serial library to read data from the sensor
        '''
        self.s = Serial(port, baudrate, bytesize, parity, stopbits,
                   timeout, rtscts) #, dsrdtr)  
        return self.s 

    def read_port(self):
        '''fucntion to read data from the ports sends commands and receives back data 
        '''
        data_string = ""
        start_time = time.time()
        MAXRECEIVETIMEOUT = 1  # is this in seconds or milli seconds?  Look up time.now()
        while True:
            b = self.s.inWaiting()
            if b > 0:
                new_char = self.s.read(1)
                if new_char == "\n":
                    break
                else:
                    data_string = data_string + new_char
            if time.time() - start_time > MAXRECEIVETIMEOUT:
                break
        time.sleep(0.5) #initallyo 0.01 was set to 0.5        

        for line in data_string:
            b=data_string.strip().split(',')
            #print b
            if len(b) == 3:
                self.dp = b[0].lstrip('DP\xf8C=')
                self.t = b[1].lstrip('AT\xf8C=')
                self.rh = b[2].lstrip('%RH=').rstrip('\x15')
            else:
                #print 'incorrect length'
                pass
        
    def record_data(self):
        '''function to save data to an excel csv file
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
        
    def run(self):
        '''function to run the above classes  
        '''
        #cycle = 1
        #timer setting variables 
        date = time.strftime('%Y-%m-%d')
        start_time = time.time()
        timer = time.time()
        #call the open_port() function
        self.ser = self.open_port()
        #open the csv file name write the headers and close the csv file
        myfile = open(FILENAME, "a")
        myfile.write("Date, Time, Timer, Cycle, DP, temp, RH"+NEWLINE)
        myfile.close()
        while True:
            #determine elapsed time and increase counter
            self.elapsed_time = time.time() - start_time
            #print 'cycle: ', self.cycle
            self.cycle +=1
            #run the read_port() function and save data to excel file
            self.read_port()
            self.record_data()
            print 'Cycle: %s, Date; %s '%(self.cycle, date)
            print "Time: %s, DP: %s, Temp: %s, RH: %s"%(self.elapsed_time, self.dp, self.t, self.rh) 
            #print repr(self.dp)
            #print repr(self.t)
            #print repr(self.rh)
            #print str(self.dp)
            print "\n\n"
            
            #if msvcrt.kbhit():
            #    ch = msvcrt.getch()
              #  if ch.upper() == "Q":
                #    print "EXITING SOFTWARE"
                  #  break
                  
        #close the serial port
        self.ser.close()

def main():
    '''main() function to run the above class
    '''
    program = Probe()
    #run class run function
    program.run()
    
################################################################################
if __name__== '__main__':
    print 'User Humidity Probe Software Running'
    #run the module
    main()
    
