import serial

class Scale(object):

    def __init__(self, serial_port):
        self.scale = serial.Serial(
            serial_port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

    def zeroScale(self):
        self.scale.write('Z\r\n'.encode('utf-8'))

    def readScale(self):
        return self.scale.write('S\r\n'.encode('utf-8'))

    def flushScale(self):
        self.scale.flushInput()

    def readLine(self):
        return self.scale.readline()
