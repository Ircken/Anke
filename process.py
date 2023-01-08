# coding=UTF-8
import subprocess
import os
from gtts import gTTS
import polars as pl

def readFile(filename): 
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text

def readAsDF(filename):
    df = pl.read_csv(
    file=filename,
    encoding="Windows 1252",
    sep=";",
    columns=[0,1],
    has_header=False,
    )
    headers = df.columns # headers
    df = df.rename({headers[0]: 'spanish', headers[1]: 'frenchSound'}) # rename cols

    # add root, folder, filename cols
    df = df.with_column(pl.lit("Audio").alias('root'))
    df = df.with_column(pl.lit("").alias('folder'))
    df = df.with_column(pl.lit("").alias('filename'))

    # replace null and nan, drop duplicated rows
    df = df.fill_nan("")
    df = df.fill_null("")
    df = df.unique()

    """
    # add folder col
    #containsClase = vecSpanish.str.contains("Clase")
    #df = df.with_column(pl.lit(containsClase).alias('folder'))
    #df = df.with_column((pl.col("spanish").str.starts_with("Clase").alias("folder")))
    #df = df.with_column(pl.col('frenchSound').apply(lambda x: re.split(rx, x)).alias('filename'))
    #df = df.with_column(pl.col('frenchSound').str.replace(r'\$i', pl.col('frenchSound')).alias('result'))
    #df = df.with_column(pl.col('frenchSound').str.replace_all('\?', ".").alias('filename'))
    #df = df.with_column(pl.col('frenchSound').arr.eval(pl.all().str.replace_all("?", ".").alias('filename')))
    #df = df.select([pl.col("frenchSound").str.count_match("c").alias("filename")])
    """

    # remove chars
    df = df.with_columns(
        [
            pl.when(
                True
                ).then(
                    pl.col('frenchSound').str.replace_all(rf'[*"<>|?¿!¡/]', ".") + ".mp3"
                    ).otherwise(
                        "ERROR").alias("filename")
        ]
    )
    
    folderName = ""
    vecSpanish = df["spanish"]

    for i in range(len(vecSpanish)):
        if vecSpanish[i].startswith("Clase"):
            folderName = vecSpanish[i].replace(" ", "")
        else:
            df[i, "folder"] = folderName # remove those chars
    
    # remove clases
    df = df.filter(pl.col("spanish").str.starts_with("Clase") == False)

    return df

def textToAudioFile(mytext, directory, language):         
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save(directory)
    
    # Playing the converted file
    #os.system("welcome.mp3")

def createFolder(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

def fileExists(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False

"""
def iniFiles(df, lang):

    # create folder
    createFolder(df["root"][0])    

    # create audio and folders
    for i in range(len(df["root"])):
        folder = df["root"][i]+"/"+df["folder"][i]
        createFolder(folder)
        dir = folder+"/"+df["filename"][i]
        # if not exists, create file
        if not(fileExists(dir)):
            textToAudioFile(df["frenchSound"][i], dir, lang)
"""
def iniFiles():
    subprocess.check_call("AudioCreator.exe")

def readAsDF(filename, rootFolder, createFilesFile):
    df = pl.read_csv(
        file=filename,
        encoding="Windows 1252",
        sep=";",
        columns=[0,1],
        has_header=False,
    )
    headers = df.columns # headers
    df = df.rename({headers[0]: 'spanish', headers[1]: 'frenchSound'}) # rename cols

    # add root, folder, filename cols
    df = df.with_column(pl.lit(rootFolder).alias('root'))
    df = df.with_column(pl.lit("").alias('folder'))
    df = df.with_column(pl.lit("").alias('filename'))

    # replace null and nan, drop duplicated rows
    df = df.fill_nan("")
    df = df.fill_null("")
    df = df.unique()

    # remove chars
    df = df.with_columns(
        [
            pl.when(
                True
                ).then(
                    pl.col('frenchSound').str.replace_all(rf'[*"<>|?¿!¡/]', ".") + ".mp3"
                    ).otherwise(
                        "ERROR").alias("filename")
        ]
    )
    
    # fill folder col
    folderName = ""
    vecSpanish = df["spanish"]

    for i in range(len(vecSpanish)):

        if vecSpanish[i].startswith("Clase"):
            folderName = vecSpanish[i].replace(" ", "")
        else:
            df[i, "folder"] = folderName # remove those chars
    
    # remove clases
    df = df.filter(pl.col("spanish").str.starts_with("Clase") == False)

    # save to create audio files
    dfSave = df[:,1:]
    dfSave.write_csv(createFilesFile, sep=";")

    return df

def readConfigAsDF(filename):
    df = pl.read_csv(
        file=filename,
        encoding="Windows 1252",
        sep=";",
        has_header=True,
    )

    # replace null and nan, drop duplicated rows
    df = df.fill_nan("")
    df = df.fill_null("")
    df = df.unique()

    return df

def createConfigFile(file_path):
    if not (os.path.isfile(file_path)):
        f = open(file_path, "a")
        f.write("lang;filenameCSV;rootFolder;createFilesFile\nfrench;French.csv;French;dataFiles.csv")
        f.close()