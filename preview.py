# A chromeless (code editor hidden) version of any particular snippet
import streamlit as st

from execbox_side import _new_sandbox
from utils import get_snippet, load_placeholder

st.set_page_config(page_title="Snippet Preview", page_icon=":rice_scene:")

# Download code by snippet_id
snippet_id = "iL_T1W23"
code = load_placeholder()
init_params = st.experimental_get_query_params()
if "snippet_id" in init_params:
    snippet_id = init_params["snippet_id"][0]
    code = get_snippet(snippet_id)

# Exec code here
try:
    local_scope = _new_sandbox()
    exec(code, local_scope)
except Exception as e:
    st.exception(e)

# Link back to the code editor
EDIT_URL = f"http://share.streamlit.io/akrolsmir/streamlit-snippet/main?snippet_id={snippet_id}"
st.write(f"*Clone and play with this Streamlit Snippet [here~]({EDIT_URL})*")
