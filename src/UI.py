import tkinter as tk
from Board import Board
from tkinter import filedialog, simpledialog
from Solver import solve # just for testing
from Level import Level
from UnsafeStack import UnsafeStack
from Game import Game
from Case import Case
from Utils import WHITE, BLACK, RED, GREEN, GRAY, int_to_color, color_to_int

# TODO: Fix non-square matrix UI bug

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

        self.level_text = tk.Label(self, text="NotLoaded", font="Arial 20 bold", height=button_height, width=button_width * 2)
        self.level_text.place(x=(self.size[0]) // 2 - button_width * 8, y=self.size[1]//nb*2.1+offset)

    def click(self, i, j) -> tuple[int, int]:
        """Change the color of a button when clicked for the nonogram"""
        if (j, i) in self.game.hint_keys and self.game.hint_keys[(j, i)] != 2:       # Can't click if case is a hint
            return
        self.buttons[i][j].config(bg="black" if self.game.user_board.grid[i, j] == 0 else "white")
        self.game.color(j, i, color_to_int[self.buttons[i][j]["bg"]])
        self.test_victory()
        self.upd_pop_unpop()

    def update_level_name(self):
        self.level_text.config(text=self.game.level.name)

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
        for j in range(self.size_b[0]):
            for i in range(self.size_b[1]):
                self.buttons[j][i].config(bg="white", fg="black")
        self.game.reset()
        self.upd_pop_unpop()

    def select(self) -> Board:
        """Select a board from a file and loads it into the UI AND returns the new board"""
        try:
            filename = filedialog.askopenfilename(
                initialdir = "src/Levels",
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

    def load(self) -> None:
        """loads a board from game"""
        self.size_b = self.game.level.size
        wgds = tk.Tk.winfo_children(self) # all widgets
        #find frame within the widgets
        for i, wgd in enumerate(wgds):
            if wgd.winfo_class() == "Frame":
                index_frame = i
                wgds[index_frame].destroy()
                break
        self.show_board(self.game.user_board, self.game.level)
        self.reset()

    def _get_hint_color(self, hint_type):
        match hint_type:
            case 1:
                return GRAY
            case 2:
                return RED
            case 3:
                return GREEN

    def test_victory(self):
        if self.game.is_finished():
            self.show_win()

    def hint(self) -> None:
        """Give an hint and asks for the level of hint"""
        hint_level = simpledialog.askinteger("Hint", "Enter hint type (1-3)", minvalue=1, maxvalue=3)
        if hint_level is None:
            return
        x, y, hint_type = self.game.new_hint(hint_level)
        if hint_type == -1:
            print("Couldn't create hint of type", hint_level)
            return
        color = self._get_hint_color(hint_type)
        if hint_type == 1:
            self.game.user_board.grid[y, x] = self.game.solved_board.grid[y, x]
        self.buttons[y][x].config(bg=int_to_color[color])
        self.upd_pop_unpop()
        self.test_victory()

    def undo(self) -> None:
        """Undo the last move in the stack"""
        if self.can_pop:
            self.game.undo()
            self.my_upd(self.game.user_board)
            self.upd_pop_unpop()
            self.test_victory()

    def redo(self) -> None:
        """Redo the last move in the stack"""
        if self.can_unpop:
            self.game.redo()
            self.my_upd(self.game.user_board)
            self.upd_pop_unpop()
            self.test_victory()

    def my_upd(self, b: Board) -> None:
        """Update the board"""
        for j in range(b.size[0]):
            for i in range(b.size[1]):
                self.buttons[j][i].config(bg=int_to_color[b.grid[j,i]])

    def show_win(self) -> None:
        """Colors the buttons green when the user wins"""
        for i in range(self.size_b[0]):
            for j in range(self.size_b[1]):
                self.buttons[j][i].config(bg="green" if self.buttons[j][i]["bg"] != "white" else "white", fg="white")

    def set_case(self, x: int, y: int, color: str) -> None:
        """Set the case of the board"""
        self.buttons[y][x].config(bg=color)

    def upd_pop_unpop(self) -> None:
        """Update the pop and unpop buttons"""
        self.can_pop = self.game.can_undo()
        self.can_unpop = self.game.can_redo()

        self.undo_button.config(bg=int_to_color[GRAY] if not self.can_pop else int_to_color[WHITE])
        self.redo_button.config(bg=int_to_color[GRAY] if not self.can_unpop else int_to_color[WHITE])
        

if __name__ == "__main__":
    Game = Game(UI())
    Game.run()
    