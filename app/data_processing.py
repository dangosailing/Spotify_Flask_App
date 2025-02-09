import pandas as pd
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
    # Noticed some dates only contained the year, this prevents them from raising an error
    df["release"] = pd.to_datetime(df["release"], errors="coerce")
    x = df[x_col]
    y = df[y_col]

    fig = Figure()
    ax = fig.subplots()
    ax.set(xlabel="Release Date", ylabel="Popularity (0-100)")
    date_form = DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_tick_params(labelrotation=20)
    ax.xaxis.set_label_position(position="top")
    ax.scatter(x, y)
    # Save it to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")
