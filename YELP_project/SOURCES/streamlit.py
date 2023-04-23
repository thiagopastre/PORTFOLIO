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

business = pd.read_pickle(file)
st.write(file.head())