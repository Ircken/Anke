import process
import gui

if __name__ == "__main__":

    # load config data
    configDF = process.readConfigAsDF("config.csv")

    # config
    lang = configDF["lang"][0][:2]
    filename = configDF["filenameCSV"][0]
    rootFolder = configDF["rootFolder"][0]

    # main df
    df = process.readAsDF(filename, rootFolder) 

    # initializing files
    process.iniFiles(df, lang)

    app = gui.Win(df)
    app.mainloop()