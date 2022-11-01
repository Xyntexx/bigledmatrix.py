import numpy as np


class LedController:
    def __init__(self, interface):
        self.H = 16
        self.W = 72
        self.interface = interface
        self.interface.write(b".q")  # quiet mode
        self.last_matrix = np.zeros((16, 72), dtype=np.uint8)

    def write_upper(self, matrix):
        hexarray = np.squeeze(np.packbits(matrix, axis=0, bitorder='little'))
        hexarray = hexarray.tobytes()
        # replace the escape character with two dots:
        hexarray.replace(b'.', b'..')
        # first write the first 8 rows:
        self.interface.write(b".0")
        self.interface.write(hexarray)
        self.interface.write(b".s")
        # add matrix to last_matrix:
        self.last_matrix[0:8, :] = matrix

    def write_lower(self, matrix):
        hexarray = np.squeeze(np.packbits(matrix, axis=0, bitorder='little'))
        hexarray = hexarray.tobytes()
        # replace the escape character with two dots:
        hexarray.replace(b'.', b'..')
        # then write the last 8 rows:
        self.interface.write(b".1")
        self.interface.write(hexarray)
        self.interface.write(b".s")
        # add matrix to last_matrix:
        self.last_matrix[8:16, :] = matrix

    def write_full(self, matrix):
        array1 = matrix[0:8, :]
        array2 = matrix[8:16, :]
        self.write_upper(array1)
        self.write_lower(array2)
