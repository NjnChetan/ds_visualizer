import tkinter as tk
from tkinter import simpledialog
import pygame
import sys

def open_searching():
    searching_window = tk.Toplevel()
    searching_window.title("Searching Visualizer")
    searching_window.geometry("1000x600")

    # Heading for Searching Visualizer
    searching_label = tk.Label(searching_window, text="Searching Visualizer", font=("Arial", 24))
    searching_label.pack(pady=20)

    # Instructions
    instructions_label = tk.Label(searching_window, text="Select a searching algorithm to visualize:", font=("Arial", 14))
    instructions_label.pack(pady=10)

    # Linear Search Button
    linear_search_button = tk.Button(
        searching_window, 
        text="Linear Search", 
        font=("Arial", 14), 
        command=lambda: visualize_search("Linear Search")
    )
    linear_search_button.pack(pady=10)

    # Binary Search Button
    binary_search_button = tk.Button(
        searching_window, 
        text="Binary Search", 
        font=("Arial", 14), 
        command=lambda: visualize_search("Binary Search")
    )
    binary_search_button.pack(pady=10)

    # Back Button
    back_button = tk.Button(searching_window, text="Back to Home", font=("Arial", 14), command=searching_window.destroy)
    back_button.pack(pady=20)

def visualize_search(search_type):
    """
    Opens a window to input array and value, then visualizes the searching algorithm using Pygame.
    """
    # Ask user for array input
    array_input = simpledialog.askstring("Input Array", "Enter a list of numbers separated by commas (e.g., 1, 2, 3, 4):")
    if not array_input:
        return

    # Parse the array
    try:
        array = [int(x.strip()) for x in array_input.split(",")]
    except ValueError:
        tk.messagebox.showerror("Invalid Input", "Please enter a valid list of integers.")
        return

    # Ask user for the value to search
    target = simpledialog.askinteger("Search Value", "Enter the value to search for:")
    if target is None:
        return

    # Call Pygame visualization
    if search_type == "Linear Search":
        linear_search_visualization(array, target)
    elif search_type == "Binary Search":
        binary_search_visualization(array, target)

def linear_search_visualization(array, target):
    """
    Visualizes Linear Search using Pygame with detailed step-by-step instructions
    and algorithm information.
    """
    pygame.init()
    width, height = 800, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Linear Search Visualization")

    font = pygame.font.Font(None, 36)
    info_font = pygame.font.Font(None, 28)
    clock = pygame.time.Clock()

    element_width = width // len(array)
    highlighted = -1
    found = False
    steps = 0

    running = True
    while running:
        screen.fill((30, 30, 30))

        # Draw the array elements
        for i, value in enumerate(array):
            color = (255, 0, 0) if i == highlighted else (0, 255, 0)
            pygame.draw.rect(
                screen,
                color,
                (i * element_width + 5, height // 2 - 50, element_width - 10, 100),
            )
            text = font.render(str(value), True, (255, 255, 255))
            screen.blit(
                text,
                (
                    i * element_width + element_width // 2 - text.get_width() // 2,
                    height // 2 - 30,
                ),
            )

        # Display algorithm progress
        progress_text = f"Step {steps}: Checking index {highlighted}" if highlighted >= 0 else "Starting search..."
        progress_display = info_font.render(progress_text, True, (255, 255, 255))
        screen.blit(progress_display, (20, 20))

        # Display search result
        if found:
            result_text = f"Found {target} at index {highlighted}"
            result_display = info_font.render(result_text, True, (0, 255, 0))
            screen.blit(result_display, (20, 60))
            running = False
        elif highlighted == len(array) - 1 and not found:
            result_text = f"{target} not found in the array"
            result_display = info_font.render(result_text, True, (255, 0, 0))
            screen.blit(result_display, (20, 60))
            running = False

        # Display time complexity
        complexity_text = "Time Complexity: O(n)"
        complexity_display = info_font.render(complexity_text, True, (255, 255, 255))
        screen.blit(complexity_display, (20, 100))

        pygame.display.flip()

        # Simulate the search step-by-step
        if not found and highlighted < len(array) - 1:
            highlighted += 1
            steps += 1
            if array[highlighted] == target:
                found = True
        else:
            pygame.time.wait(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(2)  # Limit to 60 FPS

    pygame.time.wait(2000)  # Pause to allow user to see the result
    pygame.quit()


def binary_search_visualization(array, target):
    """
    Visualizes Binary Search using Pygame.
    """
    pygame.init()
    width, height = 800, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Binary Search Visualization")

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    array.sort()
    low, high = 0, len(array) - 1
    mid = -1

    running = True
    while running:
        screen.fill((30, 30, 30))

        # Draw the array
        for i, value in enumerate(array):
            color = (0, 0, 255) if i == mid else (0, 255, 0)
            pygame.draw.rect(
                screen,
                color,
                (i * width // len(array) + 5, height // 2 - 50, width // len(array) - 10, 100),
            )
            text = font.render(str(value), True, (255, 255, 255))
            screen.blit(text, (i * width // len(array) + (width // len(array)) // 2 - text.get_width() // 2, height // 2))

        pygame.display.flip()

        # Simulate binary search step-by-step
        if low <= high:
            mid = (low + high) // 2
            if array[mid] == target:
                print(f"Found {target} at index {mid}")
                pygame.time.wait(1000)
                running = False
            elif array[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        else:
            print(f"{target} not found in the array")
            pygame.time.wait(1000)
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(2)

    pygame.quit()