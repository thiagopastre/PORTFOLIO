import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Setup do upload do arquivo
file=st.sidebar.file_uploader(
    label='Selecione o arquivo business_EDITED.pkl',
    type=['pkl']
)

if file is not None:
    business = pd.read_pickle(file)

    # Criando um Dataframe contendo a quantidade TOTAL de negócios (abertos e fechados) agrupados por Estado
    df_total_business = business[['state','is_open']].groupby('state').sum()
    df_total_business['total'] = business[['state','is_open']].groupby('state').count()
    df_total_business = df_total_business.sort_values(by='total', ascending=False).reset_index()

    graphs = ['Distribuição do target (stars)',
            'Quantidade de negócios cadastrados por Estado (barplot)',
            'Quantidade de negócios cadastrados por Estado (map)',
            'Quantidade de negócios abertos x fechados por Estado',
            'Ranking das categorias com mais negócios cadastrados (TOP 10)',
            'Categorias com mais negócios cadastrados no Estado XXX (TOP 10)'
            ]

    option = st.selectbox("Qual gráfico gostaria de analisar?", graphs)

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

        st.write("Observa-se que 50% dos negócios cadastrados estão qualificados com no máximo 3.5 estrelas, \
                 sendo que a grande maioria deles está abaixo de 3 estrelas.")
        st.write("Temos penas 25% dos negócios atingindo a pontuação máxima.")
    
    elif option == 'Quantidade de negócios cadastrados por Estado (barplot)':

        fig, ax = plt.subplots(figsize=[15,6])

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
    
    elif option == 'Quantidade de negócios cadastrados por Estado (map)':

        fig = px.choropleth(df_total_business,
                        locations='state', 
                        locationmode="USA-states", 
                        scope="usa",
                        color='total',
                        color_continuous_scale="turbo"
                        )

        fig.update_layout(title_text = 'Quantidade de negócios cadastrados por Estado',
                          title_font_size = 22,
                          )

        st.plotly_chart(fig)
    
    elif option == 'Quantidade de negócios abertos x fechados por Estado':

        fig, ax = plt.subplots(figsize=[12,5])

        plt.bar(x=df_total_business['state'], height=df_total_business['is_open'])
        plt.bar(x=df_total_business['state'], height=(df_total_business['total'] - df_total_business['is_open']))

        ax.set(xlabel='Estados',
            ylabel='Quantidade',
            title='Quantidade de negócios abertos x fechados por Estado'
            )
            
        plt.legend(['Open','Closed'])
        st.pyplot(fig)
    
    elif option == 'Ranking das categorias com mais negócios cadastrados (TOP 10)':

        # Criando um Dataframe contendo as categorias e a quantidade de negócios presentes em cada uma delas
        cat_dict = {}
        for feature in business:
            if 'category' in feature:
                new_feature = feature.replace('category_','')
                cat_dict[new_feature] = business[feature].value_counts()[1]

        df = pd.DataFrame.from_dict(cat_dict, orient='index').reset_index()
        df = df.rename({'index':'categories', 0:'qty'}, axis=1)
        df = df.sort_values(by='qty', ascending=False).reset_index(drop=True).head(10)

        fig = px.bar(df, y='qty', x='categories', text_auto='.2s',
             labels={
                     "categories": "Categorias",
                     "qty": "Quantidade"
                     }
            )

        fig.update_layout(title_text = 'Ranking das categorias com mais negócios cadastrados (TOP 10)',
                        title_font_size = 22,
                        )
        st.plotly_chart(fig)
    
    elif option == 'Categorias com mais negócios cadastrados no Estado XXX (TOP 10)':

        state_option = st.selectbox("Selecione o Estado desejado", business['state'].unique())

        # Criando um Dataframe contendo as categorias e a quantidade de negócios presentes em cada uma delas para um Estado ESPECÍFICO
        cat_dict2 = {}
        business2 = business[business['state']==state_option]

        for feature in business2:
            if 'category' in feature:
                new_feature = feature.replace('category_','')
                cat_dict2[new_feature] = business2[feature].sum()

        df2 = pd.DataFrame.from_dict(cat_dict2, orient='index').reset_index()
        df2 = df2.rename({'index':'categories', 0:'qty'}, axis=1)
        df2 = df2.sort_values(by='qty', ascending=False).reset_index(drop=True).head(10)


        # Plotando o gráfico das categorias com mais negócios cadastrados no Estado selecionado

        fig = px.bar(df2, y='qty', x='categories', text_auto='.2s',
                    labels={
                            "categories": "Categorias",
                            "qty": "Quantidade"
                            }
                    )

        fig.update_layout(title_text = "Categorias com mais negócios cadastrados no estado 'PA' (TOP 10)",
                        title_font_size = 22,
                        title_x=0.5, 
                        )
        st.plotly_chart(fig)
