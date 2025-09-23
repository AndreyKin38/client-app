import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import streamlit as st


def font_size(size: int, label: str):
    s = f"<p style='font-size: {size}px;'>{label}</p>"
    st.markdown(s, unsafe_allow_html=True)


def info(df1, df2, df3, df4):
    font_size(32, 'Info')
    st.write(df1, df2, df3, df4)


def df_statistic(df, header: str):

    font_size(32, header)
    st.write(df.head())

    st.write(f"##### shape: {df.shape}")

    st.write(f"##### duplicates: {df.duplicated().sum()}")

    font_size(28, 'is_null features:')
    col_is_na = df.isnull().sum()[df.isnull().sum() > 0]

    if len(col_is_na) != 0:
        for index, col in zip(col_is_na.index, col_is_na):
            st.write(f"{index}: {col}")
    else:
        st.write(f"##### 0")


def get_num_features1(df):
    df = df.copy()
    df = df.drop(['ID_CLIENT', 'TARGET'], axis=1)
    num_cols = df.columns[df.dtypes != 'object']
    num_cols = df[num_cols].columns[df[num_cols].std() > 1]

    return num_cols


def get_cat_features(df):
    cat_cols = df.columns[df.dtypes == 'object']

    return np.array(cat_cols)


def get_num_features2(df):
    num_cols = df.columns[df.dtypes != 'object']
    not_binary_cols = list(get_num_features1(df)) + ['ID_CLIENT', 'TARGET']
    cols = list(set(num_cols) - set(not_binary_cols))

    return cols


def correlation(df, header: str):
    font_size(32, header)

    features = list(get_num_features1(df)) + ['TARGET']

    fig = plt.figure(figsize=(8, 5))
    sns.heatmap(df[features].corr(), annot=True)
    st.pyplot(fig)


def hists(df, header: str):
    font_size(32, header)
    features = np.array(get_num_features1(df)).reshape(2, 3)

    n_row, n_col = features.shape
    fig, ax = plt.subplots(n_row, n_col, figsize=(10, 6))

    for i in range(2):
        for j in range(3):
            ax[i, j].hist(df[features[i, j]], bins=30)
            ax[i, j].set_title(features[i, j])

    plt.subplots_adjust(hspace=0.5)
    st.pyplot(fig)


def boxplot(df, header: str):
    font_size(32, header)
    features = np.array(get_num_features1(df)).reshape(2, 3)

    n_row, n_col = features.shape
    fig, ax = plt.subplots(n_row, n_col, figsize=(10, 6))

    for i in range(2):
        for j in range(3):
            ax[i, j].boxplot(df[features[i, j]])
            ax[i, j].set_title(features[i, j])

    plt.subplots_adjust(hspace=0.5)
    st.pyplot(fig)


def bars(df, header: str):
    font_size(32, header)
    features = np.array(get_num_features2(df)).reshape(3, 3)

    n_row, n_col = features.shape
    fig, ax = plt.subplots(n_row, n_col, figsize=(10, 6))

    for i in range(3):
        for j in range(3):
            ax[i, j].bar(df[features[i, j]].unique(), df[features[i, j]].value_counts())
            ax[i, j].set_title(features[i, j])

    plt.subplots_adjust(hspace=0.5)
    st.pyplot(fig)


def target_dependency(df, col: str):
    fig, ax = plt.subplots(figsize=(6, 3))

    colors = {'red': 0, 'green': 1}

    for k, v in colors.items():
        data = df.loc[df['TARGET'] == v, col]
        ax.hist(data, bins=30, color=k, alpha=0.7)
        ax.set_title(f'TARGET ON {col}')

    st.pyplot(fig)


"""Графики зависимостей целевой переменной и признаков"""


def target(df, header: str):
    font_size(32, header)

    """TARGET VALUE COUNTS"""
    stats1 = df.groupby(['TARGET'], as_index=False).agg({'ID_CLIENT': 'count'})

    """TARGET PIE"""
    fig = plt.figure(figsize=(8, 5))

    plt.pie(stats1['ID_CLIENT'], stats1['TARGET'], autopct='%1.0f%%')
    plt.legend(stats1['TARGET'])

    """TARGET STATISTICS"""
    stats2 = df.groupby(['TARGET']).agg({
        'AGE': 'mean',
        'PERSONAL_INCOME': 'mean',
        'WORK_TIME': 'mean',
        'CREDIT': 'mean',
        'FST_PAYMENT': 'mean'})

    st.write(df['TARGET'].value_counts())
    st.write('Labels percent')
    st.pyplot(fig)
    st.write('Labels statistics(mean)')
    st.write(stats2)

    cols = stats2.columns.tolist()
    for col in cols:
        target_dependency(df, col)


def predict(df, model, header: str):
    font_size(32, header)

    id_selected = st.selectbox('Client id', df['ID_CLIENT'])
    row = df.loc[df['ID_CLIENT'] == id_selected, :].drop('ID_CLIENT', axis=1)
    st.write('Not null columns')
    row_2 = row[row > 0].dropna(axis=1)
    st.write(row_2)

    with st.form('input'):

        button = st.form_submit_button()

    if button:

        prediction = model.predict(row)[0]

        text = f"Prediction {prediction}"
        st.write(text)


