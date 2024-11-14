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

def get_aguadillasales_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/Aguadilla_sales_073124.csv'
    df = pd.read_csv(DATA_FILENAME)

    

    return df

aguadilla_sales = get_aguadillasales_data()

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
    st.markdown(f"### Showing data for  week of {selected_date} compared to week of {previous_week_date}")

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
    df['Start Date'] = pd.to_datetime(df['Start Date'])

    # Set default date and product
    default_date = '2024-05-16'
    default_product = 'OCEAN SPRAY CRAN/GRAPE DIET'

    # Get unique dates in the dataframe
    date_options = df['Start Date'].dt.strftime('%Y-%m-%d').unique()

    # Sidebar selectors for date and product
    selected_date = st.sidebar.selectbox(
        'Select a date to show',
        options=date_options,
        index=list(date_options).index(default_date) if default_date in date_options else 0
    )

    # Filter data for the selected date
    filtered_df = df[df['Start Date'].dt.strftime('%Y-%m-%d') == selected_date]

    # Product selection in the sidebar
    product_options = filtered_df['Product Name'].unique()
    selected_product = st.sidebar.selectbox(
        'Select a product for analysis', 
        options=product_options, 
        index=list(product_options).index(default_product) if default_product in product_options else 0
    )

    # Filter data for the selected product over the last 4 weeks
    product_history = df[df['Product Name'] == selected_product]

    # Get the latest date for the selected product
    latest_date = product_history['Start Date'].max()

    # Filter for the last 4 weeks
    start_date = latest_date - pd.Timedelta(weeks=4)
    product_history_last_4_weeks = product_history[product_history['Start Date'] > start_date]

  
    product_data = product_history[product_history['Start Date'].dt.strftime('%Y-%m-%d') == selected_date]
    previous_week_date = (pd.to_datetime(selected_date) - pd.Timedelta(weeks=1)).strftime('%Y-%m-%d')

    dollar_change = product_data['Dollar Change'].values[0]
    price_change_percent = product_data['Price Change %'].values[0]
    price_trend = "increased" if price_change_percent > 0 else "decreased"
    trend_color = "green" if price_change_percent > 0 else "red"
    trend_emoji = "⬆️" if price_change_percent > 0 else "⬇️"
    
    # Extract relevant columns for display
    display_columns = ['Start Date', 'Total Quantity']
    product_history_display = product_history_last_4_weeks[display_columns]
    st.markdown(f"""
    <span style='font-size:30px;'>
        <span style='background-color:#0000FF; padding:5px; border-radius:5px; font-family:monospace;'>{selected_product}</span> 
        <span style='color:{trend_color};'>{trend_emoji} {price_trend}</span> in price from {previous_week_date} to {selected_date} 
        by ${dollar_change:.2f} ({price_change_percent:.2f}%)
    </span>
    """, unsafe_allow_html=True)
    # Display summary text
    price_trend = "increased" if dollar_change > 0 else "decreased"


    quantity_change = product_data['Quantity'].values[0] - product_data['Previous Week Quantity'].values[0]
    quantity_percent_change = (quantity_change / product_data['Previous Week Quantity'].values[0]) * 100 if product_data['Previous Week Quantity'].values[0] != 0 else 0

    total_quantity_change = product_data['Total Quantity'].values[0] - product_data['Previous Week Total Quantity'].values[0]
    total_quantity_percent_change = (total_quantity_change / product_data['Previous Week Total Quantity'].values[0]) * 100 if product_data['Previous Week Total Quantity'].values[0] != 0 else 0

    # Display detailed change information
    quantity_trend = "increased" if quantity_change > 0 else "decreased"
    total_quantity_trend = "increased" if total_quantity_change > 0 else "decreased"

    st.markdown(f"""
        <span style='font-size:30px;'>
            <span style='background-color:#0000FF; padding:5px; border-radius:5px; font-family:monospace;'>{selected_product}</span> 
            {quantity_trend} from <strong>{product_data['Previous Week Quantity'].values[0]:,}</strong> to 
            <strong>{product_data['Quantity'].values[0]:,}</strong> ({quantity_percent_change:.2f}%), while all store sales {total_quantity_trend} 
            from <strong>{product_data['Previous Week Total Quantity'].values[0]:,}</strong> to 
            <strong>{product_data['Total Quantity'].values[0]:,}</strong> ({total_quantity_percent_change:.2f}%).
        </span>
        """, unsafe_allow_html=True)    
    
    
    # Display charts for Quantity and Total Quantity comparison
    col1, col2 = st.columns(2)

    with col1:
        st.header("Quantity Comparison Over Time")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=product_history_last_4_weeks['Start Date'], 
            y=product_history_last_4_weeks['Quantity'], 
            mode='lines+markers', 
            name='Quantity'
        ))
        fig1.update_layout(title='Quantity Over Last 4 Weeks', xaxis_title='Date', yaxis_title='Quantity')
        st.plotly_chart(fig1)

    with col2:
        st.header("Total Quantity Comparison Over Time")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=product_history_last_4_weeks['Start Date'], 
            y=product_history_last_4_weeks['Total Quantity'], 
            mode='lines+markers', 
            name='Total Quantity'
        ))
        fig2.update_layout(title='Total Quantity Over Last 4 Weeks', xaxis_title='Date', yaxis_title='Total Quantity')
        st.plotly_chart(fig2)





        


   # Create a table for the data
    table_data = {
        "Metric": ["Price Change (Dollar)", "Price Change (%)", "Quantity Change (%)"],
        "Selected Item": [
            f"${dollar_change:.2f}" if dollar_change else "N/A", 
            f"{price_change_percent:.2f}% {trend_emoji}", 
            f"{quantity_percent_change:.2f}%"
        ],
        "All Items": ["N/A",  "N/A", f"{total_quantity_percent_change:.2f}%"]
    }
    df_table = pd.DataFrame(table_data)

    st.table(df_table)

