# -*- coding: utf-8 -*-

import streamlit as st
import tdnet_tool


def main():
    st.title('tdnet PDFs Downloader')
    st.markdown("適時開示情報閲覧サービス https://www.release.tdnet.info/inbs/I_main_00.html",
                unsafe_allow_html=True)
    sel_code = st.text_input(label='keyword')
    if len(sel_code) == 0:
        return

    td = tdnet_tool.tdNet()
    td.getData_tdnet_KeywordSearch(sel_code)

    df_ = td.df
    if len(td.df) == 0:
        return

    df_['time'] = df_['time'].str[:5]
    dict_style = [
        dict(selector=".col3", props=[('min-width', '80px')]),
        dict(selector=".col4", props=[('min-width', '180px')])]
    st.table(df_[['date', 'time', 'code', 'name', 'title', 'pdf']
                 ].style.set_table_styles(dict_style))

    return td


def download(td):
    answer = st.button('Create Files Link (TOP 10 files)')
    if answer == True:
        # PDFダウンロード
        td.df = td.df.drop_duplicates()
        td.downloadPDF(limit=10)
        file_name = 'tdnet.zip'
        link = b64_file_to_href(file_name)
        st.markdown(link, unsafe_allow_html=True)


def b64_file_to_href(file, mode='f'):
    import base64
    if mode == 'f':  # translate from file
        with open(file, "rb") as f:
            bytes_ = f.read()
    elif mode == 'b':  # direct bytes
        bytes_ = file
        file = 'file'
    b64 = base64.b64encode(bytes_).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download={file}>download</a>'
    return href


with st.spinner('Loading...'):
    td_ = main()

with st.spinner('Creating file...'):
    download(td_)
