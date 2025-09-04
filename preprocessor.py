import pandas as pd


def preprocess(df, region_df):
    # filter for Summer Olympics only
    df = df[df["Season"] == "Summer"].copy()

    # merge with region_df
    df = df.merge(region_df, on="NOC", how="left")

    # drop exact duplicates
    df = df.drop_duplicates()

    # one-hot encode medals (Gold/Silver/Bronze) — NaNs are ignored
    medal_dummies = pd.get_dummies(df["Medal"])
    df = pd.concat([df, medal_dummies], axis=1)

    return df
