import os
import sys
from time import time
import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError
import time


st.set_page_config(
    page_title="ThinkData - A data interpreation tool!",
    page_icon="📊",
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interpreters.massandspec import interpret_mass_spectrometry_data
from interpreters.spectrometer import interpret_spectrometer_data
from interpreters.microscopecounters import interpret_microscope_counts_data

st.title("ThinkData")
tool = st.selectbox(
    "What tool produced your data?",
    [" ", "Spectrometer", "Mass Spectrometry", "Microscope Counts"]
)

# Keep a dataframe in session so it doesn't disappear on reruns
if "df" not in st.session_state:
    st.session_state.df = None

st.divider(width="stretch")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

st.subheader("OR", text_alignment="center")

use_sample = st.button("Use Sample Data", icon_position="right", type="secondary", width="stretch")

st.divider(width="stretch")


preview_clicked = st.button("Preview Data", type="primary")

if uploaded_file is not None and preview_clicked:
    try:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success(f"Loaded file: {uploaded_file.name} — {st.session_state.df.shape[0]} rows, {st.session_state.df.shape[1]} columns")
    except EmptyDataError:
        st.session_state.df = None
        st.warning("The uploaded file is empty.")

if st.session_state.df is not None:
    st.header("Raw Data Preview")
    st.dataframe(st.session_state.df.head(20), use_container_width=True)
else:
    st.info("No data is uploaded yet")



if use_sample:
    if tool == "Spectrometer":
        sample_path = "sample-data/spectrometer_sample.csv"
    elif tool == "Mass Spectrometry":
        sample_path = "sample-data/mass_spec_sample.csv"
    else:
        sample_path = "sample-data/microscope_counts_sample.csv"

    st.session_state.df = pd.read_csv(sample_path)

st.divider(width="stretch")

clicked = st.button("Interpret Data", type="primary")

if clicked:
    with st.spinner("Interpreting data...", show_time=True):
        time.sleep(5)  


if clicked and tool == "Spectrometer":
    if st.session_state.df is None:
        st.warning("Please upload a CSV and click Preview Data (or click Use Sample Data) first.")
    else:
        try:
            results = interpret_spectrometer_data(st.session_state.df)

            cleaned = results.get("cleaned_table")
            findings = results.get("key_findings", [])
            explanation = results.get("explanation", "")

            left, right = st.columns ([1.2, 1])

            with left:
                st.markdown("### Cleaned Data")
                st.dataframe(cleaned.head(20), use_container_width=True)

            with right:
                st.markdown("### Chart")
                chart_df = cleaned.set_index("wavelength")[["intensity"]]
                st.line_chart(chart_df)
            
            st.markdown("### Key Findings")
            for bullet in findings:
                st.markdown(f"- {bullet}")
        
            st.markdown("### Explanation")
            st.write(explanation)

        except Exception as e:
            st.error(f"Error interpreting data: {str(e)}")
if clicked and tool == "Mass Spectrometry":
    if st.session_state.df is None:
        st.warning("Mass Spectrometry interpretation is not implemented yet. Please check back soon!")
    else:
        try:
            results = interpret_mass_spectrometry_data(st.session_state.df)

            cleaned = results.get("cleaned_table")
            findings = results.get("key_findings", [])
            explanation = results.get("explanation", "")

            left, right = st.columns ([1.2, 1])

            with left:
                st.markdown("### Cleaned Data")
                st.dataframe(cleaned.head(20), use_container_width=True)
            with right:
                st.markdown("### Chart")
                chart_df = cleaned.set_index("mass/charge")[["intensity"]]
                st.line_chart(chart_df)
            
            st.markdown("### Key Findings")
            for bullet in findings:
                st.markdown(f"- {bullet}")
            
            st.markdown("### Explanation")
            st.write(explanation)

        except Exception as e:
            st.error(f"Error interpreting data: {str(e)}")
if clicked and tool == "Microscope Counts":
    if st.session_state.df is None:
        st.warning("Microscope Counts interpretation is not implemented yet. Please check back soon!")
    else:
        try:
            results = interpret_microscope_counts_data(st.session_state.df)

            cleaned = results.get("cleaned_table")
            findings = results.get("key_findings", [])
            explanation = results.get("explanation", "")

            left, right = st.columns([1.2, 1])

            with left:
                st.markdown("### Cleaned Data")
                st.dataframe(cleaned.head(20), use_container_width=True)
            
            with right:
                st.markdown("### Chart")
                chart_df = cleaned.set_index("Sample")[["Cell Count"]]
                st.bar_chart(chart_df)

            st.markdown("### Key Findings")
            for bullet in findings:
                st.markdown(f"- {bullet}")
            
            st.markdown("### Explanation")
            st.write(explanation)

        except Exception as e:
            st.error(f"Error interpreting data: {str(e)}")


        