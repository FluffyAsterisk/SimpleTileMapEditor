import customtkinter as ctk

class Application(ctk.CTk):
    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)

        # Base settings
        self.title('Simple tile editor')
        self.geometry('800x500')
        self.attributes('-type', 'dialog')

        self.greet_user()
    
    def greet_user(self) -> None:
        window = GreetWindow(self)
        window.grab_set()

    def load_project(self) -> None:
        pass

    def create_project(self) -> None:
        pass

class GreetWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)

        self.geometry('400x200')
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
        ctk.CTkButton(self, text='Load project', font=('Arial', 15), command=self.master.load_project).grid(row=1, column=0)
        ctk.CTkButton(self, text='Create new', font=('Arial', 15), command=self.master.create_project).grid(row=1, column=2)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
