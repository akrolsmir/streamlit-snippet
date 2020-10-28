import streamlit as st
import pandas as pd
import requests
import hashlib
import base64

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


def list_data(table, page_size=25, order_by=""):
    r = requests.get(RUN_URL + f"{table}?pageSize={page_size}&orderBy={order_by}")
    return r.json()


def hash_to_id(input_string):
    # From https://stackoverflow.com/a/2510733/1222351
    hasher = hashlib.sha1(input_string.encode())
    return base64.urlsafe_b64encode(hasher.digest()).decode()[:8]


def id_to_url(id):
    return f"http://share.streamlit.io/akrolsmir/streamlit-snippet/main?snippet_id={id}"


# These are specific to Streamlit Snippets
CONTENTS_KEY = "contents"
SNIPPETS_KEY = "snippets"
TITLE_KEY = "title"
with open("placeholder.py") as file:
    PLACEHOLDER_CODE = file.read()


def get_snippet(id):
    try:
        json = get_data(SNIPPETS_KEY, id)
        return Snippet.from_json(json)
    except Exception as e:
        st.exception(e)
        return Snippet()


def set_snippet(id, snippet, title=""):
    if title:
        data = {
            "fields": {
                CONTENTS_KEY: {"stringValue": snippet},
                TITLE_KEY: {"stringValue": title},
            }
        }
    else:
        data = {
            "fields": {
                CONTENTS_KEY: {"stringValue": snippet},
            }
        }
    return set_data(SNIPPETS_KEY, id, data)


def list_snippets():
    json = list_data(SNIPPETS_KEY, page_size=0, order_by="title")
    array = [Snippet.from_json(j).pretty_print() for j in json["documents"]]


class Snippet:
    def __init__(self, contents=PLACEHOLDER_CODE, title=""):
        self.contents = contents
        self.title = title

    @staticmethod
    def from_json(json):
        contents = doc_get(json, CONTENTS_KEY)
        title = doc_get(json, TITLE_KEY)
        snippet = Snippet(contents, title)
        snippet.created = json["createTime"]
        snippet.updated = json["updateTime"]
        return snippet

    def to_dict(self):
        # Could be used as a dataframe
        return {
            "title": self.title,
            "id": self.id,
            "created": self.created,
            "url": id_to_url(self.id),
        }

    def pretty_print(self):
        text = self.title if self.title else self.id
        st.write(f"**[{text}]({id_to_url(self.id)})** - {self.updated}")

    @property
    def id(self):
        return hash_to_id(self.contents)


# Safely extracts a string key out of the document
def doc_get(json, field):
    try:
        return json["fields"][field]["stringValue"]
    except Exception:
        return ""


# TODO: Split out utils
# TODO: Debug the thing rerunning/reballoonsing.
# Maybe the button triggers execbox to refresh and pull in the placeholder code?
# Or maybe the share_button logic is just f***ed
# But why is it just for share, not for local?
# Hypothesis: experimental_set_query_params forces refresh on S4A

# TODO: Shareable link without code
# TODO: install devdependencies like bokeh

# Side by side execbox:
execbox_container = st.beta_container()

# Share button:
title_empty = st.empty()
share_button = st.button("Generate Snippet URL 🎈")

# Download code by id (if the share button was not just clicked)
init_params = st.experimental_get_query_params()
snippet = Snippet()
if "snippet_id" in init_params and not share_button:
    # Note: experimental_get_query_params always returns a dict of *lists*
    id = init_params["snippet_id"][0]
    snippet = get_snippet(id)


with execbox_container:
    code = execbox_side(snippet.contents, autorun=True, line_numbers=True, height=500)
title = title_empty.text_input(
    "(Optional) Name your snippet to make it public", snippet.title
)

# On 1) new code, 2) share, 3) edit -- the execbox resets.
# 3) overwrites 2)'s button state; TODO: Prevent this with state (or checkbox???)

# TODO: After loading a URL, the snippet naming thing doesn't work correctly.
if share_button:
    id = hash_to_id(code)
    set_snippet(id, code, title)
    # Query params breaks for /?id=blah; maybe reserved for Static Embedded Apps?
    # Anyways, use "snippet_id" for now
    st.experimental_set_query_params(snippet_id=id)
    # TODO: Is there a good way of getting the full URL from Streamlit?
    # TODO: Clean up URL via redirect? Add Notion-style title?
    # Want http;//snippet.streamlit.io/?s=Example-bar-chart-iI0cMzhy
    st.write(f"Saved to {id_to_url(id)}")
    st.balloons()

public_snippets = st.beta_expander("Public snippets")
with public_snippets:
    list_snippets()
# Next TODO: List all snippets and allow people to click on them