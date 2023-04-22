import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.title('EDA Yelp Project')

# Personalizando o SideBar
st.sidebar.title('Menu')

#Setup do upload do arquivo
arquivo=st.sidebar.file_uploader(
    label='Selecione o arquivo CSV',
    type=['csv']
)

if arquivo is not None:
    business = pd.read_csv(arquivo).drop('Unnamed: 0', axis=1)
    print(business.head(3))