# streamlit_text_to_json.py
import streamlit as st
import json

st.title("📄 Text to JSON Converter")

# File uploader
uploaded_file = st.file_uploader("Upload your text file", type=["txt"])

if uploaded_file:
    # Read the file
    content = uploaded_file.read().decode("utf-8")
    st.subheader("File Content:")
    st.text(content)

    # Convert to JSON
    lines = content.splitlines()
    json_data = {}

    for line in lines:
        if ":" in line:  # key-value pair
            key, value = line.split(":", 1)
            json_data[key.strip()] = value.strip()
        elif line.strip():  # just a line of text
            json_data.setdefault("lines", []).append(line.strip())

    st.subheader("Converted JSON:")
    st.json(json_data)

    # Download button
    st.download_button(
        label="Download JSON",
        data=json.dumps(json_data, indent=4),
        file_name="output.json",
        mime="application/json"
    )
