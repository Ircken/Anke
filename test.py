import polars as pl

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

df = readConfigAsDF("config.csv")

print(df)