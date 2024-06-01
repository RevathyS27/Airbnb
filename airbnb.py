import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("C:/Users/Revathy/Desktop/Youtube/.venv/Airbnb/Airbnb.csv")
print(df)

# Streamlit configuration
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

# Creating option menu in the sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Explore", "Overview"],
        icons=["house", "book"],
        menu_icon="cast",
        default_index=0,
    )

st.markdown('<h1 style="color:#441273;">AIRBNB ANALYSIS</h1>', unsafe_allow_html=True)

if selected == 'Explore':
    tab1, tab2, tab3 = st.tabs(["Geospatial Visualization", "Price Analysis and Visualization", "Availability Analysis"])

    with tab1:
        data = df
        country = st.sidebar.multiselect('Select a Country', sorted(data['Country'].unique()), sorted(data['Country'].unique()))
        prop = st.sidebar.multiselect('Select Property Type', sorted(data['Property Type'].unique()), sorted(data['Property Type'].unique()))
        room = st.sidebar.multiselect('Select Room Type', sorted(data['Room Type'].unique()), sorted(data['Room Type'].unique()))
        price = st.sidebar.slider('Select Price Range', min_value=float(data['Price'].min()), max_value=float(data['Price'].max()), value=(float(data['Price'].min()), float(data['Price'].max())))
        
        # Converting the user input into query
        query = f"`Country` in {country} & `Room Type` in {room} & `Property Type` in {prop} & `Price` >= {price[0]} & `Price` <= {price[1]}"

        # Total Listings by Country Choropleth Map
        country_df = df.query(query).groupby(['Country'], as_index=False)['Name'].count().rename(columns={'name': 'Name'})
        fig = px.choropleth(
            country_df,
            title='Total Listings in each Country',
            locations='Country',
            locationmode='country names',
            color='Name',
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig, use_container_width=True)


    with tab2:
        selected_location = st.sidebar.selectbox('Select Location', df['Street'].unique())
        selected_property_type = st.sidebar.selectbox('Select Property Type', df['Property Type'].unique())

        # Filter data based on user selections
        filtered_data = df[(df['Street'] == selected_location) & (df['Property Type'] == selected_property_type)]

        # Price analysis
        st.subheader('Price Analysis')

        # Average price by location and property type
        average_price = filtered_data.groupby(['Street', 'Property Type'])['Price'].mean().reset_index()
        st.write(average_price)

        #Price distribution
        st.subheader('Price Distribution')
        price_dist_fig, price_dist_ax = plt.subplots()
        sns.histplot(filtered_data['Price'], kde=True, ax=price_dist_ax)
        st.pyplot(price_dist_fig)

        #Price trend over time
        st.subheader('Price Trend Over Time')
        date_column = 'Availability'  
        price_trend_fig, price_trend_ax = plt.subplots()
        sns.lineplot(data=filtered_data, x=date_column, y='Price', ax=price_trend_ax)
        st.pyplot(price_trend_fig)


    with tab3:
        # Availability Analysis
        st.markdown("## Availability Analysis")

        # Availability by Room Type Pie Chart
        fig = px.pie(
            data_frame=df.query(query),
            values='Availability',
            names='Room Type',
            title='Availability by Room Type'
        )
        st.plotly_chart(fig, use_container_width=True)


if selected == "Overview":
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(10, 8))
        ax = sns.countplot(data=df, y=df['Property Type'], order=df['Property Type'].value_counts().index[:10])
        ax.set_title("Top 10 Property Types")
        st.pyplot(plt)

        # Find best host in the Listing name
        plt.figure(figsize=(10, 8))
        ax = sns.countplot(data=df, y=df['Host Name'], order=df['Host Name'].value_counts().index[:10])
        ax.set_title("Top 10 Hosts with Highest number of Listings")
        st.pyplot(plt)

    with col2:
        data = df
        country = st.sidebar.multiselect('Select a Country', sorted(data['Country'].unique()), sorted(data['Country'].unique()))
        prop = st.sidebar.multiselect('Select Property Type', sorted(data['Property Type'].unique()), sorted(data['Property Type'].unique()))
        room = st.sidebar.multiselect('Select Room Type', sorted(data['Room Type'].unique()), sorted(data['Room Type'].unique()))
        price = st.sidebar.slider('Select Price Range', min_value=float(data['Price'].min()), max_value=float(data['Price'].max()), value=(float(data['Price'].min()), float(data['Price'].max())))
        
        # Converting the user input into query
        query = f'`Room Type` in {room} & `Property Type` in {prop} & `Price` >= {price[0]} & `Price` <= {price[1]}'

        # Avg Price by Room Type Bar Chart
        pr_df = df.query(query).groupby('Room Type', as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(
            data_frame=pr_df,
            x='Room Type',
            y='Price',
            color='Price',
            title='Avg Price in each Room type'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Availability by Room Type Box Plot
        fig = px.box(
            data_frame=df.query(query),
            x='Room Type',
            y='Availability',
            color='Room Type',
            title='Availability by Room_type'
        )
        st.plotly_chart(fig, use_container_width=True)






