import pygame as py
import customtkinter as ctk
from PIL import Image, ImageTk

# Initialize Pygame
py.init()

# Global Variables
is_paused = False
input_text = ''

# Constants
yellow = (205, 205, 0)  # Original yellow color
red = (255, 0, 0)       # Red color for comparisons
green = (0, 255, 0)     # Green color for swaps
black = (0, 0, 0)
gray = (50, 50, 50)

w, h = 800, 600
pygame_surface = py.Surface((w, h))

min_speed = 1           
max_speed = 1000
animation_speed = 500  # Default speed

def set_animation_speed(slider_value):
    global animation_speed
    # Invert the logic: sliding left decreases animation speed, sliding right increases it
    animation_speed = min_speed + (max_speed - slider_value)

# Set up font for rendering text
font = py.font.Font(None, 36)  # Default font and size

# Visualization function
def visualize(l, compare_indices=None, swap_indices=None):
    pygame_surface.fill(gray)  # Set gray background
    num_elements = len(l)
    if num_elements == 0:
        return  # No elements to visualize

    margin = 2  # Space between bars
    rect_width = ((w - 40) // num_elements) - margin  # Leave some padding and add margin

    max_value = max(l) if max(l) > 0 else 1

    for i in range(num_elements):
        # More nuanced color selection
        if compare_indices and i in compare_indices:
            color = red  # Use red for comparisons
        elif swap_indices and i in swap_indices:
            color = green  # Use green for swaps
        else:
            color = yellow  # Use yellow for normal bars

        scaled_height = (l[i] / max_value) * (h - 50)
        bar_rect = py.Rect(
            20 + i * (rect_width + margin),
            h - 30 - scaled_height,
            rect_width,
            scaled_height,
        )
        
        # Draw the bar
        py.draw.rect(pygame_surface, color, bar_rect)

        # Render the value inside the bar
        value_text = font.render(str(l[i]), True, black)
        text_rect = value_text.get_rect(center=bar_rect.center)
        pygame_surface.blit(value_text, text_rect)

    render_pygame()

# Function to render Pygame surface inside CustomTkinter
def render_pygame():
    data = py.image.tostring(pygame_surface, "RGBA")
    image = Image.frombytes("RGBA", (w, h), data)
    photo = ImageTk.PhotoImage(image)
    pygame_label.configure(image=photo, text="")
    pygame_label.image = photo  # Prevent garbage collection

# Bubble Sort function
def bubble_sort(l):
    global is_paused  # Use global to modify the pause state

    def sort_step(i, j):
        global is_paused
        
        if is_paused:
            app.after(100, sort_step, i, j)
            return

        if j < len(l) - 1 - i:
            # Softer, more controlled comparison visualization
            visualize(l, compare_indices=(j, j + 1))
            
            # Introduce a small delay before checking for a swap
            app.after(int(animation_speed), check_swap, i, j)
        elif i < len(l) - 1:
            app.after(int(animation_speed), sort_step, i + 1, 0)
        else:
            # Sorting complete
            visualize(l)
            # Reset pause state when sorting is complete
            is_paused = False
            pause_button.configure(text="Pause")

    def check_swap(i, j):
        if l[j] > l[j + 1]:
            l[j], l[j + 1] = l[j + 1], l[j]
            visualize(l, swap_indices=(j, j + 1))
        
        # Continue to the next step
        app.after(int(animation_speed), sort_step, i, j + 1)

    sort_step(0, 0)

# Selection Sort function
def selection_sort(l):
    global is_paused  # Use global to modify the pause state

    def sort_step(i, j, min_index):
        global is_paused

        if is_paused:
            app.after(100, sort_step, i, j, min_index)
            return

        if j < len(l):
            # Softer, more controlled comparison visualization
            visualize(l, compare_indices=(j, min_index))

            # Update min_index if a smaller element is found
            if l[j] < l[min_index]:
                min_index = j

            # Continue to the next element in the unsorted portion
            app.after(int(animation_speed), sort_step, i, j + 1, min_index)
        elif i < len(l) - 1:
            # Swap the minimum element with the first element of the unsorted portion
            if min_index != i:
                l[i], l[min_index] = l[min_index], l[i]
                visualize(l, swap_indices=(i, min_index))

            # Move to the next position in the list
            app.after(int(animation_speed), sort_step, i + 1, i + 1, i + 1)
        else:
            # Sorting complete
            visualize(l)
            # Reset pause state when sorting is complete
            is_paused = False
            pause_button.configure(text="Pause")

    sort_step(0, 1, 0)

# Insertion Sort function
def insertion_sort(l):
    global is_paused  # Use global to modify the pause state

    def sort_step(i):
        global is_paused
        
        if is_paused:
            app.after(100, sort_step, i)
            return

        if i < len(l):
            visualize(l, compare_indices=[i])
            app.after(int(animation_speed), insert_step, i)
        else:
            # Sorting complete
            visualize(l)
            # Reset pause state when sorting is complete
            is_paused = False
            pause_button.configure(text="Pause")

    def insert_step(i):
        if i == 0:  # No need to do anything for the first element
            app.after(int(animation_speed), sort_step, i + 1)
            return
        
        key = l[i]
        j = i - 1
        
        # Shift elements to the right to create space for the key
        while j >= 0 and l[j] > key:
            l[j + 1] = l[j]
            visualize(l, compare_indices=[j, j + 1])  # Visualize the comparison
            j -= 1

        # Place the key in its correct position
        l[j + 1] = key
        visualize(l, swap_indices=[j + 1, i])  # Visualize the swap

        # Continue to the next step
        app.after(int(animation_speed), sort_step, i + 1)

    sort_step(1)  # Start from the second element

# Function to update the animation speed from the slider
def update_speed(value):
    global animation_speed
    slider_value = float(value)
    set_animation_speed(slider_value)
    print(f"Speed updated to: {animation_speed}")

# Function to handle the start button
def start_sorting():
    global input_text
    try:
        input_list = list(map(int, input_text.split(',')))
        if selected_sort.get() == "Bubble Sort":
            bubble_sort(input_list)
        elif selected_sort.get() == "Selection Sort":
            selection_sort(input_list)
        else:
            insertion_sort(input_list)
    except ValueError:
        input_entry.delete(0, ctk.END)

# Function to handle the pause button
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    pause_button.configure(text="Resume" if is_paused else "Pause")

# CustomTkinter GUI Setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sorting Visualizer")
app.geometry("1000x700")

# Frame for controls
control_frame = ctk.CTkFrame(app)
control_frame.pack(side="top", pady=10)

# Heading
head_label = ctk.CTkLabel(control_frame, text="Sorting Visualizer", font=("Arial", 20, "bold"))
head_label.grid(row=0, column=0, padx=8, pady=10, columnspan=2)

# Input box
input_label = ctk.CTkLabel(control_frame, text="Enter numbers (comma-separated):", font=("Arial", 16))
input_label.grid(row=1, column=0, padx=5)
input_entry = ctk.CTkEntry(control_frame, font=("Arial", 16), placeholder_text="e.g., 3,5,2,8,1", width=300)
input_entry.grid(row=1, column=1, padx=5)

def on_input_change(event):
    global input_text
    input_text = input_entry.get()

input_entry.bind("<KeyRelease>", on_input_change)

# Dropdown for sorting algorithm selection
selected_sort = ctk.StringVar(value="Bubble Sort")
sort_dropdown = ctk.CTkOptionMenu(control_frame, variable=selected_sort, values=["Bubble Sort", "Insertion Sort", "Selection Sort"])
sort_dropdown.grid(row=2, column=0, padx=5)

# Speed slider
speed_slider = ctk.CTkSlider(control_frame, from_=min_speed, to=max_speed, number_of_steps=max_speed, command=update_speed)
speed_slider.set(500)
speed_slider.grid(row=2, column=1, padx=5)

# Start button
start_button = ctk.CTkButton(control_frame, text="Start Sorting", font=("Arial", 16), command=start_sorting)
start_button.grid(row=3, column=0, padx=5)

# Pause button
pause_button = ctk.CTkButton(control_frame, text="Pause", font=("Arial", 16), command=toggle_pause)
pause_button.grid(row=3, column=1, padx=5)

# Pygame Label for displaying the sorting animation
pygame_label = ctk.CTkLabel(app)
pygame_label.pack(padx=20, pady=10)

# Start the Tkinter main loop
app.mainloop()
