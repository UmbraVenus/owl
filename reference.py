import streamlit as st
from PIL import Image
img = Image.open("assets/img/edvisorly.png")
kuhugithub = "https://github.com/kuhusharma"
sagegithub = "https://github.com/umbravenus"
kuhulinkedin = "https://www.linkedin.com/in/kuhusharma/"
sagelinkedin = "https://www.linkedin.com/in/sage-r-312631203/"

def app():
    st.title("Authors")
    st.markdown("---")
    st.header("Sage Ren")
    st.write("Check out [my github](%s)" % sagegithub)
    st.write("Connect with me [on Linkedin](%s)" % sagelinkedin)
    st.markdown("---")
    st.header("Kuhu Sharma")
    st.write("Check out [my github](%s)" % kuhugithub)
    st.write("Connect with me [on Linkedin](%s)" % kuhulinkedin)
    st.markdown("---")
    st.caption("All rights reserved @Edvisorly & Sage Ren & Kuhu Sharma 2021")
    st.markdown("---")
    # Here could be an iframe of edvisorly
    st.image(img, width = 500)

