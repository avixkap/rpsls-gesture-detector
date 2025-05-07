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
