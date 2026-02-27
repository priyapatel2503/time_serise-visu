import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    df = pd.read_csv(
        "fcc-forum-pageviews.csv",
        parse_dates=["date"],
        index_col="date"
    )
    return df


def clean_data(df):
    df = df.copy()

    lower = df["value"].quantile(0.025)
    upper = df["value"].quantile(0.975)

    df = df[(df["value"] >= lower) & (df["value"] <= upper)]

    return df


def draw_line_plot():
    df = clean_data(load_data())
    df = df.copy()

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df.index, df["value"], color="blue")

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    plt.tight_layout()
    fig.savefig("line_plot.png")

    return fig


def draw_bar_plot():
    df = clean_data(load_data())
    df = df.copy()

    df["year"] = df.index.year
    df["month"] = df.index.month

    df_grouped = df.groupby(["year", "month"])["value"].mean().unstack()

    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    fig, ax = plt.subplots(figsize=(12, 6))

    df_grouped.plot(kind="bar", ax=ax)

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months", labels=month_names)

    plt.tight_layout()
    fig.savefig("bar_plot.png")

    return fig


def draw_box_plot():
    df = clean_data(load_data())
    df = df.copy()
    df.reset_index(inplace=True)

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    month_order = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    df["month_name"] = df["month"].apply(lambda x: month_order[x - 1])

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    years = sorted(df["year"].unique())
    year_data = [df[df["year"] == year]["value"] for year in years]

    axes[0].boxplot(year_data, labels=years)
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    month_data = [
        df[df["month_name"] == month]["value"]
        for month in month_order
    ]

    axes[1].boxplot(month_data, labels=month_order)
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    plt.tight_layout()
    fig.savefig("box_plot.png")

    return fig