# Import required libraries
import random  # For generating random computer choices
import tkinter as tk  # For creating the GUI
from tkinter import Label, Button  # Specific Tkinter widgets used

# Import constants and utility functions from other modules
from constants import ROI, FRAME_SIZE, CHOICES, FRAME_WIDTH, FRAME_HEIGHT  # Constants for game settings
from src import GestureDetector, show_rules  # Gesture detection and rules display
from utils import gesture_mapper, random_pose, game_round_result  # Utility functions for game logic


# Define the main GUI class for the Rock Paper Scissors Lizard Spock game
class RPSGui:
    def __init__(self, root):
        # Initialize the main Tkinter window
        self.root = root
        self.root.title("Rock Paper Scissors Lizard Spock")  # Set window title
        self.root.configure(bg="white")  # Set background color to white

        # Initialize GUI widget references (to be set in build_layout)
        self.video_label: Label | None = None  # Label for webcam video feed
        self.greyscale_label: Label | None = None  # Label for greyscale image
        self.score_display: Label | None = None  # Label for displaying scores
        self.threshold_label: Label | None = None  # Label for thresholded image
        self.result_label: Label | None = None  # Label for game result
        self.p_result_label: Label | None = None  # Label for player's gesture
        self.c_result_label: Label | None = None  # Label for computer's gesture
        self.image_label: Label | None = None  # Label for computer's gesture image

        # Initialize game state variables
        self.player_score = 0  # Player's score
        self.computer_score = 0  # Computer's score
        self.num_frames = 0  # Frame counter for video processing
        self.gesture_name = None  # Current detected player gesture

        # Build the GUI layout and start video processing
        self.build_layout()  # Set up the GUI components
        self.detector = GestureDetector(ROI, FRAME_SIZE)  # Initialize gesture detector
        self.update_video()  # Start the video feed update loop

    def build_layout(self):
        # ---------- Title ----------
        # Create and place the game title at the top
        Label(self.root, text="RPSL Game", font=("Arial", 20, "bold"), bg="white") \
            .grid(row=0, column=0, columnspan=3, pady=(20, 10))

        # ---------- Left Frame ----------
        # Create a frame for the webcam feed and processed images
        left_frame = tk.Frame(self.root, bg="white")
        left_frame.grid(row=1, column=0, padx=20, pady=20)

        # Create a container for the webcam video feed
        main_frame = tk.Frame(left_frame, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg="black")
        main_frame.pack()

        # Initialize the video feed label
        self.video_label = Label(main_frame, bg="lightgray", width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.video_label.pack()

        # Create a frame for greyscale and thresholded images
        frame_bar = tk.Frame(left_frame, bg="white")
        frame_bar.pack(pady=15)

        # Create and place greyscale image label
        greyscale_box, self.greyscale_label = self.create_fixed_label(frame_bar, "Grayscale")
        greyscale_box.grid(row=0, column=0, padx=5)

        # Create and place thresholded image label
        threshold_box, self.threshold_label = self.create_fixed_label(frame_bar, "Thresholded")
        threshold_box.grid(row=0, column=1, padx=5)

        # ---------- Center Frame ----------
        # Create a frame for score, results, and control buttons
        center_frame = tk.Frame(self.root, bg="white")
        center_frame.grid(row=1, column=1, padx=20, pady=20)

        # Initialize and place the score display label
        self.score_display = Label(center_frame, text="Player: 0     Computer: 0", font=("Arial", 14), bg="white")
        self.score_display.pack()

        # Initialize and place the game result label
        self.result_label = Label(center_frame, text="", font=("Arial", 18, "bold"), fg="red", bg="white")
        self.result_label.pack(pady=10)

        # Initialize and place the player's gesture label
        self.p_result_label = Label(center_frame, text="You:", font=("Arial", 14), bg="white")
        self.p_result_label.pack(pady=10)

        # Initialize and place the computer's gesture label
        self.c_result_label = Label(center_frame, text="Computer:", font=("Arial", 14), bg="white")
        self.c_result_label.pack(pady=10)

        # Create and place the "Play" button to start a game round
        Button(center_frame, text="Play", font=("Arial", 12), width=15, bg="#E74C3C", fg="#ECF0F1",
               activebackground="#C0392B", command=self.play).pack(pady=8)
        # Create and place the "Reset" button to reset the game
        Button(center_frame, text="Reset", font=("Arial", 12), width=15, bg="#F1C40F", fg="#2C3E50",
               activebackground="#D4AC0D", command=self.reset).pack(pady=8)
        # Create and place the "Rule" button to show game rules
        Button(center_frame, text="Rule", font=("Arial", 12), width=15, command=show_rules).pack(pady=8)

        # ---------- Right Frame ----------
        # Create a frame for the computer's gesture image
        right_frame = tk.Frame(self.root, bg="white")
        right_frame.grid(row=1, column=2, padx=20, pady=20)

        # Create a container for the computer's gesture image
        computer_frame = tk.Frame(right_frame, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg="black")
        computer_frame.pack()
        computer_frame.pack_propagate(False)  # Prevent frame from resizing

        # Initialize the computer's gesture image label
        self.image_label = Label(computer_frame, bg="lightgray", width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.image_label.pack()

    @staticmethod
    def create_fixed_label(parent, caption_text):
        # Create a fixed-size frame for an image and its caption
        box = tk.Frame(parent, width=345, height=300, bg="white")
        box.pack_propagate(False)  # Prevent frame from resizing

        # Create an image label within the frame
        image_label = Label(box, bg="lightgray", width=345, height=260)
        image_label.pack()

        # Create a caption label below the image
        caption_label = Label(box, text=caption_text, font=("Arial", 15), bg="white")
        caption_label.pack()

        return box, image_label  # Return the frame and image label

    def update_video(self):
        # Process the next video frame and update the GUI
        frame_imgtk, self.num_frames, finger_count, gray, thresholded = self.detector.process(self.num_frames)

        # Update the webcam feed if a new frame is available
        if frame_imgtk:
            self.video_label.imgtk = frame_imgtk
            self.video_label.configure(image=frame_imgtk)

        # Update the greyscale image if available
        if gray:
            self.greyscale_label.imgtk = gray
            self.greyscale_label.configure(image=gray)

        # Update the thresholded image if available
        if thresholded:
            self.threshold_label.imgtk = thresholded
            self.threshold_label.configure(image=thresholded)

        # Update the player's gesture label if a gesture is detected
        if finger_count is not None:
            self.gesture_name = gesture_mapper(finger_count)
            self.p_result_label.config(text=f"You: {self.gesture_name}")

        # Schedule the next video frame update (every 10ms)
        self.root.after(10, self.update_video)

    def play(self):
        # Handle a game round when the "Play" button is clicked
        # Check if a valid gesture is detected
        if not self.gesture_name or self.gesture_name not in CHOICES:
            self.result_label.config(text="Show a valid hand gesture!")
            return

        # Get the player's and computer's gestures
        player = self.gesture_name
        computer = random.choice(CHOICES)  # Randomly select computer's gesture
        self.c_result_label.config(text=f"Computer: {computer}")  # Update computer's gesture label

        # Display the computer's gesture image
        imgtk = random_pose(computer)
        if imgtk:
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)

        # Determine the game result and update scores
        result, self.player_score, self.computer_score = game_round_result(
            player, computer, self.player_score, self.computer_score
        )

        # Update the result label and scores
        self.result_label.config(text=result)
        self.update_score()

    def update_score(self):
        # Update the score display with current player and computer scores
        self.score_display.config(
            text=f"Player: {self.player_score}     Computer: {self.computer_score}"
        )

    def reset(self):
        # Reset the game state and clear the GUI
        self.result_label.config(text="")  # Clear result text
        self.player_score = 0  # Reset player score
        self.computer_score = 0  # Reset computer score
        self.update_score()  # Update score display
        self.image_label.config(image="")  # Clear computer's gesture image
        self.p_result_label.config(text="You:")  # Clear player's gesture label
        self.c_result_label.config(text="Computer:")  # Clear computer's gesture label