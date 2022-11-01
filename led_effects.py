# Take a 8x72 matrix and write it to the led matrix
from time import sleep
from typing import Callable

import numpy as np

from led_controller import LedController


class LedEffects:
    def __init__(self, interface):
        self.interface = interface
        self.led_controller = LedController(interface)
        self.H = self.led_controller.H
        self.W = self.led_controller.W

    # Scroll the matrix in from the right and out to the left. Start with a blank matrix.
    def scrollMatrix(self, matrix, speed, scroll_out=True,
                     output_function: Callable[[np.ndarray], None] = None):

        if output_function is None:
            output_function = self.led_controller.write_full
        # Matrix width:
        mw = matrix.shape[1]
        h = matrix.shape[0]

        if mw < self.W:
            # Scroll matrix in from the right:
            for i in range(mw + 1):
                output_function(np.concatenate((np.zeros((h, self.W - i), dtype=bool), matrix[:, 0:i]), axis=1))
                sleep(1 / speed)
            # Scroll matrix from the right to the left:
            for i in range(1, self.W - mw + 1):
                output_function(
                    np.concatenate((np.zeros((h, self.W - mw - i), dtype=bool), matrix, np.zeros((h, i), dtype=bool)),
                                   axis=1))
                sleep(1 / speed)
            # then scroll out to the left:
            if scroll_out:
                for i in range(1, mw + 1):
                    output_function(
                        np.concatenate((matrix[:, 0:mw - i], np.zeros((h, self.W - mw + i), dtype=bool)), axis=1))
                    sleep(1 / speed)
        else:
            for i in range(self.W):
                output_function(np.concatenate((np.zeros((h, self.W - i), dtype=bool), matrix[:, 0:i]), axis=1))
                sleep(1 / speed)
            # if matrix is wider than the led matrix, scroll the text first:
            for i in range(mw - self.W):
                output_function(matrix[:, i:i + self.W])
                sleep(1 / speed)
            # then scroll out to the left:
            if scroll_out:
                for i in range(1, self.W):
                    self.led_controller.write_full(
                        np.concatenate((matrix[:, mw - self.W + i:mw], np.zeros((h, i), dtype=bool)), axis=1))
                    sleep(1 / speed)

    # Get the last matrix and scroll it out up. Fill the bottom with zeros.
    def scroll_out_up(self, speed):
        matrix = self.led_controller.last_matrix.copy()
        h = matrix.shape[0]
        for i in range(h + 1):
            self.led_controller.write_full(np.concatenate((matrix[i:h, :], np.zeros((i, self.W), dtype=bool)), axis=0))
            sleep(1 / speed)

    def scroll_out_left(self, speed):
        matrix = self.led_controller.last_matrix.copy()
        w = matrix.shape[1]
        for i in range(w + 1):
            self.led_controller.write_full(np.concatenate((matrix[:, i:w], np.zeros((self.H, i), dtype=bool)), axis=1))
            sleep(1 / speed)

    def scroll_in_from_below(self, matrix, speed):
        w = matrix.shape[1]
        # if matrix is narrower than the led matrix, add zeros to the left and right:
        if w < self.W:
            matrix = np.concatenate(
                (np.zeros((self.H, int((self.W - w) / 2)), dtype=bool), matrix,
                 np.zeros((self.H, self.W - int((self.W - w) / 2)), dtype=bool)),
                axis=1)
        # scroll in from the bottom:
        for i in range(self.H + 1):
            self.led_controller.write_full(
                np.concatenate((np.zeros((self.H - i, self.W), dtype=bool), matrix[0:i, :]), axis=0))
            sleep(1 / speed)
