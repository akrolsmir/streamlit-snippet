import requests
import hashlib
import base64

# TODO: get rid of this import
import streamlit as st


FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/plain-twig/databases/(default)/documents/"

# These could be generalized to other apps using Firestore
def get_data(table, id):
    r = requests.get(FIRESTORE_URL + f"{table}/{id}")
    return r.json()


def set_data(table, id, data):
    return requests.patch(FIRESTORE_URL + f"{table}/{id}", json=data)


def hash_to_id(input_string):
    # From https://stackoverflow.com/a/2510733/1222351
    hasher = hashlib.sha1(input_string.encode())
    return base64.urlsafe_b64encode(hasher.digest()).decode()[:8]


def load_placeholder():
    with open("placeholder.py", encoding="utf-8") as file:
        return file.read()


# These are specific to Streamlit Snippets
CONTENTS_KEY = "contents"


@st.cache
def get_snippet(id):
    try:
        return get_data("snippets", id)["fields"][CONTENTS_KEY]["stringValue"]
    except Exception as e:
        st.exception(e)
        return load_placeholder()


def set_snippet(id, snippet):
    data = {"fields": {CONTENTS_KEY: {"stringValue": snippet}}}
    return set_data("snippets", id, data)
