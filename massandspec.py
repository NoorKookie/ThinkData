import pandas as pd

# cleans the columns names
def interpret_mass_spectrometry_data(raw_df: pd.DataFrame):
    cleaned = raw_df.copy()
    cleaned.columns = [c.strip().lower() for c in cleaned.columns] 

    rename_map = {}
    for c in cleaned.columns:
        if c in ["mz", "m/z", "mass/charge", "mass"]:
            rename_map[c] = "mass/charge"
        elif c in ["intensity", "abundance", "counts"]:
            rename_map[c] = "intensity"
    cleaned = cleaned.rename(columns=rename_map)

    if "mass/charge" not in cleaned.columns or "intensity" not in cleaned.columns:
        raise ValueError("Could not find columns for mass/charge and intensity. Please ensure your CSV has these.")

    cleaned ["mass/charge"] = pd.to_numeric(cleaned["mass/charge"], errors="coerce")
    cleaned ["intensity"] = pd.to_numeric(cleaned["intensity"], errors="coerce")
    cleaned = cleaned.dropna(subset=["mass/charge", "intensity"]).sort_values("mass/charge").reset_index(drop=True)

    peak_row = cleaned.loc[cleaned["intensity"].idxmax()]
    base_mz = float(peak_row["mass/charge"])
    base_intensity = float(peak_row["intensity"])
    top5 = cleaned.sort_values("intensity", ascending=False).head(5)
    top5_mz = top5["mass/charge"].tolist()
    top5_mz_str = ", ".join([f"{mz:.2f}" for mz in top5_mz])
    tic = float(cleaned["intensity"].sum())
    mz_min = float(cleaned["mass/charge"].min())
    mz_max = float(cleaned["mass/charge"].max())
    mz_range = mz_max - mz_min

    bullets = [
        f"The base peak is at mass/intensity {base_mz:.2f} with an intensity of {base_intensity:.2f}.",
        f"The top 5 peaks are at mass/intensity values: {top5_mz_str}.",
        f"The total ion current (TIC) is {tic:.2f}.",
        f"The mass/intensity values range from {mz_min:.2f} to {mz_max:.2f}, giving a range of {mz_range:.2f}."
    ]

    explanation = (
    f"The strongest signal (base peak) occurs at m/z {base_mz:.2f}. "
    f"The most prominent peaks are around: {top5_mz_str}. "
    f"The total signal across the spectrum (TIC) is {tic:.2f}."
    )

    return {
        "cleaned_table": cleaned,
        "key_findings": bullets,
        "explanation": explanation,
    }