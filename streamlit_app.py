import streamlit as st
import pandas as pd
#import math


from pathlib import Path
import plotly.express as px
import plotly.graph_objs as go
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
    DATA_FILENAME = Path(__file__).parent/'data/matching_products5.csv'
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
    DATA_FILENAME = Path(__file__).parent/'data/matching_products5_4wk.csv'
    df = pd.read_csv(DATA_FILENAME)

    

    return df

df4wk = get_gdp_data4wk()

def display_scatter_plot_and_data(df, title, date_key):
    # Title
    st.title(title)
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    default_date = '2024-05-16'
    # Ensure the default date is in the correct format
    default_date = pd.to_datetime(default_date).strftime('%Y-%m-%d')
    
    # Check if the default date exists in the data
    date_options = df['Start Date'].dt.strftime('%Y-%m-%d').unique()
    default_date = date_options[-1]  # Assuming you want the latest date as default


    if default_date not in date_options:
        default_date = date_options[0]  # Fallback to the first date if default not available

    selected_date = st.selectbox(
        'Select a date to show',
        options=date_options,
        index=list(date_options).index(default_date),  # Set the default index
        key=date_key + '_selected_date'
    )

    previous_week_date = (pd.to_datetime(selected_date) - pd.Timedelta(weeks=1)).strftime('%Y-%m-%d')

    # Display week comparison text
    st.markdown(f"### Showing data for  week starting on {selected_date} compared to week starting on {previous_week_date}")

    filtered_df = df[df['Start Date'].dt.strftime('%Y-%m-%d') == selected_date]


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
  
    x_min = filtered_df['Price Change %'].min()
    x_max = filtered_df['Price Change %'].max()
    y_min = filtered_df['Quantity Change %'].min()
    y_max = filtered_df['Quantity Change %'].max()

    # Adjust bounds for more leniency
    x_padding = (x_max - x_min) * 0.1
    y_padding = (y_max - y_min) * 0.1
    x_min -= x_padding
    x_max += x_padding
    y_min -= y_padding
    y_max += y_padding

    # Define the line y = -x for reference
    fig.add_trace(go.Scatter(x=[x_min, x_max], y=[-x_min, -x_max], mode='lines', name='y = -x', line=dict(color='black', dash='dash')))

    # Add shading for good and bad promotion areas using trapezoids
    # Green area (above the line)
    fig.add_shape(type="path",
                  path=f"M {x_min},{-x_min} L {x_max},{-x_max} L {x_max},{y_max} L {x_min},{y_max} Z",
                  fillcolor="rgba(0, 255, 0, 0.2)", line=dict(width=0), layer="below")

    # Red area (below the line)
    fig.add_shape(type="path",
                  path=f"M {x_min},{-x_min} L {x_max},{-x_max} L {x_max},{y_min} L {x_min},{y_min} Z",
                  fillcolor="rgba(255, 0, 0, 0.2)", line=dict(width=0), layer="below")

    # Set the axis ranges based on the data
    fig.update_xaxes(range=[x_min, x_max])
    fig.update_yaxes(range=[y_min, y_max])

    # Add annotations for "Effective Promotions" and "Ineffective Promotions"
    fig.add_annotation(x=x_max, y=y_max, text="Effective Promotions", showarrow=False, xanchor='left', yanchor='top', bgcolor='rgba(0,255,0,0.3)', bordercolor='black')
    fig.add_annotation(x=x_max, y=y_min, text="Ineffective Promotions", showarrow=False, xanchor='left', yanchor='bottom', bgcolor='rgba(255,0,0,0.3)', bordercolor='black')
    # Display the plot
    st.plotly_chart(fig)

    # Display the filtered data
    st.write(filtered_df[['Start Date', 'Product Name', 'Category', 'Price Change %', 'Quantity Change %']])

