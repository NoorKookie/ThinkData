import pandas as pd

# cleans the columns names
def interpret_spectrometer_data(raw_df: pd.DataFrame):
    df= raw_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    rename_map = {}
    for c in df.columns:
        if c in ["wavelength", "wl", "nm", "lambda"]:
            rename_map[c] = "wavelength"
        elif c in ["intensity", "absorbance", "abs", "counts"]:
            rename_map[c] = "intensity"
    df = df.rename(columns=rename_map)

    if "wavelength" not in df.columns or "intensity" not in df.columns:
        raise ValueError("Could not find columns for wavelength and intensity. Please ensure your CSV has these.")

    df ["wavelength"] = pd.to_numeric(df["wavelength"], errors="coerce")
    df ["intensity"] = pd.to_numeric(df["intensity"], errors="coerce")
    df = df.dropna(subset=["wavelength", "intensity"]).sort_values("wavelength").reset_index(drop=True)

    peak_row = df.loc[df["intensity"].idxmax()]
    peak_wavelength = float(peak_row["wavelength"])
    peak_intensity = float(peak_row["intensity"])
    avg_intensity = float(df["intensity"].mean())
    min_intensity = float(df["intensity"].min())
    max_intensity = float(df["intensity"].max())

    trend = "increases overall" if df["intensity"].iloc[-1] > df["intensity"].iloc[0] else "decreases overall"

    bullets = [
        f"The peak wavelength is {peak_wavelength:.2f} nm with an intensity of {peak_intensity:.2f}.",
        f"The average intensity across all wavelengths is {avg_intensity:.2f}.",
        f"The minimum intensity is {min_intensity:.2f} and the maximum intensity is {max_intensity:.2f}.",
        f"The intensity {trend} across the spectrum."
    ]

    explantion = (
        f"The strongest signal is observed at {peak_wavelength:.2f} nm, which may indicate the presence of a specific compound or element that absorbs or emits light at that wavelength."
        f"The intensity ranges from {min_intensity:.2f} to {max_intensity:.2f}, with an average of {avg_intensity:.2f}."
        f"The signal {trend} across the scan."
    )

    return {
        "cleaned_table": df,
        "key_findings": bullets,
        "explanation": explantion
    }