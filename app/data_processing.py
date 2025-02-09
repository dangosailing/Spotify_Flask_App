import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from io import BytesIO
from matplotlib.dates import DateFormatter


def list_to_csv(data_list: list[dict], filename: str) -> None:
    """Converts a list of objects into a csv file"""
    df = pd.DataFrame(data_list)
    df.sort_values(by="release")
    df.to_csv(f"./app/data/{filename}")


def data_plot_to_base64(filename: str, x_col: str, y_col: str) -> str:
    """Reads the CSV file and converts it a into base64 string of the plot"""
    df = pd.read_csv(f"./app/data/{filename}")
    df["release"] = pd.to_datetime(df["release"])
    x = df[x_col]
    y = df[y_col]
    print(df["release"])
    fig = Figure()
    ax = fig.subplots()
    ax.set(xlabel="Release Date", ylabel="Popularity (0-100)")
    date_form = DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(date_form)
    ax.scatter(x, y)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")
