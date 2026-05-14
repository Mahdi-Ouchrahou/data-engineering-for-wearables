import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt


ACCEL_COLS    = ["x", "y", "z"]
BANDPASS_LOW  = 0.3    # Hz - removes DC drift / slow sensor bias
BANDPASS_HIGH = 20.0   # Hz - removes high-frequency noise
FILTER_ORDER  = 4
MAD_THRESHOLD = 5.0    # spikes further than this many MADs from median get replaced


def remove_spikes(df):
    # Phone sensors occasionally produce single-sample spikes — readings that are
    # physically impossible (e.g. 50 m/s² from a still phone). If we filter first,
    # the filter smears each spike across neighbouring samples, making it worse.
    # We use MAD (Median Absolute Deviation) instead of z-score because MAD is
    # not affected by the outliers themselves — the median stays robust even when
    # a few values are extreme. Spikes are replaced with the median rather than
    # dropped so the time series stays continuous.
    df = df.copy()

    for col in ACCEL_COLS:
        median = df[col].median()
        mad    = (df[col] - median).abs().median()
        spikes = (df[col] - median).abs() > MAD_THRESHOLD * mad

        df.loc[spikes, col] = median

    return df


def bandpass(df):
    # A band-pass filter keeps only the frequency range we care about and removes
    # everything outside it.
    #
    # High-pass at 0.3 Hz: removes slow DC drift — a gradual offset that builds
    # up over time due to sensor bias or temperature. Without this, the baseline
    # slowly shifts and makes the signal hard to compare across experiments.
    #
    # Low-pass at 20 Hz: removes high-frequency noise from the sensor electronics.
    # Human motion (walking, running) lives between 1-10 Hz, so anything above
    # 20 Hz is pure noise. We use filtfilt (zero-phase) so the filter does not
    # shift the signal in time.
    dt          = df["time"].diff().median()
    sample_rate = 1.0 / dt
    nyquist     = sample_rate / 2.0

    low  = BANDPASS_LOW  / nyquist
    high = min(BANDPASS_HIGH / nyquist, 0.99)  # must stay below 1.0

    b, a = butter(FILTER_ORDER, [low, high], btype="band")
    df   = df.copy()

    for col in ACCEL_COLS:
        df[col] = filtfilt(b, a, df[col])

    # recompute magnitude from the filtered axes
    df["abs"] = np.sqrt((df[ACCEL_COLS] ** 2).sum(axis=1))
    return df




def clean(df):
    df = remove_spikes(df)  # 1. replace sensor spikes using MAD
    df = bandpass(df)       # 2. band-pass 0.3-20 Hz, removes drift and noise
    return df
