import tkinter as tk

# Define the grid size
rows = 4
columns = 3

# Define colors for occupied and unoccupied seats
occupied_color = 'red'
unoccupied_color = 'white'

# Create the root window
root = tk.Tk()
root.title("Diagonal Occupied Seats")

# Function to determine if a seat is occupied
def is_occupied(row, col):
    # Define the occupied seats
    occupied_seats = [(0, 0), (1, 1), (2, 2), (3, 1), (3, 0), (0, 2)]
    return (row, col) in occupied_seats

# Create the grid
for row in range(rows):
    for col in range(columns):
        color = occupied_color if is_occupied(row, col) else unoccupied_color
        label = tk.Label(root, bg=color, width=2, height=1)
        label.grid(row=row, column=col)

# Run the Tkinter event loop
root.mainloop()
