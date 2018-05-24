import serial

class Pump(object):

    def __init__(self, serial_port):
        self.piston = serial.Serial(
            serial_port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

    def setupPiston(self, address=1):
        setupString = '/' + str(address) + 'j16m100R\r\n'
        self.piston.write(setupString.encode())

    def dispensePercent(self, amount, tpi, velocity=16000, acceleration=100000, address=1):
        steps = str(int(tpi * 1600 * amount/100))
        accel = str(round(acceleration * 65536 / 400000000))
        dispenseString = '/' + str(address) + 'V' + str(velocity) + 'L'  + accel + 'P' + steps + 'R\r\n'
        self.piston.write(dispenseString.encode())


    def aspiratePercent(self, amount, tpi, velocity=16000, acceleration=100000, address=1):
        steps = str(int(tpi * 1600 * amount/100))
        accel = str(round(acceleration * 65536 / 400000000))
        aspirateString = '/' + str(address) + 'V' + str(velocity) + 'L'  + accel + 'D' + steps + 'R\r\n'
        self.piston.write(aspirateString.encode())

    def homePiston(self, velocity=16000, acceleration=100000, address=1):
        accel = str(round(acceleration * 65536 / 400000000))
        homeString = '/' + str(address) + 'V' + str(velocity) + 'L' + accel + 'ZR\r\n'
        self.piston.write(homeString.encode())

    def dispensePiston(self, velocity=16000, address=1):
        dispenseString = '/' + str(address) + 'V' + str(velocity) + 'A0R\r\n'
        self.piston.write(dispenseString.encode())

    def aspiratePiston(self, tpi, velocity=16000, acceleration=100000, address=1):
        accel = str(round(acceleration * 65536 / 400000000))
        aspirateString = '/' + str(address) + 'V' + str(velocity) + 'L' + accel  + 'A-' + str(tpi * 1600) + 'R\r\n'
        self.piston.write(aspirateString.encode())

    def primePiston(self, tpi, velocity=16000, acceleration=100000, address=1, times=10):
        primeString = '/' + str(address) + 'gV' + str(velocity) + 'A-' + str(tpi * 1600) + 'A0G10R\r\n'
        self.piston.write(primeString.encode())

    def stopPiston(self, address=1):
        stopString = '/' + str(address) + 'TR\r\n'
        self.piston.write(stopString.encode())
