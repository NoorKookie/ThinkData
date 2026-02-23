import pandas as pd
import streamlit as st

# cleans the columns names
def interpret_microscope_counts_data(raw_df: pd.DataFrame):
    clean = raw_df.copy()
    clean.columns = [c.strip().lower() for c in clean.columns] 

    rename_map = {}
    for c in clean.columns:
        if c in ["sample", "image", "field", "location"]:
            rename_map[c] = "Sample"
        elif c in ["cell count", "count", "cells", "image", "field", "sample", "cell_count", "n_cells", "num_cells", "cellcount"]:
            rename_map[c] = "Cell Count"

    clean = clean.rename(columns=rename_map)

    if "Cell Count" not in clean.columns or "Sample" not in clean.columns:
        raise ValueError("Could not find columns for Cell Count or Sample. Please ensure your CSV has these columns.")

    clean ["Cell Count"] = pd.to_numeric(clean["Cell Count"], errors="coerce")
    clean ["Sample"] = pd.to_numeric(clean["Sample"], errors="coerce") if clean["Sample"].dtype == "object" else clean["Sample"]
    clean = clean.dropna(subset=["Cell Count"]).sort_values("Cell Count").reset_index(drop=True)

    total_cells = float(clean["Cell Count"].sum())
    avg_cells = float(clean["Cell Count"].mean())
    min_cells = float(clean["Cell Count"].min())
    max_rows = clean.loc[clean["Cell Count"].idxmax()]
    max_sample = str(max_rows["Sample"])
    max_count = float(max_rows["Cell Count"])
    max_sample = str(max_rows["Sample"])

    std = float(clean["Cell Count"].std())
    spread = float(clean["Cell Count"].max() - clean["Cell Count"].min())

    bullets = [
        f"The total cell count across all samples is {total_cells:.2f}.",
        f"The average cell count per sample is {avg_cells:.2f}.",
        f"The minimum cell count in a sample is {min_cells:.2f} and the maximum is {max_count:.2f} (in sample {max_sample}).",
        f"The standard deviation of cell counts across samples is {std:.2f}, with a range of {spread:.2f}."
    ]

    explanation = (
        f"Across {len(clean)} samples, the total count is {total_cells:.0f}. "
        f"On average, each sample has about {avg_cells:.2f} counts. "
        f"The highest value is {max_count:.0f} in sample '{max_sample}', "
        f"and counts range down to {min_cells:.0f}. "
        f"The variability (std dev) is {std:.2f}, which indicates how consistent the counts are across samples."
    )

    return {
        "cleaned_table": clean,
        "key_findings": bullets,
        "explanation": explanation,
    }