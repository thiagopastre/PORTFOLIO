import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.title('EDA Yelp Project')

# Personalizando o SideBar
st.sidebar.title('Menu')

#Setup do upload do arquivo
file=st.sidebar.file_uploader(
    label='Selecione o arquivo PKL',
    type=['pkl']
)

if file is not None:
    business = pd.read_pickle(file)
    st.write(business.head())


    stars = business['stars'].agg('value_counts')

    fig, ax = plt.subplots(1,2, figsize=[12,4])

    sns.boxplot(ax=ax[0],
                data=business,
                x='stars',
                palette='PuBu'
            )

    sns.barplot(ax=ax[1],
                x=stars.index,
                y=stars,
                palette='PuBu'
            )

    fig.suptitle('Distribuição da feature "stars"')
    ax[1].set_xlabel('Stars')
    ax[1].set_ylabel('Quantidade de avaliações')
    st.pyplot(fig)