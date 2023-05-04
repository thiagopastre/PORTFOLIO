import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Function to automatically upload the file 'business_EDITED.pkl
@st.cache_data
def load_data(url):
    df = pd.read_pickle(url)
    return df

business = load_data("https://github.com/thiagopastre/PORTFOLIO/raw/main/YELP_project/INPUT/business_EDITED.pkl")

st.title('EDA Yelp Project')

graphs = ['1. Target distribution (stars)',
        '2. Number of registered businesses per state (all states)',
        '3. Number of registered businesses per state (US only)',
        '4. Number of open x closed businesses per state',
        '5. Ranking of categories with most registered businesses',
        '6. Categories with most registered businesses in the selected state'
        ]

option = st.selectbox("Which chart would you like to analyze?", graphs)

# Creating a Dataframe containing the TOTAL amount of business (open and closed) grouped by State
df_total_business = business[['state','is_open']].groupby('state').sum()
df_total_business['total'] = business[['state','is_open']].groupby('state').count()
df_total_business = df_total_business.sort_values(by='total', ascending=False).reset_index()


if '1' in option:
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
    fig.suptitle('Distribution of the feature "stars"')
    ax[1].set_xlabel('Stars')
    ax[1].set_ylabel('Number of reviews')
    st.pyplot(fig)

    st.write("We see that 50% of the registered businesses are rated with a maximum of 3.5 stars, \
              with the vast majority of them below 3 stars.")
    st.write("We have only 25% of the businesses achieving the maximum score.")


elif '2' in option:
    fig, ax = plt.subplots(figsize=[15,6])
    ax = sns.barplot(x=df_total_business['state'],
                    y=df_total_business['total'],
                    palette='PuBu_r',
                    order=df_total_business['state']
                    )
    for i in ax.containers:
        ax.bar_label(i,)
    ax.set(xlabel='States',
        ylabel='Quantity',
        title='Number of registered businesses per state'
        )
    st.pyplot(fig)


elif '3' in option:
    fig = px.choropleth(df_total_business,
                    locations='state', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='total',
                    color_continuous_scale="turbo"
                    )
    fig.update_layout(title_text = 'Number of registered businesses per state (US)',
                        title_font_size = 22,
                        )

    st.plotly_chart(fig)


elif '4' in option:
    fig, ax = plt.subplots(figsize=[12,5])
    plt.bar(x=df_total_business['state'], height=df_total_business['is_open'])
    plt.bar(x=df_total_business['state'], height=(df_total_business['total'] - df_total_business['is_open']))
    ax.set(xlabel='States',
        ylabel='Quantity',
        title='Number of open x closed businesses per State'
        )
    plt.legend(['Open','Closed'])
    st.pyplot(fig)


elif '5' in option:
    # Creating a Dataframe containing the categories and the number of businesses present in each category (All States)
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
                    "categories": "Categories",
                    "qty": "Quantity"
                    }
        )
    fig.update_layout(title_text = 'Ranking of the categories with the most registered businesses (TOP 10)',
                    title_font_size = 22,
                    )
    st.plotly_chart(fig)


elif '6' in option:
    state_option = st.selectbox("Select the State you want", business['state'].unique())

    # Creating a Dataframe containing the categories and the amount of business present in each of them for a SPECIFIC STATE
    cat_dict2 = {}
    business2 = business[business['state'] == state_option]
    for feature in business2:
        if 'category' in feature:
            new_feature = feature.replace('category_','')
            cat_dict2[new_feature] = business2[feature].sum()

    df2 = pd.DataFrame.from_dict(cat_dict2, orient='index').reset_index()
    df2 = df2.rename({'index':'categories', 0:'qty'}, axis=1)
    df2 = df2.sort_values(by='qty', ascending=False).reset_index(drop=True).head(10)

    fig = px.bar(df2, y='qty', x='categories', text_auto='.2s',
                labels={
                        "categories": "Categories",
                        "qty": "Quantity"
                        }
                )
    fig.update_layout(title_text = f"Categories with most registered businesses in the state {state_option} (TOP 10)",
                    title_font_size = 22,
                    )
    st.plotly_chart(fig)
