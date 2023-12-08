import tkinter as tk


class Cell:
    def __init__(self, master, value, row, col):
        self.master = master
        self.value = value
        self.row = row
        self.col = col
        self.button = tk.Button(master, text=str(value), width=5, height=2, command=self.move_cell)
        self.button.grid(row=row, column=col)

    def move_cell(self):
        # Swap the cell with the empty cell
        empty_row, empty_col = empty_cell.get_position()
        empty_cell.set_position(self.row, self.col)
        self.row, self.col = empty_row, empty_col

        # Update the grid display
        update_grid()

    def get_position(self):
        return self.row, self.col

    def set_position(self, row, col):
        self.row = row
        self.col = col
        self.button.grid(row=row, column=col)


def create_grid():
    grid = [[j + i * 8 for j in range(8)] for i in range(8)]
    return grid


def update_grid():
    for row in range(8):
        for col in range(8):
            cell = cells[grid[row][col]]
            cell.set_position(row, col)


def init_empty_cell():
    empty_cell.set_position(7, 7)


# Initialize the Tkinter window
root = tk.Tk()
root.title("Grid of Cells")

# Create the grid
grid = create_grid()

# Create cells and add them to the grid
cells = {}
for row in range(8):
    for col in range(8):
        value = grid[row][col]
        if value != 63:  # 8x8 grid, so 64 cells; leave the last cell empty
            cells[value] = Cell(root, value, row, col)

# Initialize the empty cell
empty_cell = Cell(root, "", 7, 7)
empty_cell.button.config(state=tk.DISABLED)  # Make the empty cell unclickable

# Initialize the grid display
init_empty_cell()

# Start the Tkinter event loop
root.mainloop()
