import numpy as np
import pandas as pd


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )

    # Filters
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
        groupby_key = "region"
    elif year == "Overall" and country != "Overall":
        temp_df = medal_df[medal_df["region"] == country]
        groupby_key = "Year"
    elif year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(year)]
        groupby_key = "region"
    else:
        temp_df = medal_df[
            (medal_df["Year"] == int(year)) & (medal_df["region"] == country)
        ]
        groupby_key = "region"

    # Aggregate only medal columns to avoid numeric_only issues
    agg_cols = ["Gold", "Silver", "Bronze"]
    grouped = temp_df.groupby(groupby_key, sort=True)[agg_cols].sum().reset_index()

    if groupby_key == "Year":
        grouped = grouped.sort_values("Year")
    else:
        grouped = grouped.sort_values("Gold", ascending=False)

    grouped["total"] = grouped["Gold"] + grouped["Silver"] + grouped["Bronze"]

    return grouped.astype(
        {"Gold": "int", "Silver": "int", "Bronze": "int", "total": "int"}
    )


def country_year_list(df):
    years = sorted(df["Year"].unique().tolist())
    years.insert(0, "Overall")

    country = sorted(np.unique(df["region"].dropna().values).tolist())
    country.insert(0, "Overall")

    return years, country


def data_over_time(df, col):
    """
    Returns a DataFrame with columns:
    - 'Edition' (Year)
    - <col> (count of unique entries per edition)
    """
    temp = df.drop_duplicates(["Year", col])
    counts = temp["Year"].value_counts().sort_index()
    out = counts.rename(col).rename_axis("Edition").reset_index()
    return out


def most_successful(df, sport):
    temp_df = df.dropna(subset=["Medal"])
    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]

    top = (
        temp_df["Name"]
        .value_counts()
        .head(15)
        .rename_axis("Name")
        .reset_index(name="Medals")
        .merge(df[["Name", "Sport", "region"]], on="Name", how="left")
        .drop_duplicates("Name")[["Name", "Medals", "Sport", "region"]]
    )
    return top


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )
    new_df = temp_df[temp_df["region"] == country]
    final_df = (
        new_df.groupby("Year", sort=True)["Medal"].count().reset_index(name="Medal")
    )
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )
    new_df = temp_df[temp_df["region"] == country]
    pt = new_df.pivot_table(
        index="Sport", columns="Year", values="Medal", aggfunc="count"
    ).fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df[temp_df["region"] == country]

    top = (
        temp_df["Name"]
        .value_counts()
        .head(10)
        .rename_axis("Name")
        .reset_index(name="Medals")
        .merge(df[["Name", "Sport"]], on="Name", how="left")
        .drop_duplicates("Name")[["Name", "Medals", "Sport"]]
    )
    return top


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=["Name", "region"]).copy()
    athlete_df["Medal"] = athlete_df["Medal"].fillna("No Medal")
    if sport != "Overall":
        return athlete_df[athlete_df["Sport"] == sport]
    return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    men = (
        athlete_df[athlete_df["Sex"] == "M"]
        .groupby("Year", sort=True)["Name"]
        .count()
        .reset_index(name="Male")
    )
    women = (
        athlete_df[athlete_df["Sex"] == "F"]
        .groupby("Year", sort=True)["Name"]
        .count()
        .reset_index(name="Female")
    )

    final = men.merge(women, on="Year", how="left").fillna(0)
    return final
