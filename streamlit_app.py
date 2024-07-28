import streamlit as st
import pandas as pd
import math
from pathlib import Path
import plotly.express as px
# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='BetterBasket',
    page_icon=':basket:', # This is an emoji shortcode. Could be a URL too.
)



# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/matching_products.csv'
    df = pd.read_csv(DATA_FILENAME)

    

    return df

df = get_gdp_data()

def get_gdp_data4wk():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/matching_products4wk.csv'
    df = pd.read_csv(DATA_FILENAME)

    

    return df

df4wk = get_gdp_data4wk()


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :basket: BetterBasket and Econo

'''

# Add some spacing
''
''
tab1, tab2, tab3 = st.tabs(["Scatter Plot: Week over Week","Scatter Plot: Month over Month", "Recommendations"])

with tab1:
    # Title
    st.title("Quantity Impact of Price Changes")
    df['Start Date'] = pd.to_datetime(df['Start Date'])

    # Date selection toggle
    all_dates = st.checkbox('Show all dates', value=True, key='all_dates_tab1')

    if all_dates:
        filtered_df = df
    else:
        # Let the user select specific dates
        selected_dates = st.multiselect(
            'Select dates to show',
            options=df['Start Date'].dt.strftime('%Y-%m-%d').unique(),
            default=df['Start Date'].dt.strftime('%Y-%m-%d').unique(), 
            key='all_dates_tab1'
        )
        
        # Filter the data based on selected dates
        filtered_df = df[df['Start Date'].dt.strftime('%Y-%m-%d').isin(selected_dates)]

    # Scatter plot using Plotly
    fig = px.scatter(
        filtered_df, 
        x='Price Change %', 
        y='Quantity Change %', 
        title='Scatter Plot of Quantity Change % vs Percentage Change',
        labels={'Percentage Change': 'Percentage Change', 'Quantity Change %': 'Quantity Change %'},
        color='Category',
        size='Quantity',
        size_max=20,
        hover_data=['Product Name', 'SKU', 'Start Date']
    )



    # Display the plot
    st.plotly_chart(fig)

    # Display the filtered data
    #selected_columns = ['Start Date', 'Product Name', 'Category', 'Price Change %', 'Quantity Change %']
    #filtered_selected_df = filtered_df[selected_columns]
    st.write(filtered_df[['Start Date', 'Product Name', 'Category', 'Price Change %', 'Quantity Change %']])
with tab2:

       # Title
    st.title("Quantity Impact of Price Changes")
    df4wk['Start Date'] = pd.to_datetime(df4wk['Start Date'])

    # Date selection toggle
    all_dates = st.checkbox('Show all dates', value=True, key='all_dates_tab2')

    if all_dates:
        filtered_df4wk = df4wk
    else:
        # Let the user select specific dates
        selected_dates4wk = st.multiselect(
            'Select dates to show',
            options=df4wk['Start Date'].dt.strftime('%Y-%m-%d').unique(),
            default=df4wk['Start Date'].dt.strftime('%Y-%m-%d').unique(),
            key='all_dates_tab2'

        )
        
        # Filter the data based on selected dates
        filtered_df4wk = df4wk[df4wk['Start Date'].dt.strftime('%Y-%m-%d').isin(selected_dates4wk)]

    # Scatter plot using Plotly
    fig = px.scatter(
        filtered_df4wk, 
        x='Price Change %', 
        y='4 Week Avg % Change', 
        title='Scatter Plot of Quantity Change % vs Percentage Change',
        labels={'Percentage Change': 'Percentage Change', '4 Week Avg % Change': '4 Week Avg % Change'},
        color='Category',
        size='Quantity',
        size_max=20,
        hover_data=['Product Name', 'SKU', 'Start Date']
    )



    # Display the plot
    st.plotly_chart(fig)

    # Display the filtered data
    #selected_columns = ['Start Date', 'Product Name', 'Category', 'Price Change %', 'Quantity Change %']
    #filtered_selected_df = filtered_df[selected_columns]
    st.write(filtered_df4wk[['Start Date', 'Product Name', 'Category', 'Price Change %', '4 Week Avg % Change']])


with tab3:
    # Display filter options in the main section
    st.title("Recommendations")
    threshold = st.number_input("Enter the minimum ratio of Quantity Change % to Price Change %:", min_value=0.0, step=0.1)


    # Calculate the ratio and filter the DataFrame
    df['ratio'] = df['Quantity Change %'] / df['Price Change %']
    filtered_df2 = df[df['ratio'] > threshold]

    # Display the filtered data
    st.write(filtered_df2[['Start Date', 'Product Name', 'Category', 'Price Change %', 'Quantity Change %']])

