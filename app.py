import streamlit as st
st.set_page_config(layout="wide")

from multiapp import MultiApp
# import apps here
import reference
# comment placeholder
import placeholder

st.markdown('<style>' + open('assets/custom.css').read() + '</style>', unsafe_allow_html=True)

# initiate multiple app sidebar interface
app = MultiApp()

# add apps here, order matters
app.add_app("Placeholder",placeholder.app)
app.add_app("Reference", reference.app)


# run apps
app.run()