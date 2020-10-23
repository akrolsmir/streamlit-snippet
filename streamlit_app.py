import streamlit as st
import requests

from execbox_side import execbox_side

# TODO: the zero width joiner feof thing is really annoying here
scissors_emoji = "https://twemoji.maxcdn.com/2/72x72/2702.png"
st.beta_set_page_config(
    layout="wide", page_title="Streamlit Snippets", page_icon=scissors_emoji
)

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
import numpy as np
import pandas as pd

st.write("Hello there. Check this out!")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
st.line_chart(chart_data)
"""


def get_snippet(id):
    try:
        return get_data("snippets", id)["fields"][CONTENTS_KEY]["stringValue"]
    except Exception as e:
        st.exception(e)
        return PLACEHOLDER_CODE


def set_snippet(id, snippet):
    data = {"fields": {CONTENTS_KEY: {"stringValue": snippet}}}
    return set_data("snippets", id, data)


# Download the code, if any
init_code = PLACEHOLDER_CODE
init_params = st.experimental_get_query_params()
if "snippet_id" in init_params:
    # Note: experimental_get_query_params always returns a dict of *lists*
    id = init_params["snippet_id"][0]
    init_code = get_snippet(id)


# Side by side st_execbox:
code = execbox_side(init_code, autorun=True, line_numbers=True, height=600)

# Share button:
share_button = st.button("Share your work 🎈")
if share_button:
    # TODO: Use a more concise hash (alphanumeric chars? words?)
    id = str(hash(code))
    set_snippet(id, code)
    # Query params breaks for /?id=blah; maybe reserved for Static Embedded Apps?
    # Anyways, use "snippet_id" for now
    st.experimental_set_query_params(snippet_id=id)
    # TODO: Is there a good way of getting the full URL from Streamlit?
    st.write(
        f"Saved to http://share.streamlit.io/akrolsmir/streamlit-snippet/main?snippet_id={id}"
    )
    st.balloons()

# Next TODO: List all snippets and allow people to click on them