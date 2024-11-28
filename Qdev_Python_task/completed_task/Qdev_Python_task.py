import csv
import tkinter as tk
from tkinter import filedialog

def process_file(file_path):
    # Initialize counters and storage
    occurrences = {'Red': 0, 'Yellow': 0, 'Green': 0}
    durations = {'Red': 0, 'Yellow': 0, 'Green': 0}
    green_times = []  # List to store times when Green was active
    complete_cycles = 0
    mistake_lines = 0
    
    previous_state = None  # To track the state for detecting complete cycles
    cycle_state = []  # To track the sequence of states for cycle detection
    
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                # Extract values safely (default to 0 if the column is missing)
                red = int(row.get('Red', 0))
                yellow = int(row.get('Yellow', 0))
                green = int(row.get('Green', 0))
                time_active = int(row.get('TimeActive', 0))
                time = row.get('Time', '')

                # Check if multiple colours are active at the same time or no colours
                if (red + yellow + green) > 1 or (red + yellow + green) == 0:
                    mistake_lines += 1
                
                # Count occurrences and sum durations
                if red:
                    occurrences['Red'] += 1
                    durations['Red'] += time_active
                if yellow:
                    occurrences['Yellow'] += 1
                    durations['Yellow'] += time_active
                if green:
                    occurrences['Green'] += 1
                    durations['Green'] += time_active
                    green_times.append(time)  # Store green times

                # Detect complete cycles: Red -> Yellow -> Green -> Yellow -> Red
                if red:
                    cycle_state.append('Red')
                elif yellow:
                    cycle_state.append('Yellow')
                elif green:
                    cycle_state.append('Green')

                if len(cycle_state) >= 5 and cycle_state[-5:] == ['Red', 'Yellow', 'Green', 'Yellow', 'Red']:
                    complete_cycles += 1
                    cycle_state = []

        # Display results in a pop-up
        display_results(occurrences, durations, green_times, complete_cycles, mistake_lines)

    except Exception as e:
        display_error(f"Error processing the file:\n{e}")

def display_results(occurrences, durations, green_times, complete_cycles, mistake_lines):
    # Create a centered pop-up window
    popup = tk.Toplevel()
    popup.title("Results")
    popup.geometry("600x400")  # Adjust width and height as needed
    popup.resizable(True, True)  # Allow resizing

    # Center the pop-up on the screen
    popup.update_idletasks()
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    window_width = 600
    window_height = 400
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Results string
    results = (
        f"Occurrences:\n"
        f"  Red: {occurrences['Red']}\n"
        f"  Yellow: {occurrences['Yellow']}\n"
        f"  Green: {occurrences['Green']}\n\n"
        f"Durations (seconds):\n"
        f"  Red: {durations['Red']} seconds\n"
        f"  Yellow: {durations['Yellow']} seconds\n"
        f"  Green: {durations['Green']} seconds\n\n"
        f"Complete Cycles (Red-Yellow-Green-Yellow-Red):\n"
        f"  {complete_cycles}\n\n"
        f"Mistake Lines (Multiple colours active or no colours):\n"
        f"  {mistake_lines}"
    )

    # Add results label with wrapping
    label = tk.Label(popup, text=results, justify="left", anchor="w", padx=20, pady=20)
    label.pack(expand=True, fill="both")

    # Create a canvas for Green Times with a scrollbar
    canvas = tk.Canvas(popup)
    scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the Green Times labels
    green_frame = tk.Frame(canvas)

    # Add Green Times labels to the frame
    green_times_label = tk.Label(green_frame, text="Green Times:\n" + "\n".join(green_times), justify="left", anchor="w", padx=20, pady=20, wraplength=550)
    green_times_label.pack()

    # Place the frame inside the canvas
    canvas.create_window((0, 0), window=green_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Update the canvas scroll region
    green_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def display_error(message):
    # Create a centered error pop-up window
    popup = tk.Toplevel()
    popup.title("Error")
    popup.geometry("500x200")  # Adjust size as needed
    popup.resizable(True, True)  # Allow resizing

    # Center the pop-up
    popup.update_idletasks()
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    window_width = 500
    window_height = 200
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Add content to the pop-up
    label = tk.Label(popup, text=message, justify="center", padx=20, pady=20, fg="red")
    label.pack(expand=True, fill="both")

def open_file():
    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select a Traffic Data File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:
        process_file(file_path)

# Create the main GUI window
root = tk.Tk()
root.title("Traffic Light Data Processor")
root.geometry("300x200")  # Main window size

# Center the main window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 350
window_height = 100
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Add a button to select and open a file
button = tk.Button(root, text="Choose File and Process", command=open_file, padx=20, pady=10)
button.pack(pady=20)

# Run the application
root.mainloop()