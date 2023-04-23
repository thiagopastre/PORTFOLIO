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

business = pd.read_pickle('https://github.com/thiagopastre/PORTFOLIO/blob/main/YELP_project/INPUT/business_EDITED.pkl')
st.write(business.head())