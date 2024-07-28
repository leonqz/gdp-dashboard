import streamlit as st
import pandas as pd
#import math
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

def display_scatter_plot_and_data(df, title, date_key):
    # Title
    st.title(title)
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    default_date = '2024-03-28'
    # Ensure the default date is in the correct format
    default_date = pd.to_datetime(default_date).strftime('%Y-%m-%d')
    
    # Check if the default date exists in the data
    date_options = df['Start Date'].dt.strftime('%Y-%m-%d').unique()
    if default_date not in date_options:
        default_date = date_options[0]  # Fallback to the first date if default not available

    selected_date = st.selectbox(
        'Select a date to show',
        options=date_options,
        index=list(date_options).index(default_date),  # Set the default index
        key=date_key + '_selected_date'
    )
    
    filtered_df = df[df['Start Date'].dt.strftime('%Y-%m-%d') == selected_date]

    selected_products = st.multiselect(
        'Select products to show',
        options=filtered_df['Product Name'].unique(),
        default=filtered_df['Product Name'].unique(),
        key=date_key + '_selected_products'
    )

    # Further filter the data based on the selected products
    filtered_df = filtered_df[filtered_df['Product Name'].isin(selected_products)]

    # Scatter plot using Plotly
    fig = px.scatter(
        filtered_df, 
        x='Price Change %', 
        y='Quantity Change %', 
        title=f'Scatter Plot of {title}',
        labels={'Price Change %': 'Price Change %', 'Quantity Change %': 'Quantity Change %'},
        color='Category',
        size='Quantity',
        size_max=20,
        hover_data=['Product Name', 'SKU', 'Start Date']
    )

    # Display the plot
    st.plotly_chart(fig)

    # Display the filtered data
    st.write(filtered_df[['Start Date', 'Product Name', 'Category', 'Price Change %', 'Quantity Change %']])


tab1, tab2 = st.tabs(["Quantity Impact of Price Changes", "Month-Over-Month Data"])

with tab1:
    display_scatter_plot_and_data(df, "Quantity Impact of Price Changes", "tab1")

with tab2:
    display_scatter_plot_and_data(df4wk, "Month-Over-Month Data", "tab2")

'''
# :basket: BetterBasket and Econo

'''

# Add some spacing
''
''

tab1, tab2, tab3 = st.tabs(["Quantity Impact of Price Changes", "Month-Over-Month Data", "Recommendations"])

with tab1:
    display_scatter_plot_and_data(df, "Quantity Impact of Price Changes",  "selected_dates_tab1")

with tab2:
    display_scatter_plot_and_data(df4wk, "Month-Over-Month Data", "selected_dates_tab2")


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.

#tab1, tab2, tab3 = st.tabs(["Scatter Plot: Week over Week","Scatter Plot: Month over Month", "Recommendations"])


with tab3:
    # Display filter options in the main section
    st.title("Recommendations")
    threshold = st.number_input("Enter the minimum ratio of Quantity Change % to Price Change %:", min_value=0.0, step=0.1)


    # Calculate the ratio and filter the DataFrame
    df['ratio'] = df['Quantity Change %'] / df['Price Change %']
    filtered_df2 = df[df['ratio'] > threshold]

    # Display the filtered data
    st.write(filtered_df2[['Start Date', 'Product Name', 'Category', 'Price Change %', 'Quantity Change %']])

