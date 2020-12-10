import streamlit as st

st.write("# Current params")
st.write(st.experimental_get_query_params())

st.write("# Update params")
param = st.text_input("Param")

if st.button("Button"):
    st.experimental_set_query_params(param=param)
    st.write(f"Set param: ?param={param}")
