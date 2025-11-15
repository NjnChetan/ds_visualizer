import os
from PIL import Image, ImageTk

def load_animation_frames(folder_path):
    """
    Load and return all animation frames from a folder as a list of PhotoImage objects.
    :param folder_path: The path to the folder containing animation frames.
    :return: A list of PhotoImage objects.
    """
    frame_files = sorted(os.listdir(folder_path))
    frames = []

    for frame in frame_files:
        if frame.endswith(".png"):  # Assuming all frames are in PNG format
            img = Image.open(os.path.join(folder_path, frame))
            frames.append(ImageTk.PhotoImage(img))
    return frames

def animate_frames(label, frames, delay=100):
    """
    Animate frames on a given Tkinter label.
    :param label: The Tkinter Label widget to display the animation.
    :param frames: List of PhotoImage frames to animate.
    :param delay: Delay between frames in milliseconds.
    """
    def update_frame():
        nonlocal frame_index
        label.config(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
        label.after(delay, update_frame)

    frame_index = 0
    update_frame()
