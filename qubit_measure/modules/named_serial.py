import os
import platform
import serial
if os.name == 'posix':
    import fcntl #for locking
def __setup():
    '''On module import read rc file and setup namedports dictionary'''
    # stuck in a function to hide all the variables
    if platform.system() == 'Linux':
        rcfilename = '/etc/namedserialrc'
    elif platform.system() == 'Windows':
        # I don't know the best place for a win32 configuration file ...
        rcfilename = 'namedserialrc'
    elif platform.system() == 'Darwin':
        rcfilename = '/etc/namedserialrc'
    rcfile = open(rcfilename, 'rt')
    lines = rcfile.readlines()
    rcfile.close()#On module import, setup the list
    _namedports = {}
    for line in lines:
        if line[0] == '#' or len(line.strip()) <= 1:
            continue
        port, name = line.split()
        print(port)
        _namedports[name] = port
    return _namedports
namedports = __setup()

def getnames():
    '''Convenience routine for building ui - returns all defined names'''
    return namedports.keys()

class Serial(serial.Serial):
    ''' Wrapper class around the serial.Serial that uses logical device
    names instead of physical device names.
    '''
    def __init__(self, port=None, baud=115200, shared=False, **kwargs):
        '''Return a serial port object.  Parameter are:
        port - the logical name of the port defined in the config file
        baud - baudrate
        shared - allow others to used this serial port.  Only works
                 on posix system
        '''
        #print "port", port, baud, shared
        self.the_port   = port
        self.the_baud   = baud
        self.the_shared = shared

        # pass other serial init args?
        if not port in namedports:
            # Hmmm - raise an exception or just pass it on to serial
            # allowing use of "normal" device names?
            # This is probably better.
            raise ValueError("Named port '%s' not in configuration file" % port)
        myport = namedports[port]
        try:
            # serial.Serial.__init__(self, myport, baud)
            super(Serial, self).__init__(port=myport, baudrate=baud, **kwargs) #better?
        except serial.serialutil.SerialException as e:
            e.args = ("Error auto-loading serial port %s" % port, e.args[0])
            raise (e)
        if not shared and os.name == 'posix':
            try:
                fcntl.lockf(self.fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
            except IOError as e:
                e.args = ('Error locking on serial port %s' % port, e.args[0])
                raise (e)
        if shared and os.name != 'posix':
            raise ValueError('No shared ports on non-posix systems')

#    def write(self, value):
#        print "writing [%s]=%s" % (self.the_port, value)
#        super(Serial, self).write(value)

    def writelist(self, inlist):
        '''Send a list of integers as characters'''
        outstring = ''.join(map(chr, inlist))
        return self.write(outstring)