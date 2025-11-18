import streamlit as st

import streamlit as st

def show():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to:", ["Home", "Selection", "Verbose"])

    if page == "Home": 
        print("In Home")
    if page == "Selection":
        import Selection
        Selection.show()
    elif page == "Verbose":
        import Verbose
        Verbose.show()

    st.title("HELLO")