import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk

from src.gui import RPSGui
from constants import CHOICES


class TestRPSGui(unittest.TestCase):
    def setUp(self):
        # Set up a Tkinter root window for testing
        self.root = tk.Tk()
        self.gui = RPSGui(self.root)

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.root.destroy()

    @patch("src.gui.random.choice")
    @patch("src.gui.random_pose")
    @patch("src.gui.game_round_result")
    def test_play(self, mock_game_round_result, mock_random_pose, mock_random_choice):
        # Mock the dependencies
        mock_random_choice.return_value = "Rock"
        mock_random_pose.return_value = None
        mock_game_round_result.return_value = ("You Win", 1, 0)

        # Simulate a valid gesture
        self.gui.gesture_name = "Paper"
        self.gui.play()

        # Assertions
        mock_random_choice.assert_called_once_with(CHOICES)
        mock_game_round_result.assert_called_once_with("Paper", "Rock", 0, 0)
        self.assertEqual(self.gui.player_score, 1)
        self.assertEqual(self.gui.computer_score, 0)
        self.assertEqual(self.gui.result_label.cget("text"), "You Win")

    def test_reset(self):
        # Simulate a game state
        self.gui.player_score = 5
        self.gui.computer_score = 3
        self.gui.result_label.config(text="You Win")

        # Call the reset method
        self.gui.reset()

        # Assertions
        self.assertEqual(self.gui.player_score, 0)
        self.assertEqual(self.gui.computer_score, 0)
        self.assertEqual(self.gui.result_label.cget("text"), "")
        self.assertEqual(self.gui.p_result_label.cget("text"), "You:")
        self.assertEqual(self.gui.c_result_label.cget("text"), "Computer:")

    @patch("src.gui.gesture_mapper")
    def test_update_video(self, mock_gesture_mapper):
        # Mock the gesture_mapper function
        mock_gesture_mapper.return_value = "Rock"

        # Mock the detector's process method
        self.gui.detector.process = MagicMock(return_value=(None, 1, 1, None, None))

        # Call the update_video method
        self.gui.update_video()

        # Assertions
        self.assertEqual(self.gui.num_frames, 1)
        self.assertEqual(self.gui.gesture_name, "Rock")
        mock_gesture_mapper.assert_called_once_with(1)
