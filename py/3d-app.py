import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import LabelEncoder

st.title("3D Chart Generator (Supports CSV/XLSX + Text/Numeric Data)")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]

    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Select Excel Sheet", xls.sheet_names)
        df = xls.parse(sheet_name)

    st.subheader("Data Preview")
    st.dataframe(df)

    x_col = st.selectbox("X-axis", df.columns)
    y_col = st.selectbox("Y-axis", df.columns)
    z_col = st.selectbox("Z-axis (Height)", df.columns)

    row_start = st.number_input("Start row", 0, len(df)-1, 0)
    row_end = st.number_input("End row", row_start+1, len(df), len(df))
    df_subset = df.iloc[int(row_start):int(row_end)].dropna(subset=[x_col, y_col, z_col])

    chart_type = st.selectbox("Choose 3D Chart Type", [
        "3D Scatter", "3D Line", "3D Bar (Histogram)", "3D Surface", "3D Wireframe"
    ])

    def encode(series):
        if series.dtype == object or series.dtype.name == 'category':
            le = LabelEncoder()
            return le.fit_transform(series), dict(zip(le.transform(le.classes_), le.classes_))
        else:
            return series, None

    x_data, x_labels = encode(df_subset[x_col])
    y_data, y_labels = encode(df_subset[y_col])
    z_data = pd.to_numeric(df_subset[z_col], errors='coerce')

    fig = plt.figure(figsize=(20, 12))
    ax = fig.add_subplot(111, projection='3d')

    if chart_type == "3D Scatter":
        ax.scatter(x_data, y_data, z_data)
    elif chart_type == "3D Line":
        ax.plot(x_data, y_data, z_data)
    elif chart_type == "3D Bar (Histogram)":
        bins = st.slider("Number of bins", 2, 20, 10)
        hist, xedges, yedges = np.histogram2d(x_data, y_data, bins=bins)

        xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing="ij")
        xpos = xpos.ravel()
        ypos = ypos.ravel()
        zpos = np.zeros_like(xpos)

        dx = dy = (xedges[1] - xedges[0]) * 0.9
        dz = hist.ravel()

        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
        ax.set_zlabel("Frequency")
    elif chart_type == "3D Surface":
        try:
            xi = np.unique(x_data)
            yi = np.unique(y_data)
            xi, yi = np.meshgrid(xi, yi)
            zi = pd.pivot_table(df_subset, index=y_col, columns=x_col, values=z_col).values
            ax.plot_surface(xi, yi, zi, cmap='viridis')
        except:
            st.warning("Surface plots require a full 2D grid of data.")
    elif chart_type == "3D Wireframe":
        try:
            xi = np.unique(x_data)
            yi = np.unique(y_data)
            xi, yi = np.meshgrid(xi, yi)
            zi = pd.pivot_table(df_subset, index=y_col, columns=x_col, values=z_col).values
            ax.plot_wireframe(xi, yi, zi, color='gray')
        except:
            st.warning("Wireframe plots require a full 2D grid of data.")

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_col)

    if x_labels:
        ax.set_xticks(np.unique(x_data))
        ax.set_xticklabels([x_labels.get(i, str(i)) for i in np.unique(x_data)], rotation=45)

    if y_labels:
        ax.set_yticks(np.unique(y_data))
        ax.set_yticklabels([y_labels.get(i, str(i)) for i in np.unique(y_data)], rotation=45)

    st.pyplot(fig)
 