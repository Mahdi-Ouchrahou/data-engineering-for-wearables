import os
import pandas as pd
import matplotlib.pyplot as plt


from load import load_data
from analyze import analyze
from visualize import create_figure, plot
from clean import clean

USE_CASE = [
    "accel-still-in-hand",
    "accel-still-in-pocket",
    "accel-walking-in-hand",
    "accel-walking-in-pocket",
]
CSV_NAME = "Raw Data.csv"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_FILE = os.path.join(BASE_DIR, "analysis.txt")



def main():
    fig, all_axes = create_figure(len(USE_CASE))

    with open(REPORT_FILE, "w", encoding="utf-8") as out:
        for i, folder in enumerate(USE_CASE):
            path = os.path.join(BASE_DIR, folder, CSV_NAME)

            data         = load_data(path)
            cleaned_data = clean(data)

            analyze(cleaned_data, folder, out)
            plot(cleaned_data, folder, all_axes[i])

    fig.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()
    print(f"\nReport written to {REPORT_FILE}")


if __name__ == "__main__":
    main()
    