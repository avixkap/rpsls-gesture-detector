import random
import tkinter as tk

from constants import WINDOW_SIZE, BG_COLOR, ROI, FRAME_SIZE
from src import GestureDetector
from src import show_rules
from utils import gesture_mapper, random_pose, game_round_result

choices = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]


class RPSGui:
    def _init_(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BG_COLOR)

        self.player_score = 0
        self.computer_score = 0
        self.last_gesture = None
        self.gesture_name = None

        self.video_label = tk.Label(root)
        self.video_label.pack(side="left", padx=10, pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack(side="right", padx=10, pady=10)
        self.num_frames = 0

        self.middle = tk.Frame(root, bg=BG_COLOR)
        self.middle.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.middle, text="ROCK\nPAPER\nSCISSORS\nLIZARD\nSPOCK", font=("Arial", 18, "bold"), fg="white",
                 bg=BG_COLOR).pack(pady=10)

        # Score Display
        self.score_display = tk.Label(self.middle, text="Player: 0   Computer: 0", font=("Arial", 14), fg="white",
                                      bg=BG_COLOR)
        self.score_display.pack(pady=5)

        self.result_label = tk.Label(self.middle, text="", font=("Arial", 20, "bold"), fg="yellow", bg=BG_COLOR)
        self.result_label.pack(pady=5)

        display_frame = tk.Frame(self.middle, bg=BG_COLOR)
        display_frame.pack(pady=10)

        self.p_result_label = tk.Label(display_frame, text="YOU: ", font=("Arial", 14), fg="white", bg=BG_COLOR)
        self.p_result_label.grid(row=0, column=0, padx=20)

        self.c_result_label = tk.Label(display_frame, text="COMPUTER: ", font=("Arial", 14), fg="white", bg=BG_COLOR)
        self.c_result_label.grid(row=0, column=1, padx=20)

        btn_frame = tk.Frame(self.middle, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="PLAY", font=("Arial", 12, "bold"), width=10, command=self.play).pack(side="left",
                                                                                                        padx=5)
        tk.Button(btn_frame, text="Reset Score", command=self.reset).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Rules", command=show_rules).pack(side="left", padx=5)

        self.detector = GestureDetector(ROI, FRAME_SIZE)

        self.update_video()

    def update_video(self):
        frame_imgtk, self.num_frames, finger_count = self.detector.process(self.num_frames)
        if frame_imgtk:
            self.video_label.imgtk = frame_imgtk
            self.video_label.configure(image=frame_imgtk)

        if finger_count is not None:
            self.gesture_name = gesture_mapper(finger_count)
            self.p_result_label.config(text=f"YOU: {self.gesture_name}")
        self.root.after(10, self.update_video)