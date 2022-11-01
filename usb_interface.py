from serial import Serial


class SerialInterface:
    def __init__(self, port):
        self.ser = Serial(port, 2000000)

    def write(self, data):
        self.ser.write(data)

    def stop(self):
        self.ser.close()
        pass
