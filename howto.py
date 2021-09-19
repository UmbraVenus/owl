import streamlit as st
from PIL import Image
img = Image.open("assets/img/edvisorly.png")

def app():
    st.title("Video Tutorial")
    #st.info("Video will be here once parser questions are answered, Friday at 4 PM!")

    st.video('https://youtu.be/8_WD8JqJvL8')
    st.caption("All rights reserved @Edvisorly & Sage Ren & Kuhu Sharma 2021")
    st.image(img, width = 200)
    # screen cast can be easily done on streamlit