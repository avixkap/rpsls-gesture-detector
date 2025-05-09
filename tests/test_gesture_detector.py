import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import cv2

from src.gesture_detector import GestureDetector


class TestGestureDetector(unittest.TestCase):
    def setUp(self):
        # Define a sample ROI and frame size
        self.roi = (100, 200, 300, 400)
        self.frame_size = (640, 480)
        self.detector = GestureDetector(self.roi, self.frame_size)

    def tearDown(self):
        # Release the video capture resource
        del self.detector

    @patch("cv2.VideoCapture")
    def test_initialization(self, mock_video_capture):
        # Test if the GestureDetector initializes correctly
        mock_video_capture.return_value.isOpened.return_value = True
        detector = GestureDetector(self.roi, self.frame_size)
        self.assertEqual(detector.roi, self.roi)
        self.assertEqual(detector.frame_size, self.frame_size)
        self.assertIsNotNone(detector.cap)

    def test_run_avg(self):
        # Test the background model accumulation
        image = np.zeros((100, 100), dtype="uint8")
        self.detector.run_avg(image)
        self.assertIsNotNone(self.detector.bg_model)

    def test_segment_no_contours(self):
        # Test segmentation when no contours are found
        image = np.zeros((100, 100), dtype="uint8")
        self.detector.bg_model = image
        result = self.detector.segment(image)
        self.assertIsNone(result)

    def test_segment_with_contours(self):
        # Test segmentation with a valid contour
        image = np.zeros((100, 100), dtype="uint8")
        cv2.rectangle(image, (30, 30), (70, 70), 255, -1)
        self.detector.bg_model = np.zeros_like(image)
        result = self.detector.segment(image)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)  # thresholded and segmented

    def test_count_fingers(self):
        # Test finger counting with a mock contour
        contour = np.array([[[0, 0]], [[1, 1]], [[2, 2]], [[3, 3]]])
        finger_count = self.detector._count_fingers(contour)
        self.assertEqual(finger_count, 1)

    @patch("cv2.VideoCapture.read")
    def test_process(self, mock_read):
        # Test the process method
        mock_read.return_value = (True, np.zeros((480, 640, 3), dtype="uint8"))
        frame_imgtk, num_frames, finger_count, gray_imgtk, threshold_imgtk = self.detector.process(0)
        self.assertIsNotNone(frame_imgtk)
        self.assertEqual(num_frames, 1)
        self.assertIsNone(finger_count)

    @patch("cv2.VideoCapture.read")
    def test_process_with_hand(self, mock_read):
        # Test the process method with a hand detected
        mock_read.return_value = (True, np.zeros((480, 640, 3), dtype="uint8"))
        self.detector.bg_model = np.zeros((200, 200), dtype="uint8")
        frame_imgtk, num_frames, finger_count, gray_imgtk, threshold_imgtk = self.detector.process(60)
        self.assertIsNotNone(frame_imgtk)
        self.assertEqual(num_frames, 61)

    def test_calculate_fps(self):
        # Test FPS calculation
        fps = self.detector._calculate_fps(60)
        self.assertGreater(fps, 0)