import matplotlib.pyplot as plt


AXES = [
    ("x", "Acceleration X", "#e74c3c"),
    ("y", "Acceleration Y", "#2ecc71"),
    ("z", "Acceleration Z", "#3498db"),
]


def create_figure(n):
    fig, axes = plt.subplots(n, 3, figsize=(16, 3.5 * n), sharey=False)
    fig.suptitle("Accelerometer Data", fontsize=14, fontweight="bold")
    return fig, axes


def plot(df, name, row_axes):
    for ax, (col, label, color) in zip(row_axes, AXES):
        ax.plot(df["time"], df[col], color=color, linewidth=0.8)
        ax.set_ylabel("m/s2", fontsize=9)
        ax.set_title(f"{name} - {label}", fontsize=9, loc="left")
        ax.grid(True, linewidth=0.4, alpha=0.6)

    row_axes[-1].set_xlabel("Time (s)", fontsize=9)