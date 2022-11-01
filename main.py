from time import sleep
import faulthandler

from led_effects import LedEffects

faulthandler.enable()
import numpy as np
from led_mockup_opencv import LedMatrixMockup
from led_controller import LedController
from text_to_array import Font

interface = LedMatrixMockup()
led_controller = LedController(interface)
led_effects = LedEffects(interface)
H = led_controller.H
W = led_controller.W

pixel_font_small = Font(r'C:\Windows\Fonts\arial.ttf', 10)
pixel_font_big = Font(r'victor-pixel.ttf', 24)


def min_height(matrix, size):
    if matrix.shape[0] < size:
        return np.concatenate((matrix, np.zeros((size - matrix.shape[0], matrix.shape[1]), dtype=bool)), axis=0)
    else:
        return matrix


spinni = np.array(pixel_font_small.render_text('SPINNI'))
print(spinni.shape)
you = np.array(pixel_font_small.render_text('YOU'))

spinni = min_height(spinni, 8)
you = min_height(you, 8)

# 8x8 pixel matrix of a heart:
heart = np.unpackbits(np.array([[0b00000000,
                                 0b01100110,
                                 0b11111111,
                                 0b11111111,
                                 0b01111110,
                                 0b00111100,
                                 0b00011000,
                                 0b00000000]], dtype=np.uint8), axis=0).T

test_matrix1 = np.array([[(i % 2) ^ (j % 2) for i in range(H)] for j in range(80)]).transpose()
test_matrix2 = np.array([[0 if ((i % 2) ^ (j % 2)) else 1 for i in range(H)] for j in range(W)]).transpose()


def spinni_loves_you(speed=100):
    # Combine spinni on firt line and heart and you on second line:

    line1 = np.concatenate((spinni, heart, you), axis=1)

    matrix = np.concatenate((line1, line1), axis=0)
    led_effects.scrollMatrix(matrix, speed, False)


def main():
    while True:
        spinni_loves_you()
        sleep(1)
        led_effects.scroll_out_up(100)
        sleep(1)
        led_effects.scrollMatrix(test_matrix1, 20, False)
        sleep(1)
        led_effects.scroll_out_up(10)
        sleep(1)
        led_effects.scroll_in_from_below(test_matrix2, 20)
        sleep(1)
        led_effects.scroll_out_left(10)
        sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        interface.stop()


