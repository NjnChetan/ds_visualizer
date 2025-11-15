import tkinter as tk
from utils import load_animation_frames, animate_frames
from sorting_visualizer import open_sorting
from searching_visualizer import open_searching

# Create the main Tkinter window
root = tk.Tk()
root.title("Algorithm Visualizer")
root.geometry("1000x600")
root.resizable(True, True)

# Colors and Fonts
bg_color = "#f0f8ff"  # Light blue background
font_title = ("Arial", 28, "bold")
font_intro = ("Arial", 14, "italic")

# Set background color
root.configure(bg=bg_color)

# Main Title Label
title_label = tk.Label(root, text="Algorithm Visualizer", font=font_title, fg="blue", bg=bg_color)
title_label.pack(pady=20)

# Introductaion Text
intro_text = tk.Label(
    root,
    text="Welcome to the Algorithm Visualizer!\nHere, you can explore different sorting and searching algorithms through interactive visualizations.",
    font=font_intro,
    fg="black",
    bg=bg_color,
    justify="center",
    padx=20,
    pady=10,
)
intro_text.pack(pady=10)

# Home Frame (Landing Page)
home_frame = tk.Frame(root, bg=bg_color)
home_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

# Sorting Visualizer Box
sorting_box = tk.Frame(home_frame, bg="#90ee90", bd=5, relief="ridge", width=400, height=300)
sorting_box.pack(side=tk.LEFT, padx=20, pady=20, expand=True, fill=tk.BOTH)

# Sorting Box Title
sorting_title = tk.Label(sorting_box, text="Sorting Visualizer", font=("Arial", 16, "bold"), bg="#90ee90", fg="black")
sorting_title.pack(pady=10)

# Sorting Animation Label
sorting_label = tk.Label(sorting_box, bg="#90ee90")
sorting_label.pack(expand=True, fill=tk.BOTH)

# Load and Animate Sorting Frames
sorting_frames = load_animation_frames("animation_frames/sorting_frames")
animate_frames(sorting_label, sorting_frames)

# Sorting Button
sorting_button = tk.Button(sorting_box, text="Open", font=("Arial", 14), command=open_sorting, bg="white", fg="black")
sorting_button.pack(pady=10)

# Searching Visualizer Box
searching_box = tk.Frame(home_frame, bg="#add8e6", bd=5, relief="ridge", width=400, height=300)
searching_box.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)

# Searching Box Title
searching_title = tk.Label(searching_box, text="Searching Visualizer", font=("Arial", 16, "bold"), bg="#add8e6", fg="black")
searching_title.pack(pady=10)

# Searching Animation Label
searching_label = tk.Label(searching_box, bg="#add8e6")
searching_label.pack(expand=True, fill=tk.BOTH)

# Load and Animate Searching Frames
searching_frames = load_animation_frames("animation_frames/searching_frames")
animate_frames(searching_label, searching_frames)

# Searching Button
searching_button = tk.Button(searching_box, text="Open", font=("Arial", 14), command=open_searching, bg="white", fg="black")
searching_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
