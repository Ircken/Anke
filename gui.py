import secrets
import tkinter
import tkinter.messagebox
import customtkinter
import pygame

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Win(customtkinter.CTk):
    def __init__(self, df):
        super().__init__()

        # dimensions
        self.xDim = 800
        self.yDim = 500

        # configure window
        self.title("Anke")
        self.resizable(0, 0)
        self.geometry(f"{self.xDim}x{self.yDim}")        

        # initialize widgets
        self.textbox=customtkinter.CTkTextbox(
            self, 
            width=self.xDim*0.9, 
            height=self.yDim*0.7,
            font=("Helvetica", 17),
            border_width=2,
            border_color="black",
        )
        self.btnPlay=customtkinter.CTkButton(
            self, 
            text="Play", 
            command = lambda: play_sound(self),
            font=("Helvetica", 17),
            corner_radius=5,
        ) 
        self.btn=customtkinter.CTkButton(
            self, 
            text="Show sentence", 
            command = lambda: changeText(self),
            font=("Helvetica", 17),
            corner_radius=5,
        ) 

        # general config
        self.textbox.configure(state="disabled")
        self.btnPlay.configure(state="disabled")  
        
        # config widgets position
        self.textbox.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.btn.place(relx=0.5, rely=0.83, anchor=tkinter.CENTER)
        self.btnPlay.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        # button's function
        def play_sound(self):

            global index
            # initialize mixer
            pygame.mixer.init()
            fileDir = df["root"][index]+"/"+df["folder"][index]+"/"+df["filename"][index]
            pygame.mixer.music.load(fileDir)
            pygame.mixer.music.play()

        # button's function
        def changeText(self):

            global index
            index = secrets.randbelow(len(df["filename"]))

            # enable text
            self.textbox.configure(state="normal")

            # input text
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", str(df["frenchSound"][index]+"\n\n"+df["spanish"][index]))  # insert at line 0 character 0
            
            # textbox tag
            self.textbox.tag_add("tag_name", "0.0", "end")
            self.textbox.tag_config("tag_name", justify='center')
        
            # set display state
            self.textbox.configure(state="disabled")
            self.btnPlay.configure(state="normal")  
