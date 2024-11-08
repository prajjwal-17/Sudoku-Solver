import tkinter as tk
from tkinter import messagebox

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        
        # Initialize 9x9 grid for Sudoku with bold borders for 3x3 grids
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.initial_values = set()  # To keep track of user-entered values

        # Create a main frame to hold the 3x3 subgrid frames
        main_frame = tk.Frame(root, bg="black")  # Black border for entire board
        main_frame.pack(padx=10, pady=10)

        # Create 3x3 subgrid frames
        subgrid_frames = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(main_frame, bg="black", highlightbackground="black", highlightthickness=2)
                frame.grid(row=i, column=j, padx=1, pady=1)
                subgrid_frames[i][j] = frame

        # Populate each subgrid frame with Entry widgets
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(subgrid_frames[i // 3][j // 3], width=2, font=('Arial', 18), justify='center', fg='blue')
                entry.grid(row=i % 3, column=j % 3, padx=1, pady=1, sticky='nsew')
                self.entries[i][j] = entry

        # Add a solve button
        solve_button = tk.Button(root, text="Solve", command=self.solve)
        solve_button.pack(pady=10)

    def get_board(self):
        """Extracts the board from the Entry widgets and returns it as a 2D list."""
        board = []
        self.initial_values.clear()
        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit():
                    num = int(value)
                    row.append(num)
                    self.initial_values.add((i, j))  # Mark initial cells
                    self.entries[i][j].config(fg="blue")  # User-entered values in blue
                else:
                    row.append(0)  # Empty cells are marked with 0
            board.append(row)
        return board

    def set_board(self, board):
        """Sets the board values back to the Entry widgets."""
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.initial_values:  # Only update non-initial cells
                    self.entries[i][j].delete(0, tk.END)
                    if board[i][j] != 0:
                        self.entries[i][j].insert(0, str(board[i][j]))
                        self.entries[i][j].config(fg="red")  # Solver-added values in red

    def is_valid(self, board, row, col, num):
        """Check if placing num in board[row][col] is valid."""
        for j in range(9):
            if board[row][j] == num:
                return False
        for i in range(9):
            if board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self, board):
        """Solve the Sudoku board using backtracking."""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:  # Find an empty cell
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve_sudoku(board):
                                return True
                            board[row][col] = 0  # Backtrack
                    return False
        return True

    def solve(self):
        """Solve the puzzle and update the GUI."""
        board = self.get_board()
        if self.solve_sudoku(board):
            self.set_board(board)
            messagebox.showinfo("Sudoku Solver", "Sudoku puzzle solved successfully!")
        else:
            messagebox.showerror("Sudoku Solver", "No solution exists for the given Sudoku board.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.geometry("450x500")
    root.mainloop()
