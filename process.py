# coding=UTF-8
import os
from gtts import gTTS
import polars as pl

def getPath(*args):
    return os.path.join(*args)

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
    return os.path.isfile(file_path)

def iniFiles(df):

    for clase in set(df["folder"]):

        df2 = df.filter((pl.col("folder")==clase))
        if not(len(df2) == 0):
                
            dirClase = getPath(df2["root"][0], df2["folder"][0])
            createFolder(dirClase)

            filesFolder = os.listdir(dirClase) # get elements in directory
            filesFolder = [getPath(dirClase,n) for n in filesFolder] # add folder

            for fileName, sound in zip(df2["filename"], df2["sound"]):

                dir = getPath(df2["root"][0], df2["folder"][0], fileName)
                    
                if dir in filesFolder:
                    filesFolder.remove(dir) # remove elem from array

                if fileExists(dir) == False:
                    textToAudioFile(sound, dir, df2["root"][0].lower()[:2])

            # remove not needed file
            for m in filesFolder:
                os.remove(m)

def addElem(index, df):     
    out = pl.concat(
        [
            df[:index,:],
            pl.DataFrame(
                {
                    "spanish": ["Clase"+str(index)],
                    "sound": [""],
                    #"root": [""],
                    #"folder": [""],
                    #"filename": [""],
                }
            ),
            df[index:,:],
        ],
        how="vertical",
    )

    return out

def addClase(df):

    i=0
    cont=0
    maxCont=int(len(df)/20)
    
    while cont<=maxCont:
        if (i-cont)%20==0:
            cont+=1
            df = addElem(i, df)
            i+=1
        i+=1
            
    return df

def addElem(index, df):     
    out = pl.concat(
        [
            df[:index,:],
            pl.DataFrame(
                {
                    "spanish": ["Clase"+str(index)],
                    "sound": [""],
                    #"root": [""],
                    #"folder": [""],
                    #"filename": [""],
                }
            ),
            df[index:,:],
        ],
        how="vertical",
    )

    return out

def addClase(df):

    i=0
    cont=0
    maxCont=int(len(df)/20)
    
    while cont<=maxCont:
        if (i-cont)%20==0:
            cont+=1
            df = addElem(i, df)
            i+=1
        i+=1
            
    return df

def readAsDF(filename, rootFolder):
    df = pl.read_excel(
        file=filename,
        read_csv_options={"has_header": False, "new_columns": ["spanish", "sound"]},
    )
    df = df[:,:2]

    # remove clase
    df = df.filter(pl.col("spanish").str.starts_with("Clase") == False)

    # add Clase i separador
    df = addClase(df)

    # add root, folder, filename cols
    df = df.with_columns(pl.lit(rootFolder).alias('root'))
    df = df.with_columns(pl.lit("").alias('folder'))
    df = df.with_columns(pl.lit("").alias('filename'))

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
                    pl.col('sound').str.replace_all(rf'[*"<>|?¿!¡/]', ".") + ".mp3"
                    ).otherwise(
                        "ERROR").alias("filename")
        ]
    )
    
    # fill folder col
    folderName = ""
    vecSpanish = df["spanish"]

    i=0
    for elem in vecSpanish:

        if elem.startswith("Clase"):
            folderName = elem.replace(" ", "")
        else:
            df[i, "folder"] = folderName # remove those chars

        i+=1
    
    # remove clases
    df = df.filter(pl.col("spanish").str.starts_with("Clase") == False)


    return df

def createConfigFile(file_path):
    if not (fileExists(file_path)):
        f = open(file_path, "a")
        f.write("rootFolder=French")
        f.close()