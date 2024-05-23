import customtkinter as ctk
from PIL import ImageTk, Image

class Editor_grid(ctk.CTkCanvas):
    def __init__(self, parent, grid_size : list[int], tile_size : int, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.size : list[int] = grid_size
        self.cell_size : int = tile_size
        self.last_cell_id : int = self.size[0] * self.size[1]
        self.zoom_scale = 1
        self.instr = 0
        self.cur_tile = 0
        self.config(width = self.cell_size * self.size[0], height=self.cell_size * self.size[1])
        
        self.draw_grid()
        self.bind_events()


    def draw_grid(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                x = self.cell_size * col
                y = self.cell_size * row

                rect = self.create_rectangle(x, y, x + self.cell_size,y + self.cell_size, fill='white')
                #self.tag_bind(rect, "<Button-3>", self.draw)



    def bind_events(self):
        #self.bind("<Button-4>", self.do_zoom_in) 
        #self.bind("<Button-5>", self.do_zoom_out) 
        self.bind("<Button-2>", self.export_grid)
        self.bind("<Button-3>", self.draw)
        self.bind('<ButtonPress-1>', lambda event: self.scan_mark(event.x, event.y))
        self.bind("<B1-Motion>", lambda event: self.scan_dragto(event.x, event.y, gain=1))


    def export_grid(self, event):
        with open('tilemap.txt', 'w') as file:
            for col in range(self.size[0]-1):
                for row in range(self.size[1]-1):
                     # Grid cell center
                    x = row * self.cell_size + self.cell_size // 2
                    y = col * self.cell_size + self.cell_size // 2
    
                    id = self.find_closest( self.canvasx(x), self.canvasy(y) )[0]
                    if id < self.last_cell_id:
                        file.write('0,')
                    else:
                        file.write(f'{self.gettags(id)[0]},')

                file.write('\n')




    def change_instrument(self, instr) -> None:
        self.instr = instr


    def draw(self, event) -> None:
        if self.cur_tile:
            id = self.get_closest(event)

            self.instr.draw(self, id, self.last_cell_id, self.cell_size, self.zoom_scale, self.cur_tile)


    # Get closest object to click
    def get_closest(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        id = self.find_closest(x, y)[0]
        return id
        

    def do_zoom_in(self, event) -> None:
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        scale = 1.1
        self.zoom_scale *= scale
        self.scale(ctk.ALL, x, y, scale, scale) 


    def do_zoom_out(self, event) -> None:
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        scale = 0.9
        self.zoom_scale *= scale
        self.scale(ctk.ALL, x, y, scale, scale) 

