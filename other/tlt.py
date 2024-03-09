import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as messagebox
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
#                 if i % 2 == 0 and j % 2 == 0: #Dark Squares
#                     seat.occupied = True
#                     seat.color = "yellow"
#                 elif i % 2 == 1 and j % 2 == 1: #Dark squares on odd rows
#                     seat.occupied = True
#                     seat.color = "yellow"
     
#     def assign_seat(self, student):
#         for row in self.seat_grid:
#             for seat in row:
#                 if not seat.occupied:
#                     seat.occupied = True
#                     return seat.seat_number
#                 
#         return None
                    
def select_seating_pattern():
    selected_pattern = sd.askstring("Seating Pattern", "Select Seating Pattern:\nCheckerboard\nZigzag")
    return selected_pattern

def create_combobox(hall_names, var, frame):
    combobox = ttk.Combobox(frame, textvariable = var, values=hall_names)
    combobox.grid(row=0, column=0)
    combobox.bind("<<ComboboxSelected>>", lambda _: update_seat_grid(var.get()))
    
def update_seat_grid(selected_hall):
    selected_pattern = select_seating_pattern()
    hall_data = get_hall_data(selected_pattern)
    hall_seat_grid = hall_data[selected_hall]
    hall_seat_grid.apply_seating_pattern()
    update_gui(hall_seat_grid.seat_grid, frame)   # There should be a third argument hall_seat_grid.aisle_width
    
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
            
def main():
    global frame
    global spacing
    global root
    spacing = 2
    root = tk.Tk()
    root.title("Exam Hall Seating")
    hall_data = get_hall_data()
    hall_names = list(hall_data.keys())
    selected_hall = sd.askstring("Seating Pattern", "Select Seating Pattern:\n" + "\n".join(hall_names))
    if selected_hall not in hall_names:
        messagebox.showerror("Error", "Invalid Selection")
        root.destroy()
        return
    
    var = tk.StringVar()
    var.set(selected_hall)
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0,sticky=(tk.W, tk.E, tk.N, tk.S))
#   update_gui(seat_grid.seat_grid, frame)
    update_seat_grid(selected_hall)
    root.mainloop()
    
if __name__ == "__main__":
    main()
