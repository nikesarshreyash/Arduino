import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
st.title("Welcome to chatgpt Go")
st.text_input("Ask your question")

st.write("This is our first streamlit app")
st.text("Let's get started")

name = st.text_input("Enter you name")
if st.button("Greet") :
    st.success(f"Hello {name}")
    
# How to upload csv file

upload_file = st.file_uploader("Upload a csv file", type = "csv")
if upload_file :
    df = pd.read_csv(upload_file)
    st.dataframe(df)
    
st.header(" This is a header") 
st.subheader("This is a subheader")
st.markdown("[Github](https://github.com/nikesarshreyash)")
st.text_area('Enter your message : ')

level = st.slider("Choose a level", min_value=1, max_value=5)
st.write(f"Selected level: {level}")


result = st.selectbox("Select Language:", ['Python', 'Java', 'CPP'])
st.write(f"You selected {result} language")

languages = st.multiselect("Select Language:", ['Python', 'Java', 'CPP'])
st.write("You selected", len(languages), "languages")

#form tag
with st.form("login form"):
    username = st.text_input("Enter username")
    password = st.text_input("passowrd", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        st.success(f"Welcome, {username}")

df = pd.DataFrame(np.random.randn(20,3) , columns=["A","B","C"])
st.line_chart(df)
st.area_chart(df)
st.bar_chart(df)

st.video("https://www.youtube.com/watch?v=ZVp0GFFSyAc")
st.image("https://pictures.altai-travel.com/1920x0/mount-everest-aerial-view-himalayas-istock-3745.jpg",caption = "Mountains")