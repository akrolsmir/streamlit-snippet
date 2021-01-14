import streamlit as st
import base64

def download_link(object_to_download, download_filename, download_link_text):
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def to_lines_multi(files):
    lines = []
    for file in files:
        lines.extend(to_lines(file))
    return lines

def to_lines(file):
    if not file:
        return []
    return file.read().decode('utf-8').split('\n')

larger = st.file_uploader('CSVs with more (can upload multiple)', accept_multiple_files=True)
larger_lines = to_lines_multi(larger)
st.write(f"Larger file has {len(larger_lines)} lines total")


smaller = st.file_uploader('CSVs with less', accept_multiple_files=True)
smaller_lines = set(to_lines_multi(smaller))
st.write(f"Smaller file has {len(smaller_lines)} lines")


diff = [line for line in larger_lines if line not in smaller_lines]
st.write(f"Difference has {len(diff)} lines")
st.write(diff)

link = download_link('\n'.join(diff), 'difference.csv', 'Download difference.csv')
st.write(link, unsafe_allow_html=True)
