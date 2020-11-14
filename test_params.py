import streamlit as st

param = st.text_input("Param")

if st.button("Button"):
    st.experimental_set_query_params(param=param)
    st.write(f"Set param: ?param={param}")
