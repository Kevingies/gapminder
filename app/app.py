import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns


st.title('Showing my own Version of the Gapminder Dashboard')
st.write("You can select which countries you want to display over the years the size of the bubbles is the population")

@st.cache_data
# Preprocess df_lex
def preprocess_data():
    df_lex = pd.read_csv('lex.csv')
    df_lex = df_lex.fillna(method='ffill')
    df_lex = df_lex.melt(id_vars='country', var_name='year', value_name='KPI')

    # Preprocess df_gnp_percap
    df_gnp_percap = pd.read_csv('ny_gnp_pcap_pp_cd.csv')
    df_gnp_percap = df_gnp_percap.fillna(method='ffill')
    df_gnp_percap = df_gnp_percap.melt(id_vars='country', var_name='year', value_name='KPI')

    # Preprocess df_gnp_percap
    df_pop= pd.read_csv('pop.csv')
    df_pop = df_pop.fillna(method='ffill')
    df_pop = df_pop.melt(id_vars='country', var_name='year', value_name='KPI')

    # merge dfs
    merged_df = pd.merge(pd.merge(df_lex, df_gnp_percap, on=['country', 'year']), df_pop, on=['country', 'year'])

    # rename columns
    merged_df.columns = ['country', 'year', 'lifeexpectancy', 'gnp','population']

    
    pattern = r'^(\d+\.?\d*)'

    # Convert the values to numeric
    merged_df["gnp"] = merged_df["gnp"].str.extract(pattern, expand=False).astype(float)
    merged_df["population"] = merged_df["population"].str.extract(pattern, expand=False).astype(float)
    merged_df["gnp"] = merged_df["gnp"]*1000
    #merged_df["population"] = merged_df["population"]*1000000

    merged_df['country_color_coded'] = [i+1 for i, _ in enumerate(merged_df['country'])]

 
    return merged_df

merged_df = preprocess_data()

year = st.slider('Which year do you want to select?', int(merged_df['year'].min()), int(merged_df['year'].max()), 2020)
st.write("I select", year)

options = st.multiselect(
    'What country do you want to select',
    merged_df['country'].unique())
#st.write('You selected:', options)

gni = merged_df[(merged_df["year"] == str(year)) & (merged_df["country"].isin(options))]


def plt_data(gni):
    
    x = gni["gnp"]
    y = gni["lifeexpectancy"]
    z = gni["population"]
    colors = gni['country_color_coded']

    max_loggnp = np.log(merged_df["gnp"].max())

    #colors = np.random.rand(len(gni['country']))

    fig, ax = plt.subplots()
    ax.scatter(np.log(x), y, s=z, c= colors)
    plt.xlim(0, max_loggnp)
    plt.xlabel('logged gnu per capita')
    plt.ylabel('life expectancy')

    return fig


st.pyplot(plt_data(gni))

#st.write(gni.head(5))
