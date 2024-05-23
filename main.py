from abc import abstractmethod
import customtkinter as ctk
import os
from PIL import Image, ImageTk
import tkinter as tk
from greet_window import Greet_window
from editor_grid import Editor_grid

class Application(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instr_bar_w = 50
        self.tiles = []

        self.window_setup()
        self.init_gui()
        self.init_instruments()
        
        # self.greet_user()


    def window_setup(self):
        self.title('Simple tile editor')
        self.geometry('1200x800')
        self.attributes('-type', 'dialog')


    def init_instruments(self):
        self.instruments = {
            'brush' : Brush(),
            'eraser' : Eraser()
        }

        self.change_instrument('brush')


    def init_gui(self):
        self.create_paned_window()
        self.create_editor_grid()
        self.create_tiles_panel()
        self.create_instruments_bar()

        self.panel_divider.add(self.editor_grid)
        self.panel_divider.add(self.tiles_panel, minsize=200)


    def create_instruments_bar(self):
        self.instruments_bar = Instruments_bar(self, self.change_instrument, width=self.instr_bar_w, height=self.winfo_screenheight(), corner_radius=0)
        self.instruments_bar.pack_propagate(False)
        self.instruments_bar.place(anchor='nw')


    def create_paned_window(self):
        self.panel_divider = tk.PanedWindow(orient='horizontal', bd=0, bg='lightgrey')
        self.panel_divider.place(x=self.instr_bar_w, y=0)


    def create_editor_grid(self):
        self.editor_grid = Editor_grid(self.panel_divider, [30, 30], 32)


    def create_tiles_panel(self):
        self.tiles_panel = ctk.CTkFrame(master=self.panel_divider, fg_color='white', corner_radius=0)
        self.tiles_panel.pack_propagate(False)
        self.tiles_panel.grid_propagate(False)

        self.tiles_panel.rowconfigure((0,1,2,3,4), weight=1)
        self.tiles_panel.columnconfigure(tuple(i for i in range(50)), weight=1)
        self.render_tiles_thumbnails()

    
    def render_tiles_thumbnails(self):
        self.load_sprites()

        prevY = 0
        prevIndex = 0
        padx = 10
        for ind, image in enumerate(self.tiles):
            l = ctk.CTkLabel(self.tiles_panel, image=image, text='')
            l._image_ref = image

            self.update_idletasks()
            self.tiles_panel.update_idletasks()

            y = (ind * 32 + padx) // 200

            if prevY != y:
                prevIndex = ind

            prevY = y
            x = 32 * (ind - prevIndex) + padx

            l.place(x=x, y=y)

            l.bind('<Button-1>', self.select_tile)


    def greet_user(self) -> None:
        window = Greet_window(load_project=self.load_project, create_project=self.create_project)
        window.grab_set()


    def change_instrument(self, instr : str):
        if instr not in self.instruments : return -1
        self.cur_instr = self.instruments[instr]

        for key, val in self.instruments_bar.instr_labels.items():
            if key == instr:
                val.configure(bg_color='red')
            else:
                val.configure(bg_color='white')

        self.editor_grid.change_instrument(self.instruments[instr])


    def load_sprites(self) -> None:
        images = []
        for (dirpath, dirnames, filenames) in os.walk('Tiles'):
            images.extend(filenames)
            break

        images = list(filter(lambda el: el.endswith('.png'), images))
        self.tiles = list(map(lambda el: ImageTk.PhotoImage(Image.open('Tiles/' + el).convert('RGBA')), images))


    def select_tile(self, event):
        widget = event.widget
        self.editor_grid.cur_tile = widget.cget('image')


    def load_project(self) -> None:
        print("Project loaded")


    def create_project(self) -> None:
        print("Prject created")


class Instruments_bar(ctk.CTkFrame):
    def __init__(self, master, change_instr, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.change_instrument = change_instr
        self.instr_labels = {}

        self.instr_labels.update({'brush' : ctk.CTkLabel(self, text='Brush')})
        self.instr_labels.update({'eraser' : ctk.CTkLabel(self, text='Eraser')})

        for key, val in self.instr_labels.items():
            def mk_lmbd(x):
                return lambda event: self.change_instrument(x)

            val.pack(fill='x')
            val.bind('<Button-1>', mk_lmbd(key))

class Instrument:
    def __init__(self):
        self.size = 3

    @abstractmethod
    def draw(self, canvas, cell_id, last_cell_id, cell_size, zoom_scale, tile):
        pass


class Brush(Instrument):
    def __init__(self):
        super().__init__()

    def draw(self, canvas, cell_id, last_cell_id, cell_size, zoom_scale, tile):
        coords = canvas.bbox(cell_id)

        if cell_id < last_cell_id:
            img_id = canvas.create_image(coords[0], coords[1], anchor='nw', image=tile, tags=[f'{tile[-1]}'])
        else:
            canvas.itemconfig(cell_id, image=tile)


class Eraser(Instrument):
    def __init__(self):
        super().__init__()

    def draw(self, canvas, cell_id, last_cell_id, cell_size, zoom_scale, tile):
        if cell_id > 900:
            canvas.delete(cell_id)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
