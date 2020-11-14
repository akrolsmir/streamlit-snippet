import streamlit as st

from execbox_side import execbox_side, _new_sandbox
from utils import hash_to_id, get_snippet, set_snippet, load_placeholder

# Wait, feof makes :scissors: not work (?!)
scissors_icon = "https://twemoji.maxcdn.com/2/72x72/2702.png"
st.set_page_config(
    layout="wide", page_title="Streamlit Snippets", page_icon=scissors_icon
)

left_pane, right_pane = st.beta_columns(2)

with right_pane:
    st.subheader("Code editor")

    # Side by side execbox:
    execbox_container = st.beta_container()

    # Share button:
    share_button = st.button("Share your work 🎈")

# Download code by id (if the share button was not just clicked)
init_code = load_placeholder()
init_params = st.experimental_get_query_params()
if "snippet_id" in init_params and not share_button:
    # Note: experimental_get_query_params always returns a dict of *lists*
    id = init_params["snippet_id"][0]
    init_code = get_snippet(id)

with execbox_container:
    code = execbox_side(init_code, autorun=True, line_numbers=True, height=600)

with left_pane:
    try:
        # TODO: Allow people to set their own local_scope (so two execboxes call share scopes!). For
        # this we'll likely need to use session state, though.
        local_scope = _new_sandbox()
        # TODO: Add a new container and a `with` block here!
        exec(code, local_scope)
    except Exception as e:
        st.exception(e)


if share_button:
    id = hash_to_id(code)
    set_snippet(id, code)
    # Query params breaks for /?id=blah; maybe reserved for Static Embedded Apps?
    # Anyways, use "snippet_id" for now
    st.experimental_set_query_params(snippet_id=id)
    st.write(
        f"Saved to http://share.streamlit.io/akrolsmir/streamlit-snippet/main?snippet_id={id}"
    )
    st.balloons()
