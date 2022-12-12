import tkinter as tk
from Board import Board
from tkinter import filedialog, simpledialog
from Solver import solve # just for testing
from Level import Level
from UnsafeStack import UnsafeStack
from Game import Game
from Case import Case
from Utils import WHITE, BLACK, RED, GREEN, GRAY, int_to_color, color_to_int

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
        self.size_b = None
        self.can_pop = self.game.can_undo() if self.game else False
        self.can_unpop = self.game.can_redo() if self.game else False

        self.show_menu()


    def show_board(self, b: Board, l: Level) -> None:
        """Display a given board"""
        self.grid = tk.Frame(self, bg="white")
        self.grid.pack()
        button_width = 3
        button_height = 1
        self.buttons = []

        for i in range(b.size[0]):
            tk.Label(self.grid, text="\n".join([str(c) for c in l.constraints[i]]), font="Arial 20 bold", bg="white", fg="black").grid(row=0, column=i+1)
        for i in range(b.size[1]):
            tk.Label(self.grid, text=" ".join([str(c) for c in l.constraints[i+b.size[0]]]), font="Arial 20 bold", bg="white", fg="black").grid(row=i+1, column=0)

        for i in range(b.size[0]):
            self.buttons.append([])
            for j in range(b.size[1]):
                self.buttons[i].append(tk.Button(self.grid, text=" ", font="Arial 20 bold", width=button_width, height=button_height, bg=int_to_color[b.grid[i,j]], fg="black", command=lambda i=i, j=j: self.click(i, j)))
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
        self.undo_button = tk.Button(self, text="Undo", font="Arial 20 bold", width=button_width, height=button_height, bg="gray" if not self.can_pop else "white", fg="black", command=self.undo)
        self.undo_button.place(x=self.size[0]//nb*4+offset//(nb+5), y=self.size[1]//nb*3+offset)

        # add a button to redo
        self.redo_button = tk.Button(self, text="Redo", font="Arial 20 bold", width=button_width, height=button_height, bg="gray" if not self.can_unpop else "white", fg="black", command=self.redo)
        self.redo_button.place(x=self.size[0]//nb*5+offset//(nb+5), y=self.size[1]//nb*3+offset)

    def click(self, i, j) -> tuple[int, int]:
        """Change the color of a button when clicked for the nonogram"""
        self.buttons[i][j].config(bg="black" if self.buttons[i][j]["bg"] == "white" else "white")
        self.game.color(i, j, color_to_int["black"] if self.buttons[i][j]["bg"] == "black" else color_to_int["white"])
        self.upd_pop_unpop()

    def run(self) -> None:
        """Run the UI mainloop"""
        self.bind('<Escape>', lambda e: self.destroy()) # close the window when pressing escape
        self.mainloop()

    def solve(self) -> None:
        """Solve the board and show the solution"""
        self.my_upd(self.game.solved_board)
        self.show_win() # altough it's obvious now, or is it?

    def reset(self) -> None:
        """Reset the board to 0"""
        for i in range(self.size_b[0]):
            for j in range(self.size_b[1]):
                self.buttons[i][j].config(bg="white", fg="black")
        self.game.reset()

    def select(self) -> Board:
        """Select a board from a file and loads it into the UI AND returns the new board"""
        try:
            filename = filedialog.askopenfilename(
                initialdir = "src/",
                title = "Select file",
                filetypes = (("Text files", "*.lvl"), ("all files", "*.*"))
            )
            new_l = Level.from_file(filename)
            self.game.load_level(new_l)
            self.size_b = new_l.size

            wgds = tk.Tk.winfo_children(self) # all widgets
            #find frame within the widgets
            for i, wgd in enumerate(wgds):
                if wgd.winfo_class() == "Frame":
                    index_frame = i
                    wgds[index_frame].destroy()
                    break
            self.show_board(self.game.user_board, self.game.level)

            self.reset()
        except(FileNotFoundError, AttributeError):
            return None # if the user cancels the file selection

    def hint(self) -> None:
        """Give an hint and asks for the level of hint"""
        hint_level = simpledialog.askinteger("Hint", "Enter hint type (1-3)", minvalue=1, maxvalue=3)
        if hint_level is not None:
            self.game.new_hint(hint_level)
            x, y = self.game.hints[-1].x, self.game.hints[-1].y
            match hint_level:
                case 1:
                    self.set_case(x, y, "black")
                    self.game.color(x, y, color_to_int["black"])
                case 2:
                    self.set_case(x, y, "white")
                    self.game.color(x, y, color_to_int["white"])
                case 3:
                    self.set_case(x, y, "green")
                    self.game.color(x, y, color_to_int["green"])
            self.upd_pop_unpop()

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
                self.buttons[i][j].config(bg=int_to_color[b.grid[i,j]])

    def show_win(self) -> None:
        """Colors the buttons green when the user wins"""
        for i in range(self.size_b[0]):
            for j in range(self.size_b[1]):
                self.buttons[i][j].config(bg="green" if self.buttons[i][j]["bg"] == "black" else "white", fg="white")

    def set_case(self, x: int, y: int, color: str) -> None:
        """Set the case of the board"""
        self.buttons[y][x].config(bg=color)

    def upd_pop_unpop(self) -> None:
        """Update the pop and unpop buttons"""
        self.can_pop = self.game.can_undo()
        self.can_unpop = self.game.can_redo()

        self.undo_button.config(bg=int_to_color[GRAY] if not self.can_pop else int_to_color[WHITE])
        self.redo_button.config(bg=int_to_color[GRAY] if not self.can_unpop else int_to_color["white"])
        

if __name__ == "__main__":
    Game = Game(UI())
    Game.run()
    