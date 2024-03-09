import tkinter as tk

root = tk.Tk()
col_count = 30
row_count = 20

# Set minimum size for all columns and rows
col_count, row_count = root.grid_size()
for col in range(col_count):
    root.grid_columnconfigure(col, minsize=20)
for row in range(row_count):
    root.grid_rowconfigure(row, minsize=20)

# Add widgets with adjusted spacing
label = tk.Label(root, text='Label')
label.grid(column=3, row=8, padx=5, pady=5)

button = tk.Button(root, text='Button')
button.grid(column=5, row=1, padx=5, pady=5)

root.mainloop()
