# streamlit_file_to_json.py
import streamlit as st
import pandas as pd
import json
from io import StringIO, BytesIO
from docx import Document

st.title("📄 Multi-Format File to JSON Converter")
st.markdown("Upload text, CSV, Excel, or Word files and convert them into JSON.")

# Accept multiple file types
uploaded_file = st.file_uploader(
    "📂 Browse and select your file",
    type=["txt", "csv", "xlsx", "xls", "docx"]
)

def convert_docx_to_text(file):
    doc = Document(file)
    return [para.text for para in doc.paragraphs if para.text.strip()]

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "txt":
        content = uploaded_file.read().decode("utf-8")
        st.subheader("File Content Preview:")
        st.text_area("Preview:", content, height=200)

        # Convert to JSON
        lines = content.splitlines()
        json_data = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                json_data[key.strip()] = value.strip()
            elif line.strip():
                json_data.setdefault("lines", []).append(line.strip())

    elif file_type in ["csv"]:
        df = pd.read_csv(uploaded_file)
        st.subheader("Data Preview:")
        st.dataframe(df.head())
        json_data = json.loads(df.to_json(orient="records"))

    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)
        st.subheader("Data Preview:")
        st.dataframe(df.head())
        json_data = json.loads(df.to_json(orient="records"))

    elif file_type == "docx":
        paragraphs = convert_docx_to_text(uploaded_file)
        st.subheader("Word Document Preview:")
        st.text_area("Preview:", "\n".join(paragraphs), height=200)
        json_data = {"paragraphs": paragraphs}

    else:
        st.error("Unsupported file type!")
        json_data = {}

    # Show JSON and download button
    if json_data:
        st.subheader("Converted JSON:")
        st.json(json_data)

        st.download_button(
            label="💾 Download JSON",
            data=json.dumps(json_data, indent=4),
            file_name=f"{uploaded_file.name.split('.')[0]}.json",
            mime="application/json"
        )
else:
    st.info("Please upload a file to convert.")
