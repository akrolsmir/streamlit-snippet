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

# Download code by snippet_id
snippet_id = "iL_T1W23"
init_code = load_placeholder()
init_params = st.experimental_get_query_params()
if "snippet_id" in init_params:
    # Note: experimental_get_query_params always returns a dict of *lists*
    snippet_id = init_params["snippet_id"][0]
    init_code = get_snippet(snippet_id)

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
    snippet_id = hash_to_id(code)
    set_snippet(snippet_id, code)
    # Query params breaks for /?id=blah; maybe it's reserved for Static Embedded Apps?
    # Anyways, use "snippet_id" for now
    st.experimental_set_query_params(snippet_id=snippet_id)
    st.balloons()

# For now, always show the links, since otherwise they'd disappear on S4A
# But ideally we'd only show links after "Share" is clicked, to reduce confusion & complexity
EDIT_URL = f"http://share.streamlit.io/akrolsmir/streamlit-snippet/main?snippet_id={snippet_id}"
PREVIEW_URL = f"https://share.streamlit.io/akrolsmir/streamlit-snippet/main/preview.py?snippet_id={snippet_id}"
right_pane.write(f"Last saved as {EDIT_URL} ([preview]({PREVIEW_URL}))")
