import tkinter as tk
from Board import Board
from tkinter import filedialog
from Solver import solve # just for testing
from Level import Level

class UI(tk.Tk):
    """This class represents the UI for the nonogram solver."""
    def __init__(self, title: str = "Nonogram", size: tuple =(900, 900)) -> None:
        """Initializes the UI.
        title: The title of the window
        size: The size of the window
        b: The board to display initially
        """
        super().__init__()
        self.title(title)
        self.size = size
        self.geometry(str(size[0]) + "x" + str(size[1]))
        self.resizable(0, 0)
        self.config(bg="white")
        self.game = None

        self.size_b = b.size

        self.show_board(b)
        self.show_menu()


    def show_board(self, b: Board) -> None:
        """Display a given board"""
        self.grid = tk.Frame(self, bg="white")
        self.grid.pack()
        button_width = 3
        button_height = 1
        self.buttons = []

        for i in range(b.size[0]):
            tk.Label(self.grid, text="\n".join([str(c) for c in b.constraints[i]]), font="Arial 20 bold", bg="white", fg="black").grid(row=0, column=i+1)
        for i in range(b.size[1]):
            tk.Label(self.grid, text=" ".join([str(c) for c in b.constraints[i+b.size[0]]]), font="Arial 20 bold", bg="white", fg="black").grid(row=i+1, column=0)

        for i in range(b.size[0]):
            self.buttons.append([])
            for j in range(b.size[1]):
                self.buttons[i].append(tk.Button(self.grid, text=" ", font="Arial 20 bold", width=button_width, height=button_height, bg="white" if not b.grid[i,j] else "black", fg="black", command=lambda i=i, j=j: self.click(i, j)))
                self.buttons[i][j].grid(row=i+1, column=j+1)
    
    def show_menu(self) -> None:
        """Display the menu buttons"""
        offset = 350
        nb = 6 # number of buttons

        button_width = 5
        button_height = 2
        # add a button to solve the board
        self.solve_button = tk.Button(self, text="Solve", font="Arial 20 bold", width=button_width, height=button_height, bg="white", fg="black", command=self.solve)
        self.solve_button.place(x=offset//(nb+5), y=self.size[1]//nb*3+offset)

        # add a button to reset the board
        self.reset_button = tk.Button(self, text="Reset", font="Arial 20 bold", width=button_width, height=button_height, bg="white", fg="black", command=self.reset)
        self.reset_button.place(x=self.size[0]//nb+offset//(nb+5), y=self.size[1]//nb*3+offset)

        # add a button select a board
        self.select_button = tk.Button(self, text="Select", font="Arial 20 bold", width=button_width, height=button_height, bg="white", fg="black", command=self.select)
        self.select_button.place(x=self.size[0]//nb*2+offset//(nb+5), y=self.size[1]//nb*3+offset)

        # add a button to give an hint
        self.hint_button = tk.Button(self, text="Hint", font="Arial 20 bold", width=button_width, height=button_height, bg="white", fg="black", command=self.hint)
        self.hint_button.place(x=self.size[0]//nb*3+offset//(nb+5), y=self.size[1]//nb*3+offset)

        # add a button to undo
        self.undo_button = tk.Button(self, text="Undo", font="Arial 20 bold", width=button_width, height=button_height, bg="white", fg="black", command=self.undo)
        self.undo_button.place(x=self.size[0]//nb*4+offset//(nb+5), y=self.size[1]//nb*3+offset)

        # add a button to redo
        self.redo_button = tk.Button(self, text="Redo", font="Arial 20 bold", width=button_width, height=button_height, bg="white", fg="black", command=self.redo)
        self.redo_button.place(x=self.size[0]//nb*5+offset//(nb+5), y=self.size[1]//nb*3+offset)

    def click(self, i, j) -> tuple[int, int]:
        """Change the color of a button when clicked for the nonogram"""
        self.buttons[i][j].config(bg="black" if self.buttons[i][j]["bg"] == "white" else "white")
        return i,j

    def run(self) -> None:
        """Run the UI mainloop"""
        self.bind('<Escape>', lambda e: self.destroy()) # close the window when pressing escape
        self.mainloop()


    def solve(self) -> None:
        """Solve the board and show the solution"""
        pass

    def reset(self) -> None:
        """Reset the board to 0"""
        for i in range(self.size_b[0]):
            for j in range(self.size_b[1]):
                self.buttons[i][j].config(bg="white", fg="black")
        #TODO: reset stacks and stuffs in the game class when called from the game class and vice versa

    def select(self) -> Board:
        """Select a board from a file and loads it into the UI AND returns the new board"""
        try:
            filename = filedialog.askopenfilename(
                initialdir = "src/",
                title = "Select file",
                filetypes = (("Text files", "*.txt"), ("all files", "*.*"))
            )

            new_b = Level.from_file(filename)
            self.size_b = new_b.size

            wgds = tk.Tk.winfo_children(self) # all widgets
            #find frame within the widgets
            index_frame = 0
            for i in range(len(wgds)):
                if wgds[i].winfo_class() == "Frame":
                    index_frame = i
                    break
            wgds[index_frame].destroy()
            self.show_board(new_b)

            self.reset()

            return new_b
        except:
            return None # The user didn't select a file

    def hint(self) -> None:
        """Give an hint and asks for the level of hint"""
        pass

    def undo(self) -> None:
        """Undo the last move in the stack"""
        pass

    def redo(self) -> None:
        """Redo the last move in the stack"""
        pass

    def my_upd(self, b: Board) -> None:
        """Update the board"""
        for i in range(b.size[0]):
            for j in range(b.size[1]):
                self.buttons[i][j].config(bg="black" if b.grid[i,j] else "white")

if __name__ == "__main__":
    b = Board.from_file("src/TestBoard.txt")
    b.grid[0,0] = 1
    b.grid[0,1] = 1
    b.grid[0,2] = 1
    b.grid[0,3] = 1
    ui = UI(b=b)
    ui.my_upd(solve(b))
    ui.run()