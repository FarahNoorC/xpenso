import streamlit as st
import pandas as pd
import os

st.markdown(
    """
    <style>
     html, body, [class*="css"] {
        font-size: 26px !important; /* Slightly larger base font */
        font-family: 'Segoe UI', sans-serif;
    }
    /* All text inputs, textareas and number inputs */
    input[type="text"],
    input[type="number"],
    textarea {
        border: 2px solid #e4e2f6 !important;  /* mild blue */
        box-shadow: 0 0 6px 1px #e4e2f6 !important; /* soft blue glow */
        border-radius: 5px;
        padding: 6px 10px;
        transition: all 0.3s ease;
    }

    /* Also highlight on focus */
    input[type="text"]:focus,
    input[type="number"]:focus,
    textarea:focus {
        border-color: #e4e2f6 !important;
        box-shadow: 0 0 8px 2px #e4e2f6 !important;
        outline: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Default filename stored in session state
if 'filename' not in st.session_state:
    st.session_state.filename = "data.xlsx"
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0  # used to force form rebuild

def load_data(filename):
    if os.path.exists(filename):
        if filename.endswith('.xlsx'):
            return pd.read_excel(filename)
        elif filename.endswith('.csv'):
            return pd.read_csv(filename)
    return pd.DataFrame()

def save_data(df, filename):
    if filename.endswith('.xlsx'):
        df.to_excel(filename, index=False)
    elif filename.endswith('.csv'):
        df.to_csv(filename, index=False)

st.title("📊 Data Entry")

# Input for file name (with extension)
filename_input = st.text_input("Enter filename (with .xlsx or .csv):", value=st.session_state.filename)
if filename_input:
    st.session_state.filename = filename_input

# Load existing data from file
data = load_data(st.session_state.filename)

if data.empty:
    st.info("No existing data found. Please enter column names to create a new file.")
    cols_input = st.text_input("Enter column names (Name,Age,Country,...):", "")
    if cols_input:
        columns = [col.strip() for col in cols_input.split(',')]
        data = pd.DataFrame(columns=columns)
else:
    columns = list(data.columns)
    st.write("📂 Current Data:")
    st.dataframe(data)

if len(data.columns) > 0:
    st.subheader("➕ Add New Row")

    # Use form key from session state to force form reset
    with st.form(f"data_form_{st.session_state.form_key}"):
        new_data = {}
        for col in columns:
            new_data[col] = st.text_input(f"{col}", key=f"input_{col}")
        submit = st.form_submit_button("Add Row")

    if submit:
        new_row = pd.DataFrame([new_data])
        data = pd.concat([data, new_row], ignore_index=True)
        save_data(data, st.session_state.filename)
        st.success(f"✅ Row added and saved to `{st.session_state.filename}`")

        # Increment form_key to rebuild form and clear inputs
        st.session_state.form_key += 1

        # Reload and show updated data
        data = load_data(st.session_state.filename)
        st.write("📂 Updated Data:")
        st.dataframe(data)

# Download button
if os.path.exists(st.session_state.filename):
    with open(st.session_state.filename, "rb") as f:
        st.download_button(
            label="⬇️ Download File",
            data=f,
            file_name=st.session_state.filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            if st.session_state.filename.endswith(".xlsx") else "text/csv"
        )
