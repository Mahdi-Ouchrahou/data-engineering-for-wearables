import pandas as pd

def analyze(data: pd.DataFrame, folder: str, out) -> None:
    sep = "─" * 60
    lines = [
        sep,
        f"Experiment : {folder}",
        sep,
        f"Shape      : {data.shape[0]} rows x {data.shape[1]} columns",
        "",

    ]

    missing = data.isnull().sum()
    if missing.sum() == 0:
        lines.append("Missing values : none")
    else:
        lines.append("Missing values:")
        lines.append(missing.to_string())

    duration = data["time"].iloc[-1] - data["time"].iloc[0]
    sample_rate = len(data) / duration if duration > 0 else float("nan")
    lines += [
        "",
        f"Duration    : {duration:.3f} s",
        f"Sample rate : {sample_rate:.1f} Hz",
        "",
        "Descriptive statistics:",
        data.describe().to_string(),
        "",
    ]

    text = "\n".join(lines)
    print(text)
    out.write(text + "\n")
