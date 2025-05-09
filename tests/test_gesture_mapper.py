import unittest
from utils.gesture_mapper import gesture_mapper


class TestGestureMapper(unittest.TestCase):
    # Test if the gesture_mapper correctly maps 0 to "Rock"
    def test_rock(self):
        self.assertEqual(gesture_mapper(0), "Rock")

    # Test if the gesture_mapper correctly maps 2 to "Scissors"
    def test_scissors(self):
        self.assertEqual(gesture_mapper(2), "Scissors")

    # Test if the gesture_mapper correctly maps 3 to "Spock"
    def test_spock(self):
        self.assertEqual(gesture_mapper(3), "Spock")

    # Test if the gesture_mapper correctly maps 5 to "Paper"
    # Note: Verify if 5 is an intentional input, as it seems out of sequence
    def test_paper(self):
        self.assertEqual(gesture_mapper(5), "Paper")