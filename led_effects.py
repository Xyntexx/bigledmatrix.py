# Take a 8x72 matrix and write it to the led matrix
from time import sleep
from typing import Callable

import numpy as np

from led_controller import LedController


def center_to_full_width(matrix, full_width):
    """
    Take a matrix that's up to `width` columns wide and
    add spacing to the sides to fill up `width`
    """
    h, w = matrix.shape
    if w < full_width:
        matrix = np.concatenate(
            (np.zeros((h, int((full_width - w) / 2)), dtype=bool), matrix,
             np.zeros((h, full_width - w - int((full_width - w) / 2)), dtype=bool)),
            axis=1)
    return matrix


def expand_to_full_height(matrix, full_height):
    h, w = matrix.shape
    if h < full_height:
        matrix = np.concatenate(
            (matrix, np.zeros((8 - h, w), dtype=bool)), axis=0
        )
    return matrix


class LedEffects:
    def __init__(self, interface, mirror=False):
        self.interface = interface
        self.led_controller = LedController(interface, mirror)
        self.H = self.led_controller.H
        self.W = self.led_controller.W

    # Scroll the matrix in from the right and out to the left. Start with a blank matrix.
    def scrollMatrix(self, matrix, speed=100, scroll_out=True,
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
                        np.concatenate((matrix[:, i:], np.zeros((h, self.W - mw + i), dtype=bool)), axis=1))
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
                for i in range(1, self.W+1):
                    output_function(
                        np.concatenate((matrix[:, mw - self.W + i:], np.zeros((h, i), dtype=bool)), axis=1))
                    sleep(1 / speed)

    # Get the last matrix and scroll it out up. Fill the bottom with zeros.
    def scroll_out_up(self, speed):
        matrix = self.led_controller.get_last_matrix()
        h = matrix.shape[0]
        for i in range(h + 1):
            self.led_controller.write_full(np.concatenate((matrix[i:h, :], np.zeros((i, self.W), dtype=bool)), axis=0))
            sleep(1 / speed)

    def scroll_out_left(self, speed=100):
        matrix = self.led_controller.get_last_matrix()
        w = matrix.shape[1]
        for i in range(w + 1):
            self.led_controller.write_full(np.concatenate((matrix[:, i:w], np.zeros((self.H, i), dtype=bool)), axis=1))
            sleep(1 / speed)

    def scroll_in_from_below(self, matrix, speed=100):
        if matrix.shape[1] > 72:
            raise Exception("Matrix must be maximum of 72 wide for this effect")
        matrix = center_to_full_width(matrix, self.W)

        # scroll in from the bottom:
        for i in range(self.H + 1):
            self.led_controller.write_full(
                np.concatenate((np.zeros((self.H - i, self.W), dtype=bool), matrix[0:i, :]), axis=0))
            sleep(1 / speed)

    def set_partial(self, matrix, row=0):
        matrix = center_to_full_width(matrix, self.W)
        matrix = expand_to_full_height(matrix, 8)

        if row == 0:
            self.led_controller.write_upper(matrix)
        else:
            self.led_controller.write_lower(matrix)

