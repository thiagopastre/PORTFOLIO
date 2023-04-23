import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.title('EDA Yelp Project')

# Personalizando o SideBar
# st.sidebar.title('Menu')

#Setup do upload do arquivo
file=st.sidebar.file_uploader(
    label='Selecione o arquivo business_EDITED.pkl',
    type=['pkl']
)

if file is not None:
    business = pd.read_pickle(file)

    graphs = ['Distribuição do target (stars)',
            'Quantidade de negócios cadastrados por Estado (barplot)',
            'Quantidade de negócios cadastrados por Estado (map)'
            ]

    option = st.selectbox(
            "Qual gráfico gostaria de analisar?",
            graphs
            )

    
    if option == 'Distribuição do target (stars)':
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
    
    elif option == 'Quantidade de negócios cadastrados por Estado (barplot)':

        # Criando um Dataframe contendo a quantidade TOTAL de negócios (abertos e fechados) agrupados por Estado
        df_total_business = business[['state','is_open']].groupby('state').sum()
        df_total_business['total'] = business[['state','is_open']].groupby('state').count()
        df_total_business = df_total_business.sort_values(by='total', ascending=False).reset_index()

        fig, ax = plt.subplots(figsize=[15,5])

        ax = sns.barplot(x=df_total_business['state'],
                        y=df_total_business['total'],
                        palette='PuBu_r',
                        order=df_total_business['state']
                        )
        for i in ax.containers:
            ax.bar_label(i,)

        ax.set(xlabel='Estados',
            ylabel='Quantidade',
            title='Quantidade de negócios cadastrados por Estado'
            )
        st.pyplot(fig)
