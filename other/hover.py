import tkinter as tk
from PIL import ImageTk, Image

# Example student data
students = {
    'A1': {'name': 'Jane Doe', 'image': 'C:/Users/Dell/UsersDellSAAFRT/static/Jane_Doe.jfif'},
    'B2': {'name': 'John Doe', 'image': 'C:/Users/Dell/UsersDellSAAFRT/static/John_Doe.jfif'},
    # Add more students as needed
}

class Seat:
    def __init__(self, seat_number, row, column, occupied=False):
        self.seat_number = seat_number
        self.row = row
        self.column = column
        self.occupied = occupied
        self.color = "white"
        self.student_info = students.get(seat_number, None)

    def get_color(self):
        return "black" if self.occupied else "white"

    def get_image(self):
        if self.student_info:
            image = Image.open(self.student_info['image'])
            image = image.resize((100, 100)) # Resize as needed
            return ImageTk.PhotoImage(image)
        return None

def on_click(event):
    widget = event.widget
    seat = widget.seat
    if seat.student_info:
        print(f"Clicked on {seat.seat_number}: {seat.student_info['name']}")
        # Display additional information or image as needed

def on_enter(event):
    widget = event.widget
    seat = widget.seat
    if seat.student_info:
        print(f"Hovered over {seat.seat_number}: {seat.student_info['name']}")
        # Display additional information or image as needed

def on_leave(event):
    widget = event.widget
    seat = widget.seat
    if seat.student_info:
        print(f"Left {seat.seat_number}: {seat.student_info['name']}")
        # Hide additional information or image as needed

# Create the root window
root = tk.Tk()
root.title("Seating Arrangement")

# Example grid creation with spacing
rows = 30
columns = 20
spacing = 1 # Define spacing

for row in range(rows):
    for col in range(columns):
        # Adjust row and column indices to account for spacing
        adjusted_row = row * (spacing + 1)
        adjusted_col = col * (spacing + 1)
        
        seat_number = f"{chr(65 + row % 26)}{row // 26 + 1}" # Example seat numbering
        seat = Seat(seat_number, row, col, occupied=True) # Example occupied seat
        label = tk.Label(root, bg=seat.get_color(), width=2, height=1)
        label.grid(row=adjusted_row, column=adjusted_col)
        label.seat = seat # Store the Seat object for event handling
        label.bind("<Button-1>", on_click)
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)

# Configure grid to add spacing between rows and columns
for i in range(rows * (spacing + 1)):
    root.grid_rowconfigure(i, minsize=20) # Adjust the minsize as needed
    root.grid_columnconfigure(i, minsize=20) # Adjust the minsize as needed

root.mainloop()
