import streamlit as st
from streamlit_ace import st_ace

# Modified from https://github.com/tvst/st-execbox/blob/master/execbox/__init__.py


FONT_SIZE = 14
EXTRA_LINES = 3


def execbox_side(
    body="",
    button_label="Run",
    autorun=False,
    height=None,
    line_numbers=False,
    key=None,
):
    """Display a button widget.
    Parameters
    ----------
    body : str
        The initial code to show in the execbox.
    button_label : str
        The label to use for the "Run" button.
    autorun : bool
        Whether the code should execute with each keystroke.
    height : int or None
        The height of the execbox, in pixels. If None, calculates the height smartly to fill the
        content and a couple more lines.
    line_numbers : bool
        Whether to show line numbers.
    key : str or None
        An optional string to use as the unique key for the widget. If this is omitted, a key will
        be generated for the widget based on its content. Multiple widgets of the same type may not
        share the same key.
    Returns
    -------
    str
        The source code in the execbox.
    """

    body = body.strip()

    if height is None:
        nlines = body.count("\n")
        if nlines < 3:
            nlines = 3
        height = (FONT_SIZE + 2) * (nlines + 1 + EXTRA_LINES)

    kwargs = dict(
        value=body,
        language="python",
        theme="dawn",
        keybinding="vscode",
        font_size=FONT_SIZE,
        height=height,
        show_gutter=line_numbers,
        key=key,
    )
    # TODO: Find some way to enter small text so we can show a label above the editor, just like
    # Streamlit's normal components.
    # TODO: Make this collapsible.
    content = st_ace(**kwargs)

    # TODO: Change AceEditor (or use our own editor frontend) so we don't rerun the script on every
    # keystroke when autorun is False.
    if autorun:
        run = True
    else:
        autokey = hash((body, button_label, autorun, height, line_numbers, key))
        run = st.button(button_label, key=autokey)

    return content


def _new_sandbox():
    import types

    module = types.ModuleType("__main__")
    return module.__dict__
