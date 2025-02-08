import tkinter as tk
import threading

# Global variables to hold references to each label widget, the window instance, and the canvas
board_squares = {}
board_items = {}
window = None  # This will hold the Tkinter window instance
bingo_thread = None  # This will hold the Bingo board thread instance
box_size = 150  # Set box size to be consistent and large
window_size = 800  # Increase window size to fit the board
board_size = 0
show_items = False

# Color configuration
bg_color = "white"
square_color = "white"
highlight_color = "green"
text_color = "black"


def get_square_name(row, col):
    return f"{chr(65 + row)}{col + 1}"


def get_row_item_name(row):
    return f"{chr(row)}1-{chr(row)}{board_size}"


def get_col_item_name(col):
    return f"A{col}-{chr(ord('A') + board_size - 1)}{col}"


def get_diag_item_name(major):
    if major:
        return f"A1-{chr(ord('A') + board_size - 1)}{board_size}"
    return f"{chr(ord('A') + board_size - 1)}1-A{board_size}"


def create_item_label(frame, item_name, row, col):
    label = tk.Label(
        frame, text=item_name, width=10, height=5,
        font=("Helvetica", 8), fg=text_color,
        wraplength=box_size - 40, justify='center'
    )
    label.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')  # Adjust sticky for resizing
    board_items[item_name] = label
    return label


def create_bingo_board():
    global window, bg_color, square_color, text_color
    global board_size

    # If the window already exists, just bring it to the front
    if window is not None:
        window.lift()  # Bring the existing window to the front
        return

    # Set effective parameters depending on whether items are shown or not
    # If item rewards are shown, add one row above, one row below, and one column to the right for item labels
    total_board_rows = board_size + 2 if show_items else board_size
    total_board_cols = board_size + 1 if show_items else board_size

    # Create a new window
    window = tk.Tk()
    window.title("Bingo Board")
    window.geometry(f"{window_size}x{window_size}")  # Set the window size
    window.configure(bg=bg_color)  # Set the window background color to the specified color

    # Create a frame for the Bingo board
    frame = tk.Frame(window, bg=bg_color)  # Set frame background to match window
    frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)  # Expand frame to fill the window

    # Configure grid weights for dynamic resizing
    for i in range(total_board_rows):
        frame.grid_rowconfigure(i, weight=1)  # Allow rows to expand
    for i in range(total_board_cols):
        frame.grid_columnconfigure(i, weight=1)  # Allow columns to expand

    # Initialize the board with placeholder labels based on board_size
    for i in range(board_size):
        for j in range(board_size):
            square_name = get_square_name(i, j)  # Create names like "A1", "A2", etc.
            label = tk.Label(
                frame, text=square_name, width=10, height=5,
                font=("Helvetica", 8), borderwidth=4, relief="groove",
                bg=square_color, fg=text_color, wraplength=box_size - 40,
                justify='center'
            )
            eff_i = i + 1 if show_items else i  # If items are shown, the first column will be taken by the item labels
            label.grid(row=eff_i, column=j, padx=10, pady=10, sticky='nsew')  # Adjust sticky for resizing
            board_squares[square_name] = label  # Store each label in the dictionary

    # If item rewards are shown, add placeholder labels for the items
    if show_items:
        # Rows
        for row in range(ord('A'), ord('A') + board_size):
            item_name = get_row_item_name(row)
            create_item_label(frame, item_name, row - 1, 5)
        # Columns
        for col in range(1, board_size + 1):
            item_name = get_col_item_name(col)
            create_item_label(frame, item_name, 6, col - 1)
        # Diagonals
        item_name = get_diag_item_name(True)
        create_item_label(frame, item_name, 6, 5)
        item_name = get_diag_item_name(False)
        create_item_label(frame, item_name, 0, 5)
        # All
        item_name = "ALL"
        create_item_label(frame, item_name, 0, 0)

    # Start the Tkinter main loop
    window.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window close event
    window.mainloop()


def on_closing():
    global window, bingo_thread

    # Quit the Tkinter main loop
    window.quit()  # This will exit the main loop
    window.destroy()  # Close the Tkinter window
    window = None  # Reset the window variable when closed
    bingo_thread = None  # Reset the bingo thread variable


def update_bingo_board(new_labels):
    global board_size

    # Ensure the new_labels list has the correct number of items based on board size
    expected_size = board_size * board_size  # Calculate the expected number of labels
    if len(new_labels) != expected_size:
        raise ValueError(f"The new_labels list must contain exactly {expected_size} items.")

    # Update each square with the new label
    for i, label_text in enumerate(new_labels):
        row = i // board_size  # Calculate the row based on board size
        col = i % board_size  # Calculate the column based on board size
        square_name = get_square_name(row, col)  # Create square name dynamically
        board_squares[square_name].config(text=label_text)  # Update the text of the label


def update_bingo_board_items(item_labels):
    global board_size

    # Ensure the item_labels list has the correct number of items based on board size
    expected_size = board_size * 4 + 5
    if len(item_labels) != expected_size:
        raise ValueError(f"The item_labels list must contain exactly {expected_size} items.")

    # Update each item with the new label
    # item_labels is in rows/cols/diags/all format
    # Rows
    for i in range(0, board_size * 2, 2):
        label_text = item_labels[i] + "\n" + item_labels[i + 1]
        row = i // 2
        item_name = get_row_item_name(row)
        board_items[item_name].config(text=label_text)
    # Columns
    for i in range(board_size * 2, board_size * 4, 2):
        label_text = item_labels[i] + "\n" + item_labels[i + 1]
        col = (board_size * 2) - (i // 2)
        item_name = get_col_item_name(col)
        board_items[item_name].config(text=label_text)
    # Diagonals
    for diag_type, i in enumerate([board_size * 4, board_size * 4 + 2]):
        label_text = item_labels[i] + "\n" + item_labels[i + 1]
        item_name = get_diag_item_name(diag_type == 0)
        board_items[item_name].config(text=label_text)
    # All
    label_text = item_labels[board_size * 4 + 4]
    board_items["ALL"].config(text=label_text)


def highlight_square(square_name):
    # Highlight a specific square in the specified highlight color
    if square_name in board_squares:
        board_squares[square_name].config(bg=highlight_color, fg=text_color)
    else:
        print(f"Square '{square_name}' not found on the board.")


# Function to run the Bingo board in a separate thread
def run_bingo_board(new_board_size, bg="white", sq_color="white", hl_color="green", txt_color="black",
                    auto_hint_items=False):
    global bingo_thread, board_size, bg_color, square_color, highlight_color, text_color, show_items

    # Set colors based on input parameters
    bg_color = bg
    square_color = sq_color
    highlight_color = hl_color
    text_color = txt_color

    # Set the board size and create the board if it doesn't exist
    board_size = new_board_size
    show_items = auto_hint_items
    if bingo_thread is None or not bingo_thread.is_alive():  # Check if the thread is not alive
        bingo_thread = threading.Thread(target=create_bingo_board)
        bingo_thread.start()
