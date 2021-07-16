import pandas as pd


# merge the characteristics of an information
def merge_characteristics(df):
    dict_extract = {'infors': [], 'characterictics': []}
    infors_pros_unique = df.iloc[:, 0].unique()
    for i in range(len(infors_pros_unique)):
        list_infors = []
        list_characterictics = []
        for j in range(len(df.iloc[:, 0])):
            if df.iloc[:, 0][j] == infors_pros_unique[i]:
                list_infors.append(infors_pros_unique[i])
                list_characterictics.append(df.iloc[:, 1][j])
        list_infors_unique = list(set(list_infors))
        dict_extract['infors'].append(list_infors_unique)
        dict_extract['characterictics'].append(list_characterictics)
    df_extract = pd.DataFrame(dict_extract)
    df_extract['infors'] = ['; '.join(map(str, l)) for l in df_extract['infors']]
    df_extract['characterictics'] = ['; '.join(map(str, l)) for l in df_extract['characterictics']]
    return df_extract
