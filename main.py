import process
import gui
import os



if __name__ == "__main__":

    # generate base config file
    process.createConfigFile("config.csv")

    # load config data
    configDF = process.readConfigAsDF("config.csv")

    # config
    lang = configDF["lang"][0][:2]
    filename = configDF["filenameCSV"][0]
    rootFolder = configDF["rootFolder"][0]
    createFilesFile = configDF["createFilesFile"][0]

    # main df
    df = process.readAsDF(filename, rootFolder, createFilesFile) 

    # initializing files
    process.iniFiles()

    # erase auxiliar file
    os.remove(createFilesFile)

    app = gui.Win(df)
    app.mainloop()