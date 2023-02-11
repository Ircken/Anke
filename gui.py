import secrets
import tkinter
import tkinter.messagebox
import pygame
import eng_to_ipa as ipa

global index

class Win(tkinter.Tk):
    def __init__(self, df):
        super().__init__()

        # dimensions
        self.xDim = 800
        self.yDim = 500

        # configure window
        self.config(bg='#202020')
        self.title("Anke")
        self.resizable(0, 0)
        self.geometry(f"{self.xDim}x{self.yDim}")  

        # button config 
        btnColor = "0078ff"    
        btnFont = ("Helvetica", 13)
        textColor = "white"

        # initialize widgets
        self.btnPlay=tkinter.Button(
            self, 
            text="Play", 
            command = lambda: play_sound(self),
            font=btnFont,
            bg='#'+btnColor,
            width=13, 
            height=1,
            foreground=textColor,
        ) 
        self.btn=tkinter.Button(
            self, 
            text="Show sentence", 
            command = lambda: changeText(self),
            font=btnFont,
            bg='#'+btnColor,
            width=13, 
            height=1,
            foreground=textColor,
        ) 
        self.textbox= tkinter.Text(
            self, 
            bd=0, 
            width=int(self.xDim*0.07), 
            height=int(self.yDim*0.027),
            font=("Helvetica", 17),
            bg='#3f3f3f',
            highlightbackground='black', 
            highlightcolor='black', 
            highlightthickness=2,
            foreground=textColor,
        )

        # general config
        self.textbox.configure(state="disabled")
        self.btnPlay.configure(state="disabled")  
        
        # config widgets position
        self.textbox.place(relx=0.5, rely=0.39, anchor=tkinter.CENTER)
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

            # phonetic
            phonetic = ""
            if df["root"][0] == "English":
                phonetic = "\n\n"+ipa.convert((df["sound"][index]))
            elif df["root"][0] == "French":
                phonetic = "\n\n"
            else:
                phonetic = "\n\n"

            # enable text
            self.textbox.configure(state="normal")

            # input text
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", str(
                "\n\n\n"+
                df["sound"][index]+
                "\n\n"+
                df["spanish"][index]+
                phonetic
            ))  # insert at line 0 character 0
            
            # textbox tag
            self.textbox.tag_add("tag_name", "0.0", "end")
            self.textbox.tag_config("tag_name", justify='center')
        
            # set display state
            self.textbox.configure(state="disabled")
            self.btnPlay.configure(state="normal")  
    