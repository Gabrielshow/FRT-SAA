import tkinter as tk

# Define the grid size
rows = 30
columns = 20

# Define colors for occupied and unoccupied seats
occupied_color = 'red'
unoccupied_color = 'white'

# Create the root window
root = tk.Tk()
root.title("Two Empty Spaces")

# Function to determine the color of a seat based on its position
def get_color(row, col):
    # The first tile of each row is always occupied
    if col == 0:
        return occupied_color
    # Every occupied seat is followed by two unoccupied seats
    elif col % 3 == 0:
        return occupied_color
    else:
        return unoccupied_color

# Create the grid
for row in range(rows):
    for col in range(columns):
        color = get_color(row, col)
        label = tk.Label(root, bg=color, width=2, height=1)
        label.grid(row=row, column=col)

# Run the Tkinter event loop
root.mainloop()
