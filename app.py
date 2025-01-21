import streamlit as st
import openai
import os

# Function to convert scripts between languages using OpenAI API
def convert_script(source_script, source_language, target_language, api_key):
    # Set the OpenAI API key from the form data
    openai.api_key = api_key

    prompt = (
        f"Convert the following {source_language} script into {target_language} syntax, "
        f"return only the equivalent expression, without any explanation:\n\n"
        f"{source_script}\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant that helps convert between different scripting languages."},
                      {"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.3,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Custom CSS for dark mode and styling
st.markdown("""
    <style>
    html, body {
        background-color: #121212;  /* Dark background for the entire page */
        color: #FFFFFF;  /* White text for the body */
        margin: 0;
        padding: 0;
        height: 100%;
    }
    .stApp {
        background-color: #121212;  /* Ensure the entire app background is dark */
    }
    .stButton>button {
        background-color: #6200EE;  /* Light purple for the button */
        color: white;
        border: none;
        border-radius: 4px;
        font-size: 1.1em;
        cursor: pointer;
        padding: 12px 20px;
    }
    .stButton>button:hover {
        background-color: #3700B3;  /* Darker purple on hover */
    }
    .stTextInput>div>div>input {
        background-color: #333333;  /* Dark grey background for text input */
        color: #FFFFFF;  /* White text for text input */
        border: 1px solid #444444;  /* Slightly lighter grey border */
        border-radius: 4px;
        padding: 10px;
    }
    .stTextInput label {
        color: #FFFFFF;  /* White text for the label above the input */
    }
    .stSelectbox>div>div>div {
        background-color: #333333;  /* Dark grey background for select box */
        color: #FFFFFF;  /* White text for select box */
       /* border: 1px solid #444444;   Slightly lighter grey border */
        border-radius: 4px;
        padding: 10px;
        height: 150%;
    }
    .stSelectbox label {
        color: #FFFFFF;  /* White text for the label above the input */
        font-size: 1.1em;  /* Slightly larger label text */
    }
    .stFileUploader>div>div>div {
        background-color: #333333;  /* Dark grey background for file uploader */
        color: #FFFFFF;  /* White text for file uploader */
        border: 1px solid #444444;  /* Slightly lighter grey border */
        border-radius: 4px;
        padding: 10px;
    }
    .stFileUploader label {
        color: #FFFFFF;  /* White text for the label above the input */
        font-size: 1.1em;  /* Slightly larger label text */
    }
    /* Targeting the title (h1) to make the text white */
    h1 {
        color: #FFFFFF !important;  /* White color for the title text */
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
st.title("BI Migrator")

# OpenAI API Key Input
api_key = st.text_input("Enter OpenAI API Key:", type="password")

# Language Selection
source_language = st.selectbox("Source Language:", ["Qlik", "SQL", "Power BI DAX", "Looker", "Python", "R", "JavaScript"])
target_language = st.selectbox("Target Language:", ["Qlik", "SQL", "Power BI DAX", "Looker", "Python", "R", "JavaScript"])

# File Upload
uploaded_file = st.file_uploader("Upload Script File:")

if st.button("Convert"):
    if not api_key:
        st.error("API key is required")
    elif not uploaded_file:
        st.error("No file uploaded")
    else:
        # Read and process the uploaded file
        file_content = uploaded_file.read().decode('utf-8')
        scripts = file_content.splitlines()

        # Convert scripts using OpenAI API
        converted_scripts = [convert_script(script, source_language, target_language, api_key) for script in scripts]

        output_filename = 'converted_scripts.txt'
        with open(output_filename, 'w') as output_file:
            for script in converted_scripts:
                output_file.write(script + "\n")

        st.success("File converted successfully!")
        st.download_button("Download Converted Scripts", data=open(output_filename).read(), file_name=output_filename)

