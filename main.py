import process
import gui

if __name__ == "__main__":

    # generate base config file
    process.createConfigFile("config.txt")

    # load config data
    with open("config.txt", "r") as file:
        lines = file.readlines()

    rootFolder = lines[0].split("=")[1]
    filename = process.getPath("RawData"+"/"+rootFolder+".xlsx")
    lang = rootFolder.lower()

    # main df
    df = process.readAsDF(filename, rootFolder) 

    # initializing files
    process.iniFiles(df)

    app = gui.Win(df)
    app.mainloop()