from time import sleep
from led_effects import LedEffects
import numpy as np
from led_mockup_opencv import LedMatrixMockup
from pixel_font import Font
from usb_interface import SerialInterface

#interface = LedMatrixMockup()
interface = SerialInterface("COM4")
led_effects = LedEffects(interface)
H = led_effects.H
W = led_effects.W

pixel_font_small = Font(r'C:\Windows\Fonts\arial.ttf', 10)


pixel_font_big = Font(r'C:\Windows\Fonts\arial.ttf', 20)


def min_height(matrix, size, align_up=True):
    if matrix.shape[0] < size:
        if align_up:
            return np.concatenate((matrix, np.zeros((size - matrix.shape[0], matrix.shape[1]), dtype=bool)), axis=0)
        else:
            return np.concatenate((np.zeros((size - matrix.shape[0], matrix.shape[1]), dtype=bool), matrix), axis=0)
    else:
        return matrix


spinni = np.array(pixel_font_small.render_text('SPINNI'))
you = np.array(pixel_font_small.render_text('YOU'))
spinni = min_height(spinni, 8)
you = min_height(you, 8)

now_playing = np.array(pixel_font_small.render_text('PLAYING:'))
now_artist = np.array(pixel_font_small.render_text('TODD TERDELLA PRESENTS: BIGGA  BANGARE'))

next_up = np.array(pixel_font_small.render_text('NEXT UP:'))
next_artists = np.array(pixel_font_small.render_text(
    "DJ CASTOR 18:00   DJ CASTOR 19:00   DJ CASTOR 20:00   DJ CASTOR 21:00   DJ CASTOR 22:00-00:00"
))

spinni3you = np.array(pixel_font_big.render_text("SPINNI <3 YOU"))


print(next_up.shape)
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

ones = np.ones((H, W), dtype=bool)
zeros = np.zeros((H, W), dtype=bool)


def show_now_playing(speed=100):
    led_effects.scroll_in_from_below(min_height(now_playing, 16))
    led_effects.scrollMatrix(min_height(now_artist, 8, False), speed=40, scroll_out=True,
                             output_function=led_effects.led_controller.write_lower)


def show_next_playing(speed=100):
    led_effects.scroll_in_from_below(min_height(next_up, 16))
    led_effects.scrollMatrix(min_height(next_artists, 8, False), speed=20, scroll_out=True,
                             output_function=led_effects.led_controller.write_lower)


def spinni_loves_you(speed=100):
    # Combine spinni on firt line and heart and you on second line:

    line1 = np.concatenate((spinni, heart, you), axis=1)

    matrix = np.concatenate((line1, line1), axis=0)
    led_effects.scroll_in_from_below(matrix, speed)
    m = led_effects.led_controller.get_last_matrix()
    sleep(1)
    for i in range(1):
        led_effects.led_controller.write_full(zeros)
        sleep(1)
        led_effects.led_controller.write_full(m)
        sleep(1)


def main():
    while True:
        #led_effects.scroll_out_up(100)
        #sleep(1)
        show_now_playing()
        sleep(1)
        led_effects.scroll_out_left()
        sleep(1)
        spinni_loves_you()
        sleep(3)
        show_next_playing()
        led_effects.scroll_out_up(100)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        interface.stop()
