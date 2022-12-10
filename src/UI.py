import tkinter as tk
from Board import Board

class UI(tk.Tk):
    def __init__(self, title="Nonogram", size=(500, 700)):
        super().__init__()
        self.title(title)
        self.geometry(str(size[0]) + "x" + str(size[1]))
        self.resizable(0, 0)
        self.config(bg="white")

        self.show_board(b)
        self.show_menu()

    def show_board(self, Board: Board):
        self.grid = tk.Frame(self, bg="white")
        self.grid.pack()

        self.buttons = []
        for i in range(Board.size[0]):
            self.buttons.append([])
            for j in range(Board.size[1]):
                self.buttons[i].append(tk.Button(self.grid, text=" ", font="Arial 20 bold", width=2, height=1, bg="white", fg="black", command=lambda i=i, j=j: self.click(i, j)))
                self.buttons[i][j].grid(row=i, column=j)
    
    def show_menu(self):

        # add a button to solve the board
        self.solve_button = tk.Button(self, text="Solve", font="Arial 20 bold", width=10, height=2, bg="white", fg="black", command=self.solve)
        self.solve_button.place(x=0, y=2)

        # add a button to reset the board
        self.reset_button = tk.Button(self, text="Reset", font="Arial 20 bold", width=10, height=2, bg="white", fg="black", command=self.reset)
        self.reset_button.place(x=0, y=1)

        # add a button select a board
        self.select_button = tk.Button(self, text="Select", font="Arial 20 bold", width=10, height=2, bg="white", fg="black", command=self.select)
        self.select_button.place(x=0, y=0)

        
    def click(self, i, j):
        self.buttons[i][j].config(bg="black" if self.buttons[i][j]["bg"] == "white" else "white")

    def run(self):
        self.mainloop()

    def solve(self):
        pass

    def reset(self):
        pass

    def select(self):
        pass

if __name__ == "__main__":
    b = Board.from_file("src/TestBoard.txt")
    ui = UI()
    ui.run()