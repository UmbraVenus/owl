import streamlit as st
st.set_page_config(layout="wide")

from multiapp import MultiApp
# import apps here
import reference
import files
import howto

# Do not delete this line, it ensures css is applied to the app
st.markdown('<style>' + open('assets/custom.css').read() + '</style>', unsafe_allow_html=True)

# initiate multiple app sidebar interface
app = MultiApp()

# add apps here, order matters
app.add_app("File(s) Parser", files.app)
app.add_app("Tutorial", howto.app) # To be done after all is finished
app.add_app("Reference", reference.app)

# run apps
app.run()