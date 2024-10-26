import tkinter as tk
import threading

# Global variables to hold references to each label widget, the window instance, and the canvas
board_squares = {}
window = None  # This will hold the Tkinter window instance
bingo_thread = None  # This will hold the Bingo board thread instance
box_size = 150  # Set box size to be consistent and large
window_size = 800  # Increase window size to fit the board

def create_bingo_board():
    global window
    # If the window already exists, just bring it to the front
    if window is not None:
        window.lift()  # Bring the existing window to the front
        return

    # Create a new window
    window = tk.Tk()
    window.title("Bingo Board")
    window.geometry(f"{window_size}x{window_size}")  # Set the window size

    # Create a frame for the Bingo board
    frame = tk.Frame(window)
    frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)  # Expand frame to fill the window

    # Configure grid weights for dynamic resizing
    for i in range(5):
        frame.grid_rowconfigure(i, weight=1)  # Allow rows to expand
        frame.grid_columnconfigure(i, weight=1)  # Allow columns to expand

    # Initialize the board with placeholder labels
    for i in range(5):
        for j in range(5):
            square_name = f"{chr(65 + i)}{j + 1}"  # Create names like "A1", "A2", etc.
            label = tk.Label(frame, text=square_name, width=10, height=5, font=("Helvetica", 8),
                             borderwidth=4, relief="groove", bg="white", wraplength=box_size - 40,
                             justify='center')
            label.grid(row=i, column=j, padx=10, pady=10, sticky='nsew')  # Adjust sticky for resizing
            board_squares[square_name] = label  # Store each label in the dictionary

    # Start the Tkinter main loop
    window.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window close event
    window.mainloop()

def on_closing():
    global window
    window.destroy()
    window = None  # Reset the window variable when closed

def update_bingo_board(new_labels):
    # Ensure the new_labels list has exactly 25 items
    if len(new_labels) != 25:
        raise ValueError("The new_labels list must contain exactly 25 items.")

    # Update each square with the new label
    for i, label_text in enumerate(new_labels):
        square_name = f"{chr(65 + (i // 5))}{(i % 5) + 1}"  # Convert index to square name
        board_squares[square_name].config(text=label_text)  # Update the text of the label

def highlight_square(square_name):
    # Highlight a specific square in green
    if square_name in board_squares:
        board_squares[square_name].config(bg="green")
    else:
        print(f"Square '{square_name}' not found on the board.")


# Function to run the Bingo board in a separate thread
def run_bingo_board():
    global bingo_thread
    if bingo_thread is None or not bingo_thread.is_alive():  # Check if the thread is not alive
        bingo_thread = threading.Thread(target=create_bingo_board)
        bingo_thread.start()

run_bingo_board()  # Call this function to open the Bingo board
