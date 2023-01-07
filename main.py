import processing
import gui
import processing

if __name__ == "__main__":

    configDF = processing.readConfigAsDF("config.csv")

    # config
    lang = configDF["lang"][0][:2]
    filename = configDF["filenameCSV"][0]
    rootFolder = configDF["rootFolder"][0]

    # main df
    df = processing.readAsDF(filename, rootFolder) 

    # initializing files
    processing.iniFiles(df, lang)

    app = gui.Win(df)
    app.mainloop()