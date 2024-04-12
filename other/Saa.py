import tkinter as tk
import tkinter.simpledialog as sd
from tkinter import ttk

matric_numbers = ['A1', 'B7', 'C3', 'D9', 'E8', 'D6', 'A2']

class Seat:
    def __init__(self, seat_number, row, column, occupied=False):
        self.seat_number = seat_number
        self.row = row
        self.column = column
        self.occupied = occupied
        self.color = "white"

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
            
class ZigZagPattern:
    def apply_pattern(self, seat_grid):
        for i in range(len(seat_grid)):
            for j in range(len(seat_grid[i])):
                seat = seat_grid[i][j]
                if i == 0 and j % 2 == 0:
                    seat.occupied = True
                    seat.color = "yellow"
                    
class ChessBoardPattern:
    def apply_pattern(self, seat_grid):
        for i in range(len(seat_grid)):
            for j in range(len(seat_grid[i])):
                seat = seat_grid[i][j]
                if (i + j) % 2 == 0:
                    seat.occupied = True
                    seat.color = "yellow"

def select_hall():
    selected_hall = sd.askstring("Select Hall", "Select Hall:\nTLT\nFLT")
    return selected_hall

def select_seating_pattern():
    selected_pattern = sd.askstring("Seating Pattern", "Select Seating Pattern:\nCheckerboard\nZigzag")
    return selected_pattern

def update_seat_grid(selected_hall, selected_pattern):
    hall_data = get_hall_data(selected_pattern)
    hall_seat_grid = hall_data[selected_hall]
    hall_seat_grid.apply_seating_pattern()
    update_gui(hall_seat_grid.seat_grid, frame)

def get_hall_data(selected_pattern):
    if selected_pattern == "Checkerboard":
        hall_data = {
            "TLT" : SeatGrid(20, 30, 2, ChessBoardPattern()),
            "FLT" : SeatGrid(15, 5, 2, ChessBoardPattern())}
    elif selected_pattern == "Zigzag":
        hall_data = {
            "TLT" : SeatGrid(20, 30, 2, ZigZagPattern()),
            "FLT" : SeatGrid(15, 5, 2, ZigZagPattern())}
    else:
        raise ValueError("Invalid seating pattern selected.")
    return hall_data

def update_gui(seat_grid, frame):
    global matric_numbers
    total_students = len(matric_numbers)
    student_counter = 0

    for i in range(len(seat_grid)):
        for j in range(len(seat_grid[i])):
            seat = seat_grid[i][j]
            update_color(seat, j % spacing == 0)
            if seat.occupied:
                if student_counter < total_students:
                    seat.seat_number = matric_numbers[student_counter]
                    student_counter += 1
                else:
                    seat.seat_number = "Empty"
            else:
                seat.seat_number = "Empty"
            
            label = tk.Label(frame, text=seat.seat_number, bg=seat.color, padx=5, pady=5)
            label.grid(row=i, column=j)
            root.after(2000, lambda seat=seat, label=label: update_color_after_delay(seat, label))
        
def update_color(seat, is_spacing):
    if is_spacing:
        seat.occupied = True
    if seat.occupied:
        seat.color = "yellow"
    else:
        seat.color = "white"

def update_color_after_delay(seat, label):
    update_color(seat, seat.column % spacing == 0)
    label.configure(bg=seat.color)

# Saa.py

def run_saa(selected_hall, selected_pattern):
    # Perform operations based on selected hall and pattern
    # For example:
    if selected_hall == 'TLT':
        # Do something for TLT
        pass
    elif selected_hall == 'FLT':
        # Do something for FLT
        pass

    if selected_pattern == 'Checkerboard':
        # Do something for Checkerboard
        pass
    elif selected_pattern == 'Zigzag':
        # Do something for Zigzag
        pass
    
    # Return the result or perform further operations

            
def main():
    global frame
    global spacing
    global root
    spacing = 2
    root = tk.Tk()
    root.title("Exam Hall Seating")
    selected_hall = select_hall()
    if selected_hall not in ["TLT", "FLT"]:
        tk.messagebox.showerror("Error", "Invalid Hall Selected")
        root.destroy()
        return

    selected_pattern = select_seating_pattern()
    if selected_pattern not in ["Checkerboard", "Zigzag"]:
        tk.messagebox.showerror("Error", "Invalid Seating Pattern Selected")
        root.destroy()
        return
    run_saa(selected_hall, selected_pattern)

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0,sticky=(tk.W, tk.E, tk.N, tk.S))
    update_seat_grid(selected_hall, selected_pattern)
    root.mainloop()
    
if __name__ == "__main__":
    main()
