import customtkinter as ctk

class Greet_window(ctk.CTkToplevel):
    def __init__(self, load_project, create_project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('400x170')
        self.title('Welcome')
        self.attributes('-type', 'dialog')
        self.attributes('-topmost', True)

        # Define grid
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=3)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)

        ctk.CTkLabel(self, text='Welcome to "Simple Tile Editor"!', font=('Arial', 24)).grid(row=0, column=0, columnspan=3)
        ctk.CTkButton(self, text='Load project', font=('Arial', 15), command=load_project).grid(row=1, column=0)
        ctk.CTkButton(self, text='Create new', font=('Arial', 15), command=create_project).grid(row=1, column=2)

