from time import sleep

import cv2

import numpy as np
import collections
from threading import Thread

w = 72
h = 16

scale = 5


class LedMatrixMockup:
    def __init__(self):
        self.img = np.zeros((h, w), np.uint8)
        self.array0 = collections.deque(np.zeros(72), maxlen=72)
        self.array1 = collections.deque(np.zeros(72), maxlen=72)
        self.active_array = 0
        self.escape = False
        self.imS = np.zeros((h * scale, w * scale), np.uint8)
        self.stopping = False
        new_thread = Thread(target=self.windowLoop, )
        new_thread.start()

    def windowLoop(self):
        while not self.stopping:
            if cv2.waitKey(1) == ord('q'):
                break
            cv2.imshow('output', self.imS)  # Show image
            # press q to terminate the loop
        cv2.destroyAllWindows()
        raise KeyboardInterrupt

    def write(self, data):
        for i in data:
            if i == ord('.'):
                if self.escape:
                    self.escape = False
                else:
                    self.escape = True
                    continue
            elif self.escape:
                if i == ord('s'):
                    if self.active_array == 0:
                        img = np.unpackbits(np.array([self.array0], dtype=np.uint8), axis=0, bitorder='little')
                        # replace first 8 rows with the new img:
                        self.img[0:8, :] = img * 255
                    else:
                        img = np.unpackbits(np.array([self.array1], dtype=np.uint8), axis=0, bitorder='little')
                        # replace last 8 rows with the new img:
                        self.img[8:16, :] = img * 255
                    imS = cv2.resize(self.img, (w * scale, h * scale), interpolation=cv2.INTER_AREA)  # Resize image
                    self.imS = np.pad(imS, pad_width=10, mode='constant', constant_values=100)
                    self.escape = False
                    continue
                elif i == ord('0'):
                    self.active_array = 0
                    self.escape = False
                    continue
                elif i == ord('1'):
                    self.active_array = 1
                    self.escape = False
                    continue
                else:
                    self.escape = False
                    continue
            else:
                if self.active_array == 0:
                    self.array0.append(i)
                else:
                    self.array1.append(i)

    def stop(self):
        self.stopping = True
        pass
