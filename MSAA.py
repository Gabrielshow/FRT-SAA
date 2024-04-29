import sys
import tkinter as tk
from tkinter import ttk
import json
import math
import tkinter.simpledialog as sd

class Seat:
    def __init__(self, seat_number, row, column, level, occupied=False):
        self.seat_number = seat_number
        self.row = row
        self.column = column
        self.level = level  # Add level attribute
        self.occupied = occupied
        self.color = "white"  # Default color

class SeatGrid:
    def __init__(self, rows, columns, spacing=2, seating_patterns=None):
        self.rows = rows
        self.columns = columns
        self.space = spacing
        self.seating_patterns = seating_patterns  # Dictionary of seating patterns for each level

    def apply_seating_patterns(self):
        for level, pattern in self.seating_patterns.items():
            pattern.apply_pattern(self.seat_grid)

class TwoEmptySpacesPattern:
    def apply_pattern(self, seat_grid):
        for i in range(len(seat_grid)):
            for j in range(len(seat_grid[i])):
                seat = seat_grid[i][j]
                # The first tile of each row is always occupied
                if j == 0:
                    seat.occupied = True
                    seat.set_color("yellow") # Example color for occupied seats
                # Every occupied seat is followed by two unoccupied seats
                elif j % 3 == 0:
                    seat.occupied = True
                    seat.set_color("yellow")
                else:
                    seat.occupied = False
                    seat.set_color("white")


class NormalPattern:
    def apply_pattern(self, seat_grid):
        for i in range(len(seat_grid)):
            for j in range(len(seat_grid[i])):
                seat = seat_grid[i][j]
                if i == 0 and j % 2 == 0:
                    seat.occupied = True
                    seat.color = "blue"
                    
class ChessBoardPattern:
    def apply_pattern(self, seat_grid):
        for i in range(len(seat_grid)):
            for j in range(len(seat_grid[i])):
                seat = seat_grid[i][j]
                # The first tile of each row starts with a different color
                if j == 0:
                    # Alternate between red and white starting from the first row
                    seat.set_color("red") if i % 2 == 0 else seat.set_color("white")
                else:
                    # For the rest of the tiles, alternate between the starting tile's color and a different color
                    seat.set_color("red") if (i + j) % 2 == 0 else seat.set_color("white")
                # Mark the seat as occupied if it's colored
                seat.occupied = seat.color == "red"

class CircularPattern:
    def apply_pattern(self, seat_grid):
        num_rows = len(seat_grid)
        num_cols = len(seat_grid[0])
        center_x = num_cols // 2  # X-coordinate of the center of the hall
        center_y = num_rows // 2  # Y-coordinate of the center of the hall
        radius = min(num_rows, num_cols) // 2  # Radius of the circular layout
        num_circles = min(num_rows, num_cols) // 2  # Number of concentric circles
        seats_per_circle = 10  # Number of seats per circle
        
        for circle in range(num_circles):
            for seat_num in range(seats_per_circle):
                angle = seat_num * (360 / seats_per_circle)  # Angle of rotation for each seat
                x = int(center_x + radius * math.cos(math.radians(angle)))
                y = int(center_y + radius * math.sin(math.radians(angle)))
                if 0 <= y < num_rows and 0 <= x < num_cols:
                    seat = seat_grid[y][x]
                    seat.row = y
                    seat.column = x
                    seat.occupied = False
                    if seat_num % 2 == 0:  # Introduce a space after every alternate seat
                        seat.set_color("purple")  # Set color to yellow
                    else:
                        seat.set_color("white")
                        
class MultiLevelSeatingPattern:
    def __init__(self, level_patterns):
        self.level_patterns = level_patterns  # Dictionary of seating patterns for each level

    def apply_pattern(self, seat_grid):
        for level, pattern in self.level_patterns.items():
            pattern.apply_pattern(seat_grid)

# Example color schemes for different levels
LEVEL_COLORS = {
    "Level1": "blue",
    "Level2": "green",
    "Level3": "orange",
}

# Define seating patterns for each level
LEVEL_SEATING_PATTERNS = {
    "Level1": CircularPattern(),
    "Level2": ChessBoardPattern(),
    "Level3": TwoEmptySpacesPattern(),
}

class SeatAssignmentApp:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.spacing = 2  # Define spacing as an attribute of the class
        self.seat_grid_instance = None
    def update_seat_grid(self, selected_hall, level_patterns):
        hall_data = self.get_hall_data(selected_hall, level_patterns)
        self.seat_grid_instance = hall_data[selected_hall]
        self.seat_grid_instance.apply_seating_patterns()
        self.update_gui(self.seat_grid_instance.seat_grid)
    
    def get_hall_data(self, selected_hall, level_patterns):
        hall_data = {
            selected_hall: SeatGrid(20, 30, 2, level_patterns)
        }
        return hall_data
    
    def update_gui(self, seat_grid):
        for i in range(len(seat_grid)):
            for j in range(len(seat_grid[i])):
                seat = seat_grid[i][j]
                label = tk.Label(self.frame, text=seat.seat_number, bg=seat.color, padx=5, pady=5)
                label.grid(row=i, column=j)
                self.root.after(2000, lambda seat=seat, label=label: self.update_color_after_delay(seat, label))

    def run_saa(self, selected_hall, level_patterns):
        self.update_seat_grid(selected_hall, level_patterns)



def main():
    try:
        if len(sys.argv) != 3:
            print("Usage: python MSAA.py <selected_hall> <selected_pattern>")
            sys.exit(1)

        selected_hall = sys.argv[1]
        selected_pattern = sys.argv[2]

        level_patterns = {
            "Level1": CircularPattern(),
            "Level2": ChessBoardPattern(),
            "Level3": TwoEmptySpacesPattern(),
            # Add more levels and corresponding patterns as needed
        }

        root = tk.Tk()
        root.title("Exam Hall Seating")
        app = SeatAssignmentApp(root)
        app.run_saa(selected_hall, level_patterns)
        json_data = app.get_grid_data_json(selected_hall, level_patterns)
        root.mainloop()
        return json_data
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()