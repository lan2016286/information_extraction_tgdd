import json
import streamlit as st


@st.cache(suppress_st_warning=True)
# read file stopwords
def read_file_stopwords():
    file_stopwords = open('/home/lan/PycharmProjects/information_extraction/stopwords.txt', encoding="utf8")
    sw = file_stopwords.read()
    sw = set(sw.splitlines())
    return sw


@st.cache(suppress_st_warning=True)
# loading file acronyms
def read_file_acronyms():
    with open('/home/lan/PycharmProjects/information_extraction/acronyms.json', encoding="utf8") as json_file:
        dict_acronyms = json.load(json_file)
    return dict_acronyms


@st.cache(suppress_st_warning=True)
def read_file_synonyms():
    with open('/home/lan/PycharmProjects/information_extraction/synonyms.json', encoding="utf8") as json_file:
        dict_synonyms = json.load(json_file)
    return dict_synonyms
