import numpy as np
from Tools.scripts.generate_re_casefix import hexint


class pygame:
    pass


class ImageFont:
    pass


class Image:
    pass


class ImageDraw:
    pass


h = 16
w = 72

test_matrix1 = np.array([[(i % 2) ^ (j % 2) for i in range(h)] for j in range(w)]).transpose()
test_matrix2 = np.array([[0 if ((i % 2) ^ (j % 2)) else 1 for i in range(h)] for j in range(w)]).transpose()


def print_matrix(matrix):
    for j in range(h):
        for i in range(w):
            print(matrix[j][i], end=" ")
        print()


class LedMatrixMockup:
    def __init__(self):
        self.array = pygame.PixelArray()

    def write(self, data):
        k = 0

        for i in range(w):
            for j in range(h):
                self.array[i, j] = pygame.Color(255, 0, 255) if data[k] else pygame.Color(0, 0, 0)
                k += 1


chars = {tuple(map(int, f"{n:08b}")): n for n in range(256)}


def toChars(bits):
    return bytes(chars[b] for b in zip(*(bits[7 - i::8] for i in range(8)))).decode()


def matrix_to_char(array):
    output = ""
    array1 = array[0:8, :]
    array2 = array[8:16, :]

    hexarray1 = np.packbits(array1, axis=0, bitorder='little')
    hexarray2 = np.packbits(array2, axis=0, bitorder='little')

    hexarray_joined = np.concatenate((hexarray1, hexarray2), axis=1)
    print(hexarray_joined)

    return output


def char_to_pixels(text, path='arialbd.ttf', fontsize=14):
    """
    Based on https://stackoverflow.com/a/27753869/190597 (jsheperd)
    """
    font = ImageFont.truetype(path, fontsize)
    w, h = font.getsize(text)
    h *= 2
    image = Image.new('L', (w, h), 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    return arr


def spinni_loves_you():
    pass


def main():
    print_matrix(test_matrix1)
    print()
    print_matrix(test_matrix2)
    var1 = matrix_to_char(test_matrix1)
    print(var1)


if __name__ == '__main__':
    main()
