import time

import cv2
import numpy as np
from PIL import Image, ImageTk

from utils import gesture_mapper


class GestureDetector:
    def __init__(self, roi, frame_size):
        self.roi = roi
        self.frame_size = frame_size
        self.start_time = time.time()
        self.bg_model = None
        self.finger_count = 0
        self.cap = cv2.VideoCapture(0)

import time

import cv2
import numpy as np
from PIL import Image, ImageTk

from utils import gesture_mapper


class GestureDetector:
    def _init_(self, roi, frame_size):
        self.roi = roi
        self.frame_size = frame_size
        self.start_time = time.time()
        self.bg_model = None
        self.finger_count = 0
        self.cap = cv2.VideoCapture(0)

    def run_avg(self, image, a_weight=0.5):
        if self.bg_model is None:
            self.bg_model = image.copy().astype("float")
        else:
            cv2.accumulateWeighted(image, self.bg_model, a_weight)

    def segment(self, image, threshold=25):
        assert self.bg_model is not None, "Background model is not initialized"
        diff = cv2.absdiff(self.bg_model.astype("uint8"), image)
        thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((3, 3), np.uint8)
        thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel, iterations=2)
        contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        segmented = max(contours, key=cv2.contourArea)
        return thresholded, segmented