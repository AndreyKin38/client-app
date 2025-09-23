import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from frontend.eda import info, df_statistic, correlation, predict
from frontend.eda import hists, boxplot, bars, target

import pickle


params = {'legend.fontsize': 'small',
          'figure.figsize': (12, 8),
          'axes.labelsize': 'small',
          'axes.titlesize': 'small',
          'xtick.labelsize': 'small',
          'ytick.labelsize': 'small'}

plt.rcParams.update(params)


df_clients = pd.read_csv('model/data/client_dataset.csv')
df_clients_clean = pd.read_csv('model/data/client_dataset_clean.csv')
df_target = pd.read_csv('model/data/clients/D_target.csv').drop('AGREEMENT_RK', axis=1)
df_clients_clean_2 = df_clients_clean.merge(df_target)

df_fl_pens = pd.read_csv('model/data/clients/D_pens.csv').drop('ID', axis=1)
df_fl_work = pd.read_csv('model/data/clients/D_work.csv').drop('ID', axis=1)
df_fl_gender = pd.DataFrame({'FLAG': [0, 1],
                            'GENDER': ['woman', 'man']}, index=[0, 1])
df_fl_presence = pd.DataFrame({'FLAG': [0, 1],
                               'IS_OWNER': ['tenant', 'owner']}, index=[0, 1])

df_clients_prep = pd.read_csv('model/data/client_dataset_prep.csv')

with open('pickle_model/model.pkl', 'rb') as file:
    model = pickle.load(file)


st.sidebar.title('Navigation')
# uploaded_file = st.sidebar.file_uploader("Upload your file here")

options = st.sidebar.radio("Pages", options=['Full_client_dataset',
                                             'Clean_client_dataset',
                                             'Target',
                                             'Statistics',
                                             'Correlation',
                                             'Prediction'])


try:
    if options == 'Full_client_dataset':
        st.title("Loan dataset")
        df_statistic(df_clients, 'Full dataset')

    elif options == 'Clean_client_dataset':

        df_statistic(df_clients_clean, 'Clean dataset')

    elif options == 'Target':

        target(df_clients_clean_2, "Target")

    elif options == 'Statistics':
        info(df_fl_pens, df_fl_work, df_fl_gender, df_fl_presence)
        bars(df_clients_clean_2, "Bar")
        hists(df_clients_clean_2, 'Histogram')
        boxplot(df_clients_clean_2, "Boxplot")

    elif options == 'Correlation':

        correlation(df_clients_clean_2, "Correlation")

    elif options == 'Prediction':

        predict(df_clients_prep, model, 'Logistic regression prediction')


except Exception as e:
    # st.text("There is no data uploaded!")
    raise e

