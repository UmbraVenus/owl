import streamlit as st

def app():
    st.title("AWCA x OwlHacks")

    # the app will only execute if the user chooses submit
    with st.form("my_form"):
        # uploaded files
        uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Parse!")
        # this is just to display the file names, will add function later
        if submitted:
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                st.write("filename:", uploaded_file.name)
                st.write(bytes_data)
    
    text_contents = '''
        Col1, Col2
        123, 456
        789, 000
    '''

    st.download_button(
        label="download",
        data=text_contents,
        file_name="file.json"
    )

