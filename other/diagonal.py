import tkinter as tk

# Define the grid size
rows = 30
columns = 20
# Define colors for occupied and unoccupied seats
occupied_color = 'red'
unoccupied_color = 'white'

# Create the root window
root = tk.Tk()
root.title("Diagonal Occupied Seats")

# Function to determine the color of a seat based on its position
def get_color(row, col):
    # The first tile of each row starts with a different color
    if col == 0:
        # Alternate between red and white starting from the first row
        return occupied_color if row % 2 == 0 else unoccupied_color
    else:
        # For the rest of the tiles, alternate between the starting tile's color and a different color
        return occupied_color if (row + col) % 2 == 0 else unoccupied_color

# Create the grid
for row in range(rows):
    for col in range(columns):
        color = get_color(row, col)
        label = tk.Label(root, bg=color, width=2, height=1)
        label.grid(row=row, column=col)

# Run the Tkinter event loop
root.mainloop()
