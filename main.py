import processing
import gui


if __name__ == "__main__":

    filename = "French.csv"
    df = processing.readAsDF(filename)
    processing.iniFiles(df, "fr")

    app = gui.Win(df)
    app.mainloop()