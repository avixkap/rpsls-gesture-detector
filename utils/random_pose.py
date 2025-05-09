
import os
import random

from PIL import Image, ImageTk

from constants import IMAGE_DIR, FRAME_SIZE

def random_pose(file_name):
    """
    Selects a random image from the IMAGE_DIR that contains the given file_name substring,
    resizes it to FRAME_SIZE, and returns a Tkinter-compatible PhotoImage.

    Parameters:
        file_name (str): Substring to match filenames against (case-insensitive).

    Returns:
        ImageTk.PhotoImage: A resized Tkinter-compatible image object if a match is found.
        None: If the IMAGE_DIR does not exist (and is created), or no matching files are found.

    Notes:
        - If IMAGE_DIR does not exist, it will be created and the function returns None.
        - Only the first match found is returned, selected randomly from the filtered list.
    """
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        return None
    files = [f for f in os.listdir(IMAGE_DIR) if file_name.lower() in f.lower()]
    if not files:
        return None
    path = os.path.join(IMAGE_DIR, random.choice(files))
    img = Image.open(path).resize(FRAME_SIZE)
    return ImageTk.PhotoImage(img)
