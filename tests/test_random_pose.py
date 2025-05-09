import unittest
from unittest.mock import patch, MagicMock
from utils.random_pose import random_pose
from constants import IMAGE_DIR, FRAME_SIZE
from PIL import ImageTk


class TestRandomPose(unittest.TestCase):
    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_image_dir_does_not_exist(self, mock_makedirs, mock_path_exists):
        # Simulate IMAGE_DIR not existing
        mock_path_exists.return_value = False

        result = random_pose("test")
        mock_makedirs.assert_called_once_with(IMAGE_DIR)
        self.assertIsNone(result)

    @patch("os.path.exists")
    @patch("os.listdir")
    def test_no_matching_files(self, mock_listdir, mock_path_exists):
        # Simulate IMAGE_DIR exists but no matching files
        mock_path_exists.return_value = True
        mock_listdir.return_value = ["file1.png", "file2.jpg"]

        result = random_pose("nonexistent")
        self.assertIsNone(result)

    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("os.path.join")
    @patch("PIL.Image.open")
    @patch("utils.random_pose.random.choice")
    def test_matching_file_found(
        self, mock_random_choice, mock_image_open, mock_path_join, mock_listdir, mock_path_exists
    ):
        # Simulate IMAGE_DIR exists and a matching file is found
        mock_path_exists.return_value = True
        mock_listdir.return_value = ["test_image.png", "other_image.jpg"]
        mock_random_choice.return_value = "test_image.png"
        mock_path_join.return_value = "mocked_path/test_image.png"

        mock_image = MagicMock()
        mock_image.resize.return_value = mock_image
        mock_image_open.return_value = mock_image

        result = random_pose("test")
        mock_random_choice.assert_called_once_with(["test_image.png"])
        mock_image_open.assert_called_once_with("mocked_path/test_image.png")
        mock_image.resize.assert_called_once_with(FRAME_SIZE)
        self.assertIsInstance(result, ImageTk.PhotoImage)