import streamlit as st
from newer_script import *
from zipfile import ZipFile
import os
import base64
from pathlib import Path

def save_uploadedfile(uploadedfile):
    with open(os.path.join(uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())

def app():
    my_json = Path("parsed_json.zip")
    my_csv = Path("parsed_csv.zip")

    st.title("AWCA x OwlHacks")

    if my_json.exists():
        os.remove("parsed_json.zip")
    if my_csv.exists():
        os.remove("parsed_csv.zip")

    # the app will only execute if the user chooses submit
    with st.form("my_form"):
        # uploaded files
        uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            save_uploadedfile(uploaded_file)

        global zip
        global zip2

        # Every form must have a submit button.
        submitted = st.form_submit_button("1.Parse!")
        # this is just to display the file names, will add function later
        if submitted:

            i = 1
            with ZipFile('parsed_json.zip', 'w') as zip:
                with ZipFile('parsed_csv.zip', 'w') as zip2:
                    for uploaded_file in uploaded_files:
                        df = read_table(uploaded_file.name)
                        final_object = get_object(df, uploaded_file.name)
                        get_json(final_object, str(i) + ".json")
                        df.to_csv(str(i)+".csv")
                        zip.write(str(i) + ".json")
                        zip2.write(str(i) + ".csv")
                        os.remove(str(i) + ".json")
                        os.remove(str(i) + ".csv")
                        os.remove(uploaded_file.name)
                        i += 1
            st.balloons()

    col1, col2 = st.columns(2)
    

    st.header("wait for the ballons to appear to download~")
    with col1:
        with open("parsed_json.zip", "rb") as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download=\'parsed_json.zip\'>\
            2.Click to download JSON\
            </a>'
            st.markdown(href, unsafe_allow_html=True)
    with col2:
        with open("parsed_csv.zip", "rb") as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/zip;base64,{b64}" download=\'parsed_csv.zip\'>\
            3.Click to download CSV\
            </a>'
            st.markdown(href, unsafe_allow_html=True)
    
        

    

