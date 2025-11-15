import tkinter as tk

def open_sorting():
    sorting_window = tk.Toplevel()
    sorting_window.title("Sorting Visualizer")
    sorting_window.geometry("1000x600")

    # Add sorting options (Example: Bubble Sort, Quick Sort, etc.)
    sorting_label = tk.Label(sorting_window, text="Sorting Visualizer", font=("Arial", 24))
    sorting_label.pack(pady=20)

    # Back Button
    back_button = tk.Button(sorting_window, text="Back to Home", command=sorting_window.destroy)
    back_button.pack(pady=20)
