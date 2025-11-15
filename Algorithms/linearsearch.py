import pygame as py
import customtkinter as ctk
from PIL import Image, ImageTk

# Initialize Pygame
py.init()

# Global Variables
is_paused = False
input_text = ''
search_target = None

# Constants
yellow = (205, 205, 0)  # Original yellow color
red = (255, 0, 0)       # Red color for comparisons
green = (0, 255, 0)     # Green color for found element
black = (0, 0, 0)
gray = (50, 50, 50)
white = (255, 255, 255)  # White color for text

w, h = 800, 600
pygame_surface = py.Surface((w, h))

# Variables
min_speed = 1           
max_speed = 1000
animation_speed = 500  # Default speed


py.font.init()
font = py.font.SysFont("Arial", 24)

# Visualization function
def visualize(l, compare_index=None, found_index=None, result_message=None):
    pygame_surface.fill(gray)  # Set gray background
    num_elements = len(l)
    if num_elements == 0:
        return  # No elements to visualize

    margin = 20  # Space between nodes
    node_width = 80  # Width of each node block (increased size for better visibility)
    node_height = 60  # Height of each node block (increased size)

    # Calculate available width for nodes and distribute them across the screen
    total_width = w - 80  # Subtract some padding from the window width
    node_spacing = total_width // num_elements

    for i in range(num_elements):
        # More nuanced color selection
        if found_index is not None and i == found_index:
            color = green  # Use green for the found element
        elif compare_index is not None and i == compare_index:
            color = red  # Use red for comparisons
        else:
            color = yellow  # Use yellow for normal nodes

        # Node position: Horizontally spaced across the screen
        node_x = 40 + i * node_spacing
        node_y = h // 2 - node_height // 2  # Vertically centered with the block height considered

        # Draw the rectangle (node block)
        py.draw.rect(pygame_surface, black, (node_x - 5, node_y - 5, node_width + 10, node_height + 10), border_radius=10)  # Border around block with rounded corners
        py.draw.rect(pygame_surface, color, (node_x, node_y, node_width, node_height), border_radius=10)  # Node block

        # Render the value text inside each block, white color for readability
        value_text = font.render(str(l[i]), True, white)
        text_rect = value_text.get_rect(center=(node_x + node_width // 2, node_y + node_height // 2))  # Centered inside block
        pygame_surface.blit(value_text, text_rect)

    # Render the comparison text if comparing elements
    if compare_index is not None:
        comparison_text = f"Comparing: {l[compare_index]}"
        comparison_render = font.render(comparison_text, True, white)
        comparison_rect = comparison_render.get_rect(center=(w // 2, 50))  # Positioned at the top-center
        pygame_surface.blit(comparison_render, comparison_rect)

    # Render the result message if provided
    if result_message:
        result_render = font.render(result_message, True, white)
        result_rect = result_render.get_rect(center=(w // 2, h - 50))  # Positioned at the bottom-center
        pygame_surface.blit(result_render, result_rect)

    render_pygame()

# Function to render Pygame surface inside CustomTkinter
def render_pygame():
    data = py.image.tostring(pygame_surface, "RGBA")
    image = Image.frombytes("RGBA", (w, h), data)
    photo = ImageTk.PhotoImage(image)
    pygame_label.configure(image=photo, text="")
    pygame_label.image = photo  # Prevent garbage collection

# Linear Search function
def linear_search(l):
    global is_paused

    def search_step(index):
        global is_paused

        if is_paused:
            app.after(100, search_step, index)
            return

        if index < len(l):
            visualize(l, compare_index=index)

            if l[index] == search_target:
                result_message = f"Found at position {index + 1}"  # +1 for 1-based indexing
                visualize(l, found_index=index, result_message=result_message)
                return  # Search complete
            else:
                app.after(int(animation_speed), search_step, index + 1)
        else:
            # Target not found
            result_message = "Not Found"
            visualize(l, result_message=result_message)
            pause_button.configure(text="Pause")

    search_step(0)


# Function to update the animation speed from the slider
def update_speed(value):
    global animation_speed
    # Invert the speed: higher slider value = lower speed (slower animation)
    animation_speed = max_speed - float(value) + min_speed


# Function to handle the start button
def start_searching():
    global input_text, search_target
    try:
        input_list = list(map(int, input_text.split(',')))
        search_target = int(search_entry.get())
        linear_search(input_list)
    except ValueError:
        input_entry.delete(0, ctk.END)
        search_entry.delete(0, ctk.END)

# Function to handle the pause button
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    pause_button.configure(text="Resume" if is_paused else "Pause")

# CustomTkinter GUI Setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Linear Search Visualizer")
app.geometry("1000x700")

# Frame for controls
control_frame = ctk.CTkFrame(app)
control_frame.pack(side="top", pady=10)

# Heading
head_label = ctk.CTkLabel(control_frame, text="Linear Search Visualizer", font=("Arial", 20, "bold"))
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

# Search target box
search_label = ctk.CTkLabel(control_frame, text="Enter target number:", font=("Arial", 16))
search_label.grid(row=2, column=0, padx=5)
search_entry = ctk.CTkEntry(control_frame, font=("Arial", 16), placeholder_text="e.g., 5", width=300)
search_entry.grid(row=2, column=1, padx=5)

# Slider for speed
speed_label = ctk.CTkLabel(control_frame, text="Animation Speed:", font=("Arial", 16))
speed_label.grid(row=3, column=0, padx=5)
speed_slider = ctk.CTkSlider(control_frame, from_=min_speed, to=max_speed, command=update_speed)
speed_slider.set(max_speed - animation_speed + min_speed)  # Initialize with the inverted value
speed_slider.grid(row=3, column=1, padx=5, pady=10)

# Button frame
button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

# Start button
start_button = ctk.CTkButton(button_frame, text="Start Searching", command=start_searching)
start_button.pack(side="left", padx=10)

# Pause button
pause_button = ctk.CTkButton(button_frame, text="Pause", command=toggle_pause)
pause_button.pack(side="left", padx=10)

# Pygame visualization
pygame_frame = ctk.CTkFrame(app)
pygame_frame.pack(side="bottom", pady=10)
pygame_label = ctk.CTkLabel(pygame_frame)
pygame_label.pack()

# Pygame update loop
def update_pygame():
    render_pygame()
    app.after(30, update_pygame)

update_pygame()

# Run the application
app.mainloop()
