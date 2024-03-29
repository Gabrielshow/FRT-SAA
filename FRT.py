import tkinter as tk
import tkinter.simpledialog as sd
from tkinter import ttk
import sys
import json

matric_numbers = ['A1', 'B7', 'C3', 'D9', 'E8', 'D6', 'A2']

class Seat:
    def __init__(self, seat_number, row, column, occupied=False):
        self.seat_number = seat_number
        self.row = row
        self.column = column
        self.occupied = occupied
        self.color = "white"
    
    def set_color(self, color):
        """Set the color of the seat based on the pattern."""
        self.color = color

class SeatGrid:
    def __init__(self, rows, columns, spacing=2, seating_pattern=None):
        self.rows = rows
        self.columns = columns
        self.space = spacing
        self.seating_pattern = seating_pattern
        self.seat_grid = [[Seat(row * columns + col, row, col) for col in range (columns)] for row in range(rows)]
      
    def apply_seating_pattern(self):
        if self.seating_pattern:
            self.seating_pattern.apply_pattern(self.seat_grid)

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

class SeatAssignmentApp:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.spacing = 2 # Define spacing as an attribute of the class
        self.seat_grid_instance = None

    def update_seat_grid(self, selected_hall, selected_pattern):
        hall_data = self.get_hall_data(selected_pattern)
        self.seat_grid_instance = hall_data[selected_hall] # Store the SeatGrid instance
        self.seat_grid_instance.apply_seating_pattern()
        self.update_gui(self.seat_grid_instance.seat_grid)
    
    def get_hall_data(self, selected_pattern):
        if selected_pattern == "Checkerboard":
            hall_data = {
                "TLT" : SeatGrid(20, 30, 2, ChessBoardPattern()),
                "FLT" : SeatGrid(15, 5, 2, ChessBoardPattern())}
        elif selected_pattern == "Normal":
            hall_data = {
                "TLT" : SeatGrid(20, 30, 2, NormalPattern()),
                "FLT" : SeatGrid(15, 5, 2, NormalPattern())}
        elif selected_pattern == "TwoEmptySpaces":
            hall_data = {
                "TLT" : SeatGrid(20, 30, 2, TwoEmptySpacesPattern()),
                "FLT" : SeatGrid(15, 5, 2, TwoEmptySpacesPattern())}
        else:
            raise ValueError("Invalid seating pattern selected.")
        return hall_data
    
    def update_gui(self, seat_grid):
        total_students = len(matric_numbers)
        student_counter = 0

        for i in range(len(seat_grid)):
            for j in range(len(seat_grid[i])):
                seat = seat_grid[i][j]
                # Do not change the color based on spacing
                # The color is already set by the pattern
                if seat.occupied:
                    if student_counter < total_students:
                        seat.seat_number = matric_numbers[student_counter]
                        student_counter += 1
                    else:
                        seat.seat_number = "Empty"
                else:
                    seat.seat_number = "Empty"
            
                label = tk.Label(self.frame, text=seat.seat_number, bg=seat.color, padx=5, pady=5)
                label.grid(row=i, column=j)
                self.root.after(2000, lambda seat=seat, label=label: self.update_color_after_delay(seat, label))
                
    def update_color(self, seat, is_spacing):
        pass

    def update_color_after_delay(self, seat, label):
        label.configure(bg=seat.color)
    
    def get_grid_data(self, seat_grid):
        grid_data = []
        for row in seat_grid:
            row_data = []
            for seat in row:
                row_data.append({
                    'seat_number': seat.seat_number,
                    'occupied': seat.occupied,
                    'color': seat.color
                })
            grid_data.append(row_data)
        return grid_data
    
    def get_grid_data_json(self, selected_hall, selected_pattern):
        self.update_seat_grid(selected_hall, selected_pattern)
        grid_data = self.get_grid_data(self.seat_grid_instance.seat_grid)
        return json.dumps(grid_data)

    def run_saa(self, selected_hall, selected_pattern):
         self.update_seat_grid(selected_hall, selected_pattern)

def main():
    if len(sys.argv) != 3:
        print("Usage: python saa.py <selected_hall> <selected_pattern>")
        sys.exit(1)

    selected_hall = sys.argv[1]
    selected_pattern = sys.argv[2]
    root = tk.Tk()
    root.title("Exam Hall Seating")
    app = SeatAssignmentApp(root)
    app.run_saa(selected_hall, selected_pattern) # Define selected_hall and selected_pattern before calling
    root.mainloop()
    def get_grid_data_json(selected_hall, selected_pattern):
        root = tk.Tk()
        app = SeatAssignmentApp(root)
    return app.get_grid_data_json(selected_hall, selected_pattern)

if __name__ == "__main__":
    main()
