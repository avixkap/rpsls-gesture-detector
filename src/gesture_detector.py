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

    def run_avg(self, image, a_weight=0.5):
        """Accumulate the background model."""
        if self.bg_model is None:
            self.bg_model = image.copy().astype("float")
        else:
            cv2.accumulateWeighted(image, self.bg_model, a_weight)

    def segment(self, image, threshold=25):
        """Segment the hand region using background subtraction and thresholding."""
        assert self.bg_model is not None, "Background model not initialized"

        diff = cv2.absdiff(self.bg_model.astype("uint8"), image)
        thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

        # Clean the image
        kernel = np.ones((3, 3), np.uint8)
        thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel, iterations=2)

        contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        segmented = max(contours, key=cv2.contourArea)
        return thresholded, segmented

    @staticmethod
    def _count_fingers(contour):
        """Count fingers from the hand contour using convexity defects."""
        finger_count = 0
        hull = cv2.convexHull(contour, returnPoints=False)

        if hull is not None and len(hull) > 3:
            defects = cv2.convexityDefects(contour, hull)
            if defects is not None:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(contour[s][0])
                    end = tuple(contour[e][0])
                    far = tuple(contour[f][0])

                    a = np.linalg.norm(np.array(end) - np.array(start))
                    b = np.linalg.norm(np.array(far) - np.array(start))
                    c = np.linalg.norm(np.array(end) - np.array(far))

                    angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c + 1e-6))

                    if angle <= np.pi / 2 and d > 30:
                        finger_count += 1

        return min(finger_count + 1, 5)
    
    @staticmethod
    def _draw_feedback(frame, text, pos=(10, 30), color=(0, 0, 255), scale=0.7):
        """Draw text feedback on frame."""
        cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2)

    @staticmethod
    def _draw_roi_box(frame, top, right, bottom, left):
        """Draw ROI box on the video frame."""
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    def _calculate_fps(self, num_frames):
        """Calculate frames per second."""
        elapsed_time = time.time() - self.start_time + 1e-6
        return num_frames / elapsed_time
    
    def _del_(self):
        """Release video capture on destruction."""
        if self.cap.isOpened():
            self.cap.release()