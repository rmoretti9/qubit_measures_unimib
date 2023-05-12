'''
Lakesore370
Created on Mar 11, 2009
@author: bennett
'''
import serial_instrument
from time import sleep
from threading import Lock

class PhaseMatrix_fsw(serial_instrument.SerialInstrument):
    '''
    The Lakeshore 370 AC Bridge Serial communication class
    '''

    def __init__(self, port='phasematrix1', baud=115200, shared=False,
    ):
        '''Constructor Place holder '''

        super(PhaseMatrix_fsw, self).__init__(port, baud, shared)

        self.lock = Lock()
        self.id_string = ""
        self.manufacturer = 'Phase Matrix'
        self.model_number = 'FSW-0010'
        self.description  = 'Microwave Synthesizer'


    def write(self, cmd):
        with self.lock:
            command_string = cmd + '\r\n'
            self.serial.write(command_string)
            sleep(.1)
            #result = self.serial.readline()
            #if result != '\r\n':
            #    print 'Data recievd when not expected!'

    def ask(self, cmd):
        with self.lock:
            command_string = cmd + '\r\n'
            self.serial.write(command_string)
            sleep(.1)
            result = self.serial.readline()
            result = result.split('\r\n')[0]

        return result

    def askFloat(self, cmd):
        with self.lock:
            command_string = cmd + '\r\n'
            self.serial.write(command_string)
            sleep(.1)
            result = self.serial.readline()
            if result == '' or result == '\c\r':
                print('Response was empty')
                self.write(cmd)
                result = self.serial.readline()
            fresult = float(result)

        return fresult

    def askNull(self):
        with self.lock:
            buffer_empty = True
            try:
                result = self.serial.readline()
                print (result)
                if result != '':
                    print ('Response was not empty')
                    buffer_empty = False
            except:
                print ('Buffer was already empty and timeout')

    def serialCheck(self):
        with self.lock:
            result = self.serial.readline()
            while result != '':
                result = self.serial.readline()
                print ('Clearing buffer.')
            print ('Buffer empty.')

    def setFrequencyGHz(self, frequency):
        ''' Set the microwave frequency in GHz.'''

        commandstring = 'FREQ ' + str(frequency) + ' GHz'
        self.write(commandstring)

    def getFrequency(self):
        ''' Get the microwave frequency.'''

        commandstring = 'FREQ?'
        response = self.askFloat(commandstring)

        return response

    def setPowerdBm(self, power):
        ''' Set the microwave power in dBm.'''

        commandstring = 'POW ' + str(power)
        self.write(commandstring)

    def getPowerdBm(self):
        ''' Get the microwave power.'''

        commandstring = 'POW?'
        response = self.askFloat(commandstring)

        return response

    def setRefSource(self, EXT_INT):
        ''' Set the Reference source. EXT/INT'''

        commandstring = 'ROSC:SOUR ' + str(EXT_INT)
        self.write(commandstring)

    def getRefSource(self):
        ''' Get the Reference Source.'''

        commandstring = 'ROSC:SOUR?'
        response = self.ask(commandstring)

        return response

    def setOutputStatus(self, ON_OFF):
        ''' Set the Reference source. EXT/INT'''

        commandstring = 'OUTP:STAT ' + str(ON_OFF)
        self.write(commandstring)

    def getOutputStatus(self):
        ''' Get the Reference Source.'''

        commandstring = 'OUTP:STAT?'
        response = self.ask(commandstring)

        return response