# About

Hey! Use Streamlit Snippets to try out simple scripts in your browser, save your
work, and share it with others!

# TODOs

- Generate a parameter or option to view without the execbox
- Clean up URL via redirect? Add Notion-style title?
  - Is there a good way of getting the full URL from Streamlit?
  - Want http://snippet.streamlit.io/?s=Example-bar-chart-iI0cMzhy
- List all snippets and allow people to click on them
- Start versioning this? (Eh, probably with the migration to streamlit GH org)

# Done

- Rework for first-user experience
- Play with adjustable-width columns:
  ```
  left_width = st.slider("Width", 0, 100, 50)
  left_pane, right_pane = st.beta_columns([left_width, 100 - left_width])
  ```
- Split out network/misc calls into utils.py
- Figure out why second click "share" click invariably fails
  1. Go to a nonstandard URL like http://localhost:8501/?snippet_id=W2GJPDf0
  2. Edit code
  3. Share your work
  - Expected: New link generated, code does not change
  - Saw: Always reloads to initial page
  - Solution: Always call get_snippet() if snippet_id is present,
    even if "Share" was just clicked. @st.cache to save network calls.