def display_comparative_analysis(df):
     # Convert 'Start Date' to datetime
    # Convert 'Start Date' to datetime
    df['Start Date'] = pd.to_datetime(df['Start Date'])


    default_date = '2024-05-16'
    default_product = 'OCEAN SPRAY CRAN/GRAPE DIET 64 OZ'
    date_options = df['Start Date'].dt.strftime('%Y-%m-%d').unique()

    # Select date and product
    if default_date not in date_options:
        default_date = date_options[-1]  # Fallback to the latest date if default is not available

    # Select date
    selected_date = st.selectbox(
        'Select a date to show',
        options=date_options,
        index=list(date_options).index(default_date)  # Set the default index
    )

    filtered_df = df[df['Start Date'].dt.strftime('%Y-%m-%d') == selected_date]

    product_options = filtered_df['Product Name'].unique()
    if default_product not in product_options:
        default_product = product_options[0]  # Fallback to the first product if default is not available

    # Select product
    selected_product = st.selectbox('Select a product for analysis', options=product_options, index=list(product_options).index(default_product))
    product_data = filtered_df[filtered_df['Product Name'] == selected_product]


    # Assuming 'Dollar Change' and 'Price Change %' are already calculated in df
    dollar_change = product_data['Dollar Change'].values[0]
    price_change_percent = product_data['Price Change %'].values[0]
    previous_week_date = (pd.to_datetime(selected_date) - pd.Timedelta(weeks=1)).strftime('%Y-%m-%d')

    # Display summary text

    price_change_percent = product_data['Price Change %'].values[0]
    price_trend = "increased" if price_change_percent > 0 else "decreased"
    trend_color = "green" if price_change_percent > 0 else "red"
    trend_emoji = "⬆️" if price_change_percent > 0 else "⬇️"


    st.markdown(f"""
    ### <span style='background-color:#0000FF; padding:5px; border-radius:5px; font-family:monospace;'>{selected_product}</span> 
    <span style='color:{trend_color};'>{trend_emoji} {price_trend}</span> in price from {previous_week_date} to {selected_date} 
    ({price_change_percent:.2f}%)
    """, unsafe_allow_html=True)#    st.markdown(f"### {selected_product} {price_trend} in price from {previous_week_date} to {selected_date} by ${dollar_change:.2f} ({price_change_percent:.2f}%)")

    # Create columns for charts
    col1, col2 = st.columns(2)

    # First chart: Quantity vs. Previous Week Quantity
    with col1:
        st.header("Quantity Comparison")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=[previous_week_date, selected_date], y=[product_data['Previous Week Quantity'].values[0], product_data['Quantity'].values[0]], mode='lines+markers', name='Quantity'))
        fig1.update_layout(title='Quantity vs Previous Week Quantity', xaxis_title='Date', yaxis_title='Quantity')
        st.plotly_chart(fig1)

    # Second chart: Total Quantity vs. Previous Week Total Quantity
    with col2:
        st.header("All Econo Sales")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[previous_week_date, selected_date], y=[product_data['Previous Week Total Quantity'].values[0], product_data['Total Quantity'].values[0]], mode='lines+markers', name='Total Quantity'))
        fig2.update_layout(title='Total Quantity vs Previous Week Total Quantity', xaxis_title='Date', yaxis_title='Total Quantity')
        st.plotly_chart(fig2)


    quantity_change = product_data['Quantity'].values[0] - product_data['Previous Week Quantity'].values[0]
    quantity_percent_change = (quantity_change / product_data['Previous Week Quantity'].values[0]) * 100 if product_data['Previous Week Quantity'].values[0] != 0 else 0

    total_quantity_change = product_data['Total Quantity'].values[0] - product_data['Previous Week Total Quantity'].values[0]
    total_quantity_percent_change = (total_quantity_change / product_data['Previous Week Total Quantity'].values[0]) * 100 if product_data['Previous Week Total Quantity'].values[0] != 0 else 0

    # Display detailed change information
    quantity_trend = "increased" if quantity_change > 0 else "decreased"
    total_quantity_trend = "increased" if total_quantity_change > 0 else "decreased"



    st.markdown(f"**{selected_product}** {quantity_trend} from **{product_data['Previous Week Quantity'].values[0]:,.2f}** to **{product_data['Quantity'].values[0]:,.2f}** ({quantity_percent_change:.2f}%), while all sales {total_quantity_trend} from **{product_data['Previous Week Total Quantity'].values[0]:,.2f}** to **{product_data['Total Quantity'].values[0]:,.2f}** ({total_quantity_percent_change:.2f}%).")

'''
# :basket: BetterBasket and Econo

'''



tab1, tab2, tab3 = st.tabs(["Quantity Impact of Price Changes", "Month-Over-Month Data", "In Depth Analysis"])

with tab1:
    display_scatter_plot_and_data(df, "Quantity Impact of Price Changes",  "selected_dates_tab1")

with tab2:
    display_scatter_plot_and_data(df4wk, "Month-Over-Month Data", "selected_dates_tab2")


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.

#tab1, tab2, tab3 = st.tabs(["Scatter Plot: Week over Week","Scatter Plot: Month over Month", "Recommendations"])


with tab3:
    display_comparative_analysis(df)
