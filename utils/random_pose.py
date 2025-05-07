import os
import random
from PIL import Image, ImageTk

from constants import IMAGE_DIR, FRAME_SIZE

def random_pose(file_name):
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        return None
    files = [f for f in os.listdir(IMAGE_DIR) if file_name.lower() in f.lower()]
    if not files:
        return None
    path = os.path.join(IMAGE_DIR, random.choice(files))
    img = Image.open(path).resize(FRAME_SIZE)
    return ImageTk.PhotoImage(img)