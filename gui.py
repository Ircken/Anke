# coding=UTF-8
import secrets
import tkinter
import customtkinter
import pygame
import processing

array = []
index = 0

def cajaTexto(w, xDim, yDim):
    txtbox= customtkinter.CTkTextbox(
        w, 
        width=xDim*0.9, 
        height=yDim*0.7,
        #fg_color="grey",
        font=("Helvetica", 17),
        border_width=2,
        border_color="black",
        
    )
    
    return txtbox

def boton(w, changeText, text):
    return customtkinter.CTkButton(
        w, 
        #borderwidth = 0,
        text=text, 
        #fg='white',
        #bg="black",
        command = changeText,
        font=("Helvetica", 17),
        corner_radius=5,
        #height= 5, 
        #width=10
    )   

def finalWidgets(w, xDim, yDim, df):
    # initialize widgets
    textbox=cajaTexto(w, xDim, yDim)
    btnPlay=boton(w, lambda: play_sound(df), "Play")
    btn=boton(w, lambda: changeText(textbox, df, btnPlay), "Show sentence")

    # general config
    textbox.configure(state="disabled")
    btnPlay.configure(state="disabled")  
    
    # config widgets position
    textbox.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    btn.place(relx=0.5, rely=0.83, anchor=tkinter.CENTER)
    btnPlay.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

# button's function
def play_sound(df):

    global index
    # initialize mixer
    pygame.mixer.init()
    fileDir = df["root"][index]+"/"+df["folder"][index]+"/"+df["filename"][index]
    pygame.mixer.music.load(fileDir)
    pygame.mixer.music.play()

# button's function
def changeText(textbox, df, btnPlay):

    global index
    index = secrets.randbelow(len(df["filename"]))

    # enable text
    textbox.configure(state="normal")

    # input text
    textbox.delete("0.0", "end")
    textbox.insert("0.0", str(df["frenchSound"][index]+"\n\n"+df["spanish"][index]))  # insert at line 0 character 0
    
    # textbox tag
    textbox.tag_add("tag_name", "0.0", "end")
    textbox.tag_config("tag_name", justify='center')
   
    # set display state
    textbox.configure(state="disabled")
    btnPlay.configure(state="normal")  

def display(df):

    customtkinter.set_appearance_mode("dark")  # Modes: light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    w=customtkinter.CTk()

    # dimensions
    xDim = 800
    yDim = 500

    # w config
    w.title('Anke')
    #w.configure(bg="black")
    w.resizable(0, 0)
    w.geometry(str(xDim)+"x"+str(yDim)) 

    # init files and finalWidgets
    processing.iniFiles(df, "fr")
    
    # init and config widgets
    finalWidgets(w, xDim, yDim, df)

    w.mainloop()