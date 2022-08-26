import pathlib

import pandas as pd

current = pathlib.Path(__file__).parent
file = current / "scores.csv"

if file.exists():
    df = pd.read_csv(file, index_col=0)  # type:ignore
    print(df)

    df.to_csv(file)

import pathlib

import pandas as pd

current = pathlib.Path(__file__).parent
file = current / "data.csv"
file2 = current / "data2.csv"


df = pd.read_csv(file, index_col=0)

print(df)

df2 = df.append({"name": "jiro", "score": 200}, ignore_index=True)

print(df2)

df2.to_csv(file2, index=True)