# Function to display the scatter plot for the new data
def display_new_chain_data(df):
    st.title("Aguadilla Sales Analysis")


    # Ensure 'UPC' and 'Item' columns are strings
    df['UPC'] = df['UPC'].astype(str)
    df['Item'] = df['Item'].astype(str)

    # Convert percentage change columns to numeric after stripping '%' symbol
    df['Price Change %'] = pd.to_numeric(df['Price Change %'].astype(str).str.replace('%', ''), errors='coerce') * 100
    df['Quantity Change %'] = pd.to_numeric(df['Quantity Change %'].astype(str).str.replace('%', ''), errors='coerce') * 100

    # Convert price and quantity columns to numeric
    df['Price 7/31'] = pd.to_numeric(df['Price 7/31'], errors='coerce')
    df['Price 7/24'] = pd.to_numeric(df['Price 7/24'], errors='coerce')
    df['Quantity 7/31'] = pd.to_numeric(df['Quantity 7/31'], errors='coerce')
    df['Quantity 7/24'] = pd.to_numeric(df['Quantity 7/24'], errors='coerce')

 
    # Filter data where Price Change % is nonzero
    df_filtered = df[df['Price Change %'] != 0]

        # Determine increase or decrease
    df_filtered['Price Change Direction'] = df_filtered['Price Change %'].apply(lambda x: 'increased' if x > 0 else 'decreased')
    df_filtered['Quantity Change Direction'] = df_filtered['Quantity Change %'].apply(lambda x: 'increased' if x > 0 else 'decreased')

    # Create custom hover text
    df_filtered['hover_text'] = df_filtered.apply(
        lambda row: f"<b>{row['Item']}</b> price {row['Price Change Direction']} from {row['Price 7/24']:.2f} to {row['Price 7/31']:.2f}.<br>"
                    f"{row['Item']} quantity sold {row['Quantity Change Direction']} from {row['Quantity 7/24']:.2f} in 7/24 to {row['Quantity 7/31']:.2f} in 7/31.",
        axis=1
    )

    # Scatter plot using Plotly
    fig = px.scatter(
        df_filtered, 
        x='Price Change %', 
        y='Quantity Change %', 
        title='Scatter Plot of Price Change % vs Quantity Change %',
        labels={'Price Change %': 'Price Change %', 'Quantity Change %': 'Quantity Change %'},
        color='Item',
        size_max=20,
        custom_data=['hover_text']
    )


    min_value = min(df_filtered[['Price Change %', 'Quantity Change %']].min())
    max_value = max(df_filtered[['Price Change %', 'Quantity Change %']].max())

    # Add the y=-x line
    fig.add_shape(
        type='line',
        line=dict(dash='dash', color='red'),
        x0=min_value,
        y0=-min_value,
        x1=max_value,
        y1=-max_value
    )


    fig.update_traces(
        hovertemplate='%{customdata[0]}<extra></extra>'
    )
   # Add annotations
    fig.add_annotation(
        x=max_value, 
        y=max_value,
        text="Effective Promotion",
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        font=dict(color='green', size=14)
    )

    fig.add_annotation(
        x=min_value, 
        y=min_value,
        text="Ineffective Promotion",
        showarrow=False,
        xanchor='left',
        yanchor='top',
        font=dict(color='red', size=14)
    )

    # Update the layout to include the correct axis range
    fig.update_layout(
        xaxis=dict(range=[min_value, max_value]),
        yaxis=dict(range=[min_value, max_value])
    )


    # Display the plot
    st.plotly_chart(fig)

    # Display the filtered data
    st.write(df_filtered[['UPC', 'Item', 'Price 7/31', 'Price 7/24', 'Quantity 7/31', 'Quantity 7/24']])

'''
# :basket: BetterBasket and Econo

'''



tab1, tab2, tab3, tab4 = st.tabs(["Humacao - Weekly Price Change Analysis", "Humacao - Monthly Price Change Analysis", "Humacao - In Depth Analysis", "Aguadilla - Weekly Price Change Analysis"])

with tab1:
    display_scatter_plot_and_data(df, "Weekly Sales Change vs Price Change - Humacao",  "selected_dates_tab1")

with tab2:
    display_scatter_plot_and_data(df4wk, "Monthly Sales Change vs Price Change - Humacao", "selected_dates_tab2")


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.

#tab1, tab2, tab3 = st.tabs(["Scatter Plot: Week over Week","Scatter Plot: Month over Month", "Recommendations"])


with tab3:
    display_comparative_analysis(df)

with tab4:
    display_new_chain_data(aguadilla_sales)
