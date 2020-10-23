import streamlit as st
import requests

from execbox_side import execbox_side

st.beta_set_page_config(layout="wide")

RUN_URL = "https://firestore.googleapis.com/v1/projects/plain-twig/databases/(default)/documents/"

# These could be generalized to other apps using Firestore
def get_data(table, id):
    r = requests.get(RUN_URL + f"{table}/{id}")
    return r.json()


def set_data(table, id, data):
    return requests.patch(RUN_URL + f"{table}/{id}", json=data)


# These are specific to Streamlit Snippets
CONTENTS_KEY = "contents"
PLACEHOLDER_CODE = """import streamlit as st

st.write('hello')
"""


def get_snippet(id):
    try:
        return get_data("snippets", id)["fields"][CONTENTS_KEY]["stringValue"]
    except:
        return PLACEHOLDER_CODE


def set_snippet(id, snippet):
    data = {"fields": {CONTENTS_KEY: {"stringValue": snippet}}}
    return set_data("snippets", id, data)


init_code = PLACEHOLDER_CODE
init_params = st.experimental_get_query_params()
if "snippet_id" in init_params:
    init_code = get_snippet(init_params["snippet_id"])

code = execbox_side(init_code, autorun=True, line_numbers=True, height=600)

save_button = st.button("Share your work 🎈")
if save_button:
    id = str(hash(code))
    set_snippet(id, code)
    # Query params breaks for /?id=blah; maybe reserved for Static Embedded Apps?
    # Anyways, use "snippet_id" for now
    st.experimental_set_query_params(snippet_id=id)
    # TODO: Is there a good way of getting the full URL from Streamlit?
    st.write(f"Saved to http://share.streamlit.io/FAKE/STUFF/?snippet_id={id}")
    st.balloons()

# Next TODO: List all snippets and allow people to click on them