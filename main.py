from underthesea import word_tokenize
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
from rule_by_dependency_parses_tree import rule1, rule2
from merge_characterictics import merge_characteristics
from read_file_st_ac_sy import read_file_synonyms, read_file_stopwords, read_file_acronyms


@st.cache(suppress_st_warning=True)
def read_url(url_, n):
    # getting the URL has html tag contain reviews and ratings of product
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.eventscribe.com',
        'Referer': 'https://www.eventscribe.com/2018/ADEA/speakers.asp?h=Browse%20By%20Speaker',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 '
                      'Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    page = 1
    cmt_texts_1 = []
    ratings_1 = []
    while True:
        link = url_.split('?')[0]
        url1 = link + '/danh-gia?p=' + str(page)
        req = requests.get(url1, timeout=5, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        cmt_texts = []
        ratings = []
        for div_tag in soup.find_all('div', class_='comment__item par'):
            for div in div_tag.find_all('div', class_='comment-content'):
                for p in div.find_all("p", class_="cmt-txt"):
                    cmt_texts.append(p.text)
        for div_tag in soup.find_all('div', class_='comment__item par'):
            for div in div_tag.find_all('div', class_='comment-star'):
                i = 0
                for p in div.find_all('i', class_="icon-star"):
                    i += 1
                ratings.append(i)
        if not cmt_texts:
            break
        cmt_texts_1.append(cmt_texts)
        ratings_1.append(ratings)
        page += 1
    cmt_texts_list = []
    for sublist in cmt_texts_1:
        for item in sublist:
            cmt_texts_list.append(item)
    ratings_list = []
    for sublist in ratings_1:
        for item in sublist:
            ratings_list.append(item)

    rv = pd.DataFrame(cmt_texts_list, columns=['reviews'])
    rt = pd.DataFrame(ratings_list, columns=['ratings'])  # concat review and rating of product
    data = pd.concat([rv, rt], axis=1)

    # remove rating = 4
    data.drop(data.loc[data['ratings'] == 4].index, inplace=True)

    # convert rating=5 to class 0, rating=1,2 class 1
    data["ratings"] = data["ratings"].map({5: "positive", 1: "negative", 2: "negative", 3: "negative"})
    # Statistics of product ratings
    statistical = (data["ratings"].value_counts(sort=False, ascending=False)).to_list()
    label = ['positive', 'negative']
    st.title("Statistics of number ratings of type")
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax2.pie(statistical, labels=label, autopct='%1.2f%%')
    ax1.bar(label, statistical, color='blue')
    st.pyplot()

    # remove review empty
    data.drop(data.loc[data['reviews'] == ''].index, inplace=True)
    data.drop(data.loc[data['reviews'] == '\n'].index, inplace=True)

    # splitting data to 2 class
    reviews_good = data.loc[data['ratings'] == "positive"]
    reviews_bad = data.loc[data['ratings'] == "negative"]

    # clean data
    def standardize_data(row):
        row = re.sub(r'\d+', '', row)
        row = row.lower()
        row = row.strip()
        return row

    # Tokenizer
    def tokenizer(row):
        return word_tokenize(row, format="text").split()

    def processing_data(data_):
        # 1. Standardize data
        data_["reviews"] = data_["reviews"].apply(standardize_data)

        # 2. Tokenizer
        data_["reviews"] = data_["reviews"].apply(tokenizer)

        # 3. Embedding
        x_val = data_["reviews"]
        return x_val

    rv_good = processing_data(reviews_good)
    rv_bad = processing_data(reviews_bad)

    # remove stopwords
    def remove_stopwords(list_text):
        list_rs = []
        for elements in list_text:
            row_rs = []
            for element in elements:
                if element not in stopwords:
                    row_rs.append(element)
            list_rs.append(row_rs)
        return list_rs

    # replace acronyms
    def find_replace(text_tokenize):
        # is the item in the dict?
        for elements in text_tokenize:
            for index, element in enumerate(elements):
                # iterate by keys
                if element in da:
                    # look up and replace
                    elements[index] = da[element]
        # return updated string
        return text_tokenize

    positives = find_replace(rv_good)
    negatives = find_replace(rv_bad)
    positives = remove_stopwords(positives)
    negatives = remove_stopwords(negatives)

    positives = [' '.join(ele) for ele in positives]
    negatives = [' '.join(ele) for ele in negatives]

    # get top 5 word tfidf with highest tfidf
    def get_tfidf_for_words(text):
        tfidf = TfidfVectorizer(max_features=1500, ngram_range=(1, 1))
        tfidf_matrix = tfidf.fit_transform(text)
        df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names())
        return df.sum(axis=0).nlargest(n)

    positive_ = pd.DataFrame((get_tfidf_for_words(positives)).index)
    negative_ = pd.DataFrame((get_tfidf_for_words(negatives)).index)
    ne_po_reviews = pd.concat([positive_, negative_], axis=1)
    ne_po_reviews.columns = ['positive', 'negative']
    ne_po_reviews['positive'] = ne_po_reviews['positive'].str.replace('_', ' ')
    ne_po_reviews['negative'] = ne_po_reviews['negative'].str.replace('_', ' ')
    st.title("Top common words in positive and negative reviews")
    st.table(ne_po_reviews)

    df_review_good = pd.DataFrame(data["reviews"].loc[data['ratings'] == "positive"])
    df_review_bad = pd.DataFrame(data["reviews"].loc[data['ratings'] == "negative"])

    # cut into sentences
    def sentences(text):
        # split sentences and questions
        text = re.split('[.]', text)
        clean_sent = []
        for sent in text:
            clean_sent.append(sent)
        return clean_sent

    # sentences
    df_review_good['reviews_clean'] = df_review_good['reviews'].apply(sentences)
    df_review_bad['reviews_clean'] = df_review_bad['reviews'].apply(sentences)
    row_list_pos = []
    # for-loop to go over the df
    for i in range(len(df_review_good)):
        for sent in df_review_good['reviews_clean'].iloc[i]:
            row_list_pos.append(sent)  # Append to list
    row_list_neg = []
    for j in range(len(df_review_bad)):
        for sent in df_review_bad['reviews_clean'].iloc[j]:
            row_list_neg.append(sent)
    df_reviews_good = pd.DataFrame(row_list_pos)
    df_reviews_good.columns = ['reviews_clean']
    df_reviews_bad = pd.DataFrame(row_list_neg)
    df_reviews_bad.columns = ['reviews_clean']

    infors_list_pros = []
    for i in range(len(df_reviews_good)):
        sent = str(df_reviews_good["reviews_clean"].iloc[i])
        infor_extract = rule1(sent)
        infors_list_pros.append(infor_extract)
    df_rule1 = pd.DataFrame(infors_list_pros)
    infors_list_cons = []
    for i in range(len(df_reviews_bad)):
        sent = str(df_reviews_bad["reviews_clean"].iloc[i])
        infor_extract = rule2(sent)
        infors_list_cons.append(infor_extract)

    def standardize_row(row):
        row = row.lower()
        return row

    # replace synonyms
    def find_replace_synonyms(series):
        list_text = []
        for element in series:
            if element in ds:
                # look up and replace
                element = ds[element]
                list_text.append(element)
            else:
                list_text.append(element)
        # return updated string
        return list_text

    df_rule2 = pd.DataFrame(infors_list_cons)
    infors_good = (df_rule1["infors"]).tolist()
    characterictics_good = (df_rule1["characterictics"]).tolist()
    infors_good_list = pd.DataFrame([item for elem in infors_good for item in elem])
    characterictics_good_list = pd.DataFrame([item for elem in characterictics_good for item in elem])

    extract_reviews_good = pd.concat([infors_good_list, characterictics_good_list], axis=1)
    extract_reviews_good.columns = ['Infors_pros', 'Characterictics_pros']
    extract_reviews_good['Infors_pros'] = extract_reviews_good['Infors_pros'].apply(standardize_row)
    extract_reviews_good['Characterictics_pros'] = extract_reviews_good['Characterictics_pros'].apply(standardize_row)

    df1_infor = pd.Series(find_replace_synonyms(extract_reviews_good['Infors_pros']))
    df1_character = pd.Series(find_replace_synonyms(extract_reviews_good['Characterictics_pros']))
    extract_reviews_good['Infors_pros'] = df1_infor
    extract_reviews_good['Characterictics_pros'] = df1_character
    extract_reviews_good = extract_reviews_good.drop_duplicates()
    infors_bad = (df_rule2["infors"]).tolist()
    characterictics_bad = (df_rule2["characterictics"]).tolist()
    infors_bad_list = pd.DataFrame([item for elem in infors_bad for item in elem])
    characterictics_bad_list = pd.DataFrame([item for elem in characterictics_bad for item in elem])

    extract_reviews_bad = pd.concat([infors_bad_list, characterictics_bad_list], axis=1)
    extract_reviews_bad.columns = ['Infors_cons', 'Characterictics_cons']
    extract_reviews_bad['Infors_cons'] = extract_reviews_bad['Infors_cons'].apply(standardize_row)
    extract_reviews_bad['Characterictics_cons'] = extract_reviews_bad['Characterictics_cons'].apply(standardize_row)
    df2 = pd.Series(find_replace_synonyms(extract_reviews_bad['Infors_cons']))
    extract_reviews_bad['Infors_cons'] = df2
    extract_reviews_bad = extract_reviews_bad.drop_duplicates()
    appended_extract_pros = []

    def check_word_appear_pos(df_ne_pos):
        for row_pos in df_ne_pos['positive']:
            df = extract_reviews_good[extract_reviews_good['Characterictics_pros'].str.contains(row_pos)]
            appended_extract_pros.append(df)
        return (pd.concat(appended_extract_pros)).drop_duplicates().reset_index(drop=True)

    appended_extract_cons = []

    def check_word_appear_neg(df_ne_pos):
        for row_cons in df_ne_pos['negative']:
            df = extract_reviews_bad[extract_reviews_bad['Characterictics_cons'].str.contains(row_cons)]
            appended_extract_cons.append(df)
        return (pd.concat(appended_extract_cons)).drop_duplicates().reset_index(drop=True)

    extract_reviews_good = (check_word_appear_pos(ne_po_reviews)).drop_duplicates()
    extract_reviews_bad = (check_word_appear_neg(ne_po_reviews)).drop_duplicates()

    extract_reviews_good = extract_reviews_good.replace('_', ' ', regex=True)
    extract_reviews_bad = extract_reviews_bad.replace('_', ' ', regex=True)

    # merge the characteristics of an information
    extract_pros = merge_characteristics(extract_reviews_good)
    extract_cons = merge_characteristics(extract_reviews_bad)

    col1, col2 = st.beta_columns(2)
    with col1:
        st.title("Pros of product")
        st.table(extract_pros)
    with col2:
        st.title("Cons of product")
        st.table(extract_cons)


stopwords = read_file_stopwords()
ds = read_file_synonyms()
da = read_file_acronyms()
name = st.text_input("Enter your link of product", "Type Here ...")
n = st.slider('Enter top common words in positive and negative reviews', 1, 50)
st.set_option('deprecation.showPyplotGlobalUse', False)
if st.button('Submit'):
    result = st.write(read_url(name, n))
    st.success(result)
