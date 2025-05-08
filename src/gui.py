import random
import tkinter as tk
from tkinter import Label, Button

from constants import ROI, FRAME_SIZE, CHOICES, FRAME_WIDTH, FRAME_HEIGHT
from src import GestureDetector, show_rules
from utils import gesture_mapper, random_pose, game_round_result


class RPSGui:
    def _init_(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Lizard Spock")
        self.root.configure(bg="white")

        self.video_label: Label | None = None
        self.greyscale_label: Label | None = None
        self.score_display: Label | None = None
        self.threshold_label: Label | None = None
        self.result_label: Label | None = None
        self.p_result_label: Label | None = None
        self.c_result_label: Label | None = None
        self.image_label: Label | None = None

        self.player_score = 0
        self.computer_score = 0
        self.num_frames = 0
        self.gesture_name = None

        self.build_layout()
        self.detector = GestureDetector(ROI, FRAME_SIZE)
        self.update_video()

    def build_layout(self):
        # ---------- Title ----------
        Label(self.root, text="RPSL Game", font=("Arial", 20, "bold"), bg="white") \
            .grid(row=0, column=0, columnspan=3, pady=(20, 10))

        # ---------- Left Frame ----------
        left_frame = tk.Frame(self.root, bg="white")
        left_frame.grid(row=1, column=0, padx=20, pady=20)

        main_frame = tk.Frame(left_frame, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg="black")
        main_frame.pack()

        self.video_label = Label(main_frame, bg="lightgray", width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.video_label.pack()

        frame_bar = tk.Frame(left_frame, bg="white")
        frame_bar.pack(pady=15)

        greyscale_box, self.greyscale_label = self.create_fixed_label(frame_bar, "Grayscale")
        greyscale_box.grid(row=0, column=0, padx=5)

        threshold_box, self.threshold_label = self.create_fixed_label(frame_bar, "Thresholded")
        threshold_box.grid(row=0, column=1, padx=5)

        # ---------- Center Frame ----------
        center_frame = tk.Frame(self.root, bg="white")
        center_frame.grid(row=1, column=1, padx=20, pady=20)

        self.score_display = Label(center_frame, text="Player: 0     Computer: 0", font=("Arial", 14), bg="white")
        self.score_display.pack()

        self.result_label = Label(center_frame, text="", font=("Arial", 18, "bold"), fg="red", bg="white")
        self.result_label.pack(pady=10)

        self.p_result_label = Label(center_frame, text="You:", font=("Arial", 14), bg="white")
        self.p_result_label.pack(pady=10)

        self.c_result_label = Label(center_frame, text="Computer:", font=("Arial", 14), bg="white")
        self.c_result_label.pack(pady=10)

        Button(center_frame, text="Play", font=("Arial", 12), width=15, bg="#E74C3C", fg="#ECF0F1",
               activebackground="#C0392B", command=self.play).pack(pady=8)
        Button(center_frame, text="Reset", font=("Arial", 12), width=15, bg="#F1C40F", fg="#2C3E50",
               activebackground="#D4AC0D", command=self.reset).pack(pady=8)
        Button(center_frame, text="Rule", font=("Arial", 12), width=15, command=show_rules).pack(pady=8)

        # ---------- Right Frame ----------
        right_frame = tk.Frame(self.root, bg="white")
        right_frame.grid(row=1, column=2, padx=20, pady=20)

        computer_frame = tk.Frame(right_frame, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg="black")
        computer_frame.pack()
        computer_frame.pack_propagate(False)

        self.image_label = Label(computer_frame, bg="lightgray", width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.image_label.pack()

    def update_video(self):
        frame_imgtk, self.num_frames, finger_count = self.detector.process(self.num_frames)
        if frame_imgtk:
            self.video_label.imgtk = frame_imgtk
            self.video_label.configure(image=frame_imgtk)

        if finger_count is not None:
            self.gesture_name = gesture_mapper(finger_count)
            self.p_result_label.config(text=f"YOU: {self.gesture_name}")
        self.root.after(10, self.update_video)

        @staticmethod
    def create_fixed_label(parent, caption_text):
        box = tk.Frame(parent, width=345, height=300, bg="white")
        box.pack_propagate(False)

        image_label = Label(box, bg="lightgray", width=345, height=260)
        image_label.pack()

        caption_label = Label(box, text=caption_text, font=("Arial", 15), bg="white")
        caption_label.pack()

        return box, image_label

    def update_video(self):
        frame_imgtk, self.num_frames, finger_count, gray, thresholded = self.detector.process(self.num_frames)

        if frame_imgtk:
            self.video_label.imgtk = frame_imgtk
            self.video_label.configure(image=frame_imgtk)

        if gray:
            self.greyscale_label.imgtk = gray
            self.greyscale_label.configure(image=gray)

        if thresholded:
            self.threshold_label.imgtk = thresholded
            self.threshold_label.configure(image=thresholded)

        if finger_count is not None:
            self.gesture_name = gesture_mapper(finger_count)
            self.p_result_label.config(text=f"You: {self.gesture_name}")

        self.root.after(10, self.update_video)

    def play(self):
        if not self.gesture_name or self.gesture_name not in CHOICES:
            self.result_label.config(text="Show a valid hand gesture!")
            return

        player = self.gesture_name
        computer = random.choice(CHOICES)
        self.c_result_label.config(text=f"Computer: {computer}")

        imgtk = random_pose(computer)
        if imgtk:
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)

        result, self.player_score, self.computer_score = game_round_result(
            player, computer, self.player_score, self.computer_score
        )

        self.result_label.config(text=result)
        self.update_score()

    def update_score(self):
        self.score_display.config(
            text=f"Player: {self.player_score}     Computer: {self.computer_score}"
        )

    def reset(self):
        self.result_label.config(text="")
        self.player_score = 0
        self.computer_score = 0
        self.update_score()
        self.image_label.config(image="")
        self.p_result_label.config(text="You:")
        self.c_result_label.config(text="Computer:")