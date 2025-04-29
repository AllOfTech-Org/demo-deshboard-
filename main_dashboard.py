import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import numpy as np
import json
import os
from data_processor import DashboardDataProcessor

# Load text configuration from JSON file
def load_text_config():
    """Load the text configuration from a JSON file."""
    if os.path.exists('text_config.json'):
        with open('text_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "metrics": {
            "title": "Key Performance Indicators",
            "content": "Total sales 3,086,472 Dollars (↑ 7.7% increase), average daily sales 101,239 Taka (↑ 4.0% increase), total customers 1,679 (↑ 5.9%increase). Return rate 9.2% (↓ 0.1% decrease).",
            "advice": "Performance is strong, especially with an ↑ 7.7% increase in total and daily sales. Return rate has decreased, which is a good sign. Look for ways to further increase customer growth rate."
        },
        "sales_trend": {
            "title": "Sales Trend Analysis",
            "content": "Daily sales fluctuated from July to October 2023. Notably, peak sales (200,000+ Taka) were seen at the beginning of July and September. Return amounts are very low (usually below 10,000 Taka).",
            "advice": "Analyze the reasons for sales peaks in July and early September. On August 12, sales were 75,303 Taka. Identify causes for sales growth at the end of September and apply them to other periods."
        },
        "order_analysis": {
            "title": "Order Source Analysis",
            "content": "Website (43.6%) is your main order source, followed by Instagram (21.3%), Facebook (16.7%), and direct sales (11.9%). Product_18, Product_12, and Product_8 are the best sellers, approximately 850,000, 800,000, and 750,000 Taka respectively.",
            "advice": "Increase investment in website and Instagram marketing. Keep sufficient stock of Product_18, Product_12, and Product_8 and increase promotion of these products."
        },
        "inventory": {
            "title": "Inventory Management Insights",
            "content": "Accessories (310+) and Jackets (280+) categories have the highest stock items. The second graph shows T-shirts and Shirts have higher sales (3M+ and 2M+ Taka) but comparatively lower stock (245 and 270 items).",
            "advice": "Reduce high stock of Accessories (310+) as their sales are relatively low (less than 1M Taka). Increase inventory of T-shirts (high sales, low stock). Optimize inventory and sales ratio."
        },
        "category": {
            "title": "Category Performance Review",
            "content": "T-shirt category generates the highest revenue (2.8M+ Taka, 30.6% of total sales), followed by Shirts (2.4M Taka, 25.8%), Jeans (2.1M Taka, 22.8%), Jackets (1.2M Taka, 13.3%), and Accessories (700K Taka, 7.4%).",
            "advice": "Add new products in T-shirt and Shirt categories to strengthen these segments. Use cross-selling strategies to increase sales in Accessories category."
        },
        "profitability": {
            "title": "Profitability Assessment",
            "content": "T-shirts provide the highest revenue (2.8M+ Taka) and profit (850K Taka). Jeans revenue is 2.1M+ Taka with 750K Taka profit. Across the 5 categories, profit margins range between 25-30%.",
            "advice": "Maintain profitability of T-shirts and Jeans. Find ways to reduce costs or launch premium lines to increase profit margins of Accessories and Jackets."
        },
        "customer_insights": {
            "title": "Customer Behavior Analysis",
            "content": "From July to October 2023, August saw the highest 600 new customers, which decreased to around 500 in October. Average customer spending was 6150 Taka in July and August, dropped to 5750 Taka in September, and rose again to 6030 Taka in October.",
            "advice": "Investigate reasons for customer growth in August (promotion/event?). Analyze causes for drop in average order value in September. Apply strategies for growth in October to other months."
        },
        "growth": {
            "title": "Growth and Value Analysis",
            "content": "From July to October 2023, customer count increased from about 100 in July to 600 in August, then gradually decreased. Average customer spending was 6150 Taka in July-August, dropped to 5750 Taka in September, and rose again in October.",
            "advice": "Identify and apply August growth strategies to other months. Investigate reasons for drop in customer spending in September. Launch customer loyalty programs to retain customers and increase their spending."
        }
    }


# Load the text configuration
TEXT_CONFIG = load_text_config()

def create_text_container(title, content, advice):
    return f"""
    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-top: 10px;'>
    <h4>{title}</h4>
    <p>{content}</p>
    <hr style='border-top: 1px solid #ccc;'>
    <h5><strong>Advice :</strong></h5>
    <p>{advice}</p>
    </div>
    """

# Set page configuration
st.set_page_config(
    page_title="AllOfTech Dashboard",
    page_icon="images/my_Logo.png",
    layout="wide",
)

# Hide default UI elements
hide_default_ui = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_default_ui, unsafe_allow_html=True)

######################################
# Custom Styling with Background
######################################
def set_custom_style(background_image_path, sidebar_image_path):
    with open(background_image_path, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    with open(sidebar_image_path, "rb") as sidebar_img:
        sidebar_encoded = base64.b64encode(sidebar_img.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid=stSidebar] {{
        background-image: url("data:image/png;base64,{sidebar_encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    .stSidebar .sidebar-content {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(5px);
        padding: 1rem;
        border-radius: 10px;
    }}

    .main .block-container {{
        padding: 2rem;
    }}

    [data-testid="stMetricLabel"] {{
        color: black !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}

    [data-testid="stMetricValue"] {{
        color: black !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
    }}

    [data-testid="stMetricDelta"] {{
        color: black !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}

    .js-plotly-plot .plotly .gtitle, 
    .js-plotly-plot .plotly .xtitle,
    .js-plotly-plot .plotly .ytitle,
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {{
        color: black !important;
        fill: black !important;
    }}

    .stSelectbox label, 
    .stMultiSelect label,
    .stSelectbox span,
    .stMultiSelect span {{
        color: black !important;
    }}

    .stSidebar [data-testid="stSidebarNav"] {{
        color: black !important;
    }}

    .kpi-title {{
        color: black !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }}

    [data-testid="column"] {{
        padding: 0.5rem !important;
    }}

    .sidebar-logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }}

    .sidebar-logo {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 2px solid #00000033;
        object-fit: cover;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def plot_defaults():
    return {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': 'black', 'size': 12, 'family': 'Arial, sans-serif'},
        'title': {'font': {'color': 'black', 'size': 14, 'weight': 'bold'}},
        'xaxis': {
            'title': {'font': {'color': 'black', 'size': 12}},
            'tickfont': {'color': 'black', 'size': 12},
            'gridcolor': 'rgba(128,128,128,0.1)',
            'gridwidth': 0.5,
            'tickcolor': 'black',
            'linecolor': 'black'
        },
        'yaxis': {
            'title': {'font': {'color': 'black', 'size': 12}},
            'tickfont': {'color': 'black', 'size': 12},
            'gridcolor': 'rgba(128,128,128,0.1)',
            'gridwidth': 0.5,
            'tickcolor': 'black',
            'linecolor': 'black'
        },
        'legend': {
            'font': {'color': 'black', 'size': 12},
            'title': {'font': {'color': 'black', 'size': 12}}
        },
        'margin': {'l': 20, 'r': 20, 't': 40, 'b': 20}
    }

######################################
# Dashboard Components
######################################
def show_metrics_chart(metrics_data, text_content=""):
    st.markdown('<div class="kpi-title">Key Performance Indicators</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    # Apply white background with black text to each metric box
    with col1:
        st.markdown(
            '<div style="border: 2px solid black; background-color: black; padding: 10px; border-radius: 10px; height: 100%;">'
            f'<p style="color: white; margin: 0; font-size: 1rem;">Total Sales</p>'
            f'<p style="color: white; margin: 0; font-size: 1.5rem; font-weight: bold;">{metrics_data["currency_symbol"]}{metrics_data["total_sales"]:,.0f}</p>'
            f'<p style="color: green; margin: 0; font-size: 0.9rem;">↑ {metrics_data["sales_growth"]}%</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            '<div style="border: 2px solid black; background-color: black; padding: 10px; border-radius: 10px; height: 100%;">'
            f'<p style="color: white; margin: 0; font-size: 1rem;">Avg Daily Sales</p>'
            f'<p style="color: white; margin: 0; font-size: 1.5rem; font-weight: bold;">{metrics_data["currency_symbol"]}{metrics_data["avg_daily_sales"]:,.0f}</p>'
            f'<p style="color: green; margin: 0; font-size: 0.9rem;">↑ {metrics_data["daily_sales_growth"]}%</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            '<div style="border: 2px solid black; background-color: black; padding: 10px; border-radius: 10px; height: 100%;">'
            f'<p style="color: white; margin: 0; font-size: 1rem;">Total Customers</p>'
            f'<p style="color: white; margin: 0; font-size: 1.5rem; font-weight: bold;">{metrics_data["total_customers"]:,}</p>'
            f'<p style="color: green; margin: 0; font-size: 0.9rem;">↑ {metrics_data["customer_growth"]}%</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            '<div style="border: 2px solid black; background-color: black; padding: 10px; border-radius: 10px; height: 100%;">'
            f'<p style="color: white; margin: 0; font-size: 1rem;">Return Rate</p>'
            f'<p style="color: white; margin: 0; font-size: 1.5rem; font-weight: bold;">{metrics_data["return_rate"]:.1f}%</p>'
            f'<p style="color: red; margin: 0; font-size: 0.9rem;">↓ {metrics_data["return_rate_change"]}%</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

def get_dynamic_label(data_series, column_name, currency_symbol):
    max_value = data_series[column_name].max()
    if max_value >= 1000000:
        return f'{column_name} ({currency_symbol})'
    return f'{column_name} ({currency_symbol})'

def show_line_chart(sales_data, currency_symbol, text_content=""):
    # Rename columns for display with currency info
    sales_data = sales_data.copy()
    sales_label = get_dynamic_label(sales_data, 'sales', currency_symbol)
    returns_label = get_dynamic_label(sales_data, 'returns', currency_symbol)
    
    sales_data.rename(columns={
        'sales': sales_label,
        'returns': returns_label
    }, inplace=True)

    st.markdown('<h3 style="color: black;">Your Daily Business Performance</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 0.9rem;">This chart shows your daily earnings and returns. Hover over the lines to see exact amounts.</p>', unsafe_allow_html=True)
    with st.container():
        fig = px.line(sales_data, x='date', y=[sales_label, returns_label],
                      title='Your Daily Income and Returns',
                      labels={
                          'date': 'Date',
                          'value': 'Amount'
                      },
                      template='plotly_white')
        fig.update_layout(**plot_defaults())
        fig.update_layout(dragmode=False)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
            }
        )
        st.markdown(text_content, unsafe_allow_html=True)

def show_order_source_and_top_products(order_data, product_data, currency_symbol, text_content=""):
    st.markdown('<h3 style="color: black;">Where Your Money Comes From</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 0.9rem;">See which sales channels bring you the most money and which products sell the best. Hover over the charts to see exact amounts.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.pie(order_data, values='sales', names='order_source',
                      title='How Customers Buy From You',
                      template='plotly_white',
                      hole=0.3)
        fig1.update_layout(**plot_defaults())
        fig1.update_traces(
            textfont={'color': 'black', 'size': 12},
            textinfo='percent+label',
            marker=dict(line=dict(color='black', width=1)),
            hovertemplate='%{label}<br>Amount: %{value:,.0f} {currency_symbol}<br>Percentage: %{percent:.1%}<extra></extra>'
        )
        fig1.update_layout(dragmode=False)
        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
            }
        )

    with col2:
        st.markdown('<h5 style="color: black;">Your Best Selling Products</h5>', unsafe_allow_html=True)
        fig2 = px.bar(product_data, x="sales", y="product_id", orientation="h",
                      title="Your Top 10 Money-Making Products",
                      labels={
                          "sales": f"Money Earned in {currency_symbol} ",
                          "product_id": "Product Name"
                      },
                      template="plotly_white")
        layout = plot_defaults()
        layout["yaxis"].update({'categoryorder': 'total ascending'})
        fig2.update_layout(**layout)
        fig2.update_traces(
            hovertemplate='Product: %{y}<br>Amount: %{x:,.0f} {currency_symbol}<extra></extra>'
        )
        fig2.update_layout(dragmode=False)
        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
            }
        )

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

def show_customer_growth_and_avg_order_value(monthly_data, currency_symbol, text_content=""):
    # Rename columns for display with currency info
    monthly_data = monthly_data.copy()
    avg_spending_label = get_dynamic_label(monthly_data, 'avg_order_value', currency_symbol)
    
    monthly_data.rename(columns={
        'avg_order_value': avg_spending_label,
        'new_customers': 'New Customers'
    }, inplace=True)

    st.markdown('<h3 style="color: black;">Growing Your Business</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 0.9rem;">See how your customer base and their spending are growing.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(monthly_data, x='month', y='New Customers',
                       title='New Customers Each Month',
                       markers=True,
                       template='plotly_white',
                       labels={
                           "month": "Month",
                           "New Customers": "Number of New Customers"
                       })
        fig1.update_layout(**plot_defaults())
        fig1.update_layout(dragmode=False)
        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
            }
        )

    with col2:
        fig2 = px.line(monthly_data, x='month', 
                       y=avg_spending_label,
                       title='How Much Each Customer Spends',
                       markers=True,
                       template='plotly_white',
                       labels={
                           "month": "Month"
                       })
        fig2.update_layout(**plot_defaults())
        fig2.update_layout(dragmode=False)
        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
            }
        )

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

def show_category_analysis(category_data, currency_symbol, text_content=""):
    st.markdown('<h3 style="color: black;">How Different Product Types Perform</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 0.9rem;">See which types of products make you the most money. Hover over the bars and pie slices to see exact amounts.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(category_data, x='category', y='sales',
                      title='Money Earned by Product Type',
                      labels={
                          'sales': f'Total Money Earned in {currency_symbol} (1M = 1,000,000)',
                          'category': 'Product Type'
                      },
                      template='plotly_white')
        layout = plot_defaults()
        layout.update(bargap=0.3)
        fig1.update_layout(**layout)
        fig1.update_traces(
            marker=dict(
                color='rgba(0, 128, 255, 0.8)',
                line=dict(color='rgba(0, 128, 255, 0.8)', width=0)
            ),
            hovertemplate='Product Type: %{x}<br>Amount: %{y:,.0f} {currency_symbol}<extra></extra>'
        )
        fig1.update_layout(dragmode=False)
        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
            }
        )
    with col2:
        fig2 = px.pie(category_data, values='sales', names='category',
                      title='How Your Sales Are Split',
                      template='plotly_white',
                      hole=0.4)
        fig2.update_layout(**plot_defaults())
        fig2.update_traces(
            textfont={'color': 'black', 'size': 12},
            textinfo='percent+label',
            hovertemplate='%{label}<br>Amount: %{value:,.0f} {currency_symbol}<br>Percentage: %{percent:.1%}<extra></extra>'
        )
        fig2.update_layout(dragmode=False)
        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
            }
        )

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

def show_inventory_analysis(inventory_data, currency_symbol, text_content=""):
    st.markdown('<h3 style="color: black;">Your Stock Status</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 0.9rem;">Keep track of what products you have in stock. Hover over the charts to see exact numbers.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(inventory_data, x='category', y='inventory',
                      title='How Many Items You Have in Stock',
                      labels={
                          'inventory': 'Number of Items',
                          'category': 'Product Type'
                      },
                      template='plotly_white')
        fig1.update_layout(**plot_defaults())
        fig1.update_traces(
            marker=dict(
                color='rgba(0, 128, 255, 0.8)',
                line=dict(color='rgba(0, 128, 255, 0.8)', width=0)
            ),
            hovertemplate='Product Type: %{x}<br>Items in Stock: %{y:,.0f}<extra></extra>'
        )
        fig1.update_layout(dragmode=False)
        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
            }
        )
    with col2:
        fig2 = px.scatter(inventory_data, x='sales', y='inventory',
                          size='profit_margin', color='category',
                          title='Sales vs Stock Levels',
                          labels={
                              'sales': f'Money Earned in {currency_symbol} (1M = 1,000,000)',
                              'inventory': 'Items in Stock',
                              'profit_margin': 'Profit %',
                              'category': 'Product Type'
                          },
                          template='plotly_white')
        fig2.update_layout(**plot_defaults())
        fig2.update_traces(
            marker=dict(line=dict(width=1, color='black')),
            hovertemplate='Product Type: %{customdata[0]}<br>Money Earned: %{x:,.0f} {currency_symbol}<br>Items in Stock: %{y:,.0f}<br>Profit: %{marker.size:.1f}%<extra></extra>'
        )
        fig2.update_layout(dragmode=False)
        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
            }
        )

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

def show_profitability_analysis(profit_data, currency_symbol, text_content=""):
    # Rename columns for display with currency info
    profit_data = profit_data.copy()
    sales_label = get_dynamic_label(profit_data, 'sales', currency_symbol)
    profit_label = get_dynamic_label(profit_data, 'profit', currency_symbol)
    
    profit_data.rename(columns={
        'sales': sales_label,
        'profit': profit_label
    }, inplace=True)

    st.markdown('<h3 style="color: black;">Your Profit Overview</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 0.9rem;">See how much money you make after costs. Hover over the bars to see exact amounts.</p>', unsafe_allow_html=True)
    
    fig = px.bar(profit_data, x='category', 
                 y=[sales_label, profit_label],
                 title='Money Earned vs Actual Profit',
                 labels={
                     'category': 'Product Type',
                     'value': 'Amount'
                 },
                 barmode='group', template='plotly_white')
    fig.update_layout(**plot_defaults())
    fig.update_layout(dragmode=False)
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "displaylogo": False,
            "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
        }
    )

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

def show_customer_insights(customer_data, currency_symbol, text_content=""):
    # Rename columns for display with currency info
    customer_data = customer_data.copy()
    avg_order_label = get_dynamic_label(customer_data, 'avg_order_value', currency_symbol)
    
    customer_data.rename(columns={
        'avg_order_value': avg_order_label,
        'new_customers': 'New Customers'
    }, inplace=True)

    st.markdown('<h3 style="color: black;">Understanding Your Customers</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666; font-size: 0.9rem;">Track how many customers you get and how much they spend.</p>', unsafe_allow_html=True)
    
    fig = px.line(customer_data, x='month', 
                  y=['New Customers', avg_order_label],
                  title='Customer Growth and Spending',
                  labels={
                      'month': 'Month',
                      'value': 'Amount'
                  },
                  template='plotly_white')
    fig.update_layout(**plot_defaults())
    fig.update_layout(dragmode=False)
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "displaylogo": False,
            "modeBarButtonsToAdd": ["downloadImage", "fullscreen"]
        }
    )

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

######################################
# Main App
######################################
def main():
    # Initialize data processor
    processor = DashboardDataProcessor()
    
    # Set custom style
    set_custom_style("images/background_image.avif", "images/sidebar2.jpg")

    with st.sidebar:
        st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
        logo_encoded = base64.b64encode(open("images/my_Logo.png", "rb").read()).decode()
        st.markdown(f'<img src="data:image/png;base64,{logo_encoded}" class="sidebar-logo"/>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<h2 style="color: black;">Filters</h2>', unsafe_allow_html=True)
        
        # Currency selector
        currency = st.selectbox(
            "Select Currency",
            options=["USD", "Your Currency"],
            index=0
        )
        processor.set_currency(currency)
        
        # Get date range from data
        min_date = processor.df['date'].min()
        max_date = processor.df['date'].max()
        
        # Quick date range selector
        date_range_option = st.selectbox(
            "Quick Date Range",
            options=[
                "All Time",
                "Last 7 Days",
                "Last 14 Days",
                "Last 30 Days",
                "Last 3 Months(suggestions will be shown)",
                "Last 6 Months",
                "Last Year",
                "Custom Range"
            ],
            index=4
        )
        
        # Calculate date ranges based on selection
        if date_range_option == "Last 7 Days":
            date_range = (max_date - pd.Timedelta(days=7), max_date)
        elif date_range_option == "Last 14 Days":
            date_range = (max_date - pd.Timedelta(days=14), max_date)
        elif date_range_option == "Last 30 Days":
            date_range = (max_date - pd.Timedelta(days=30), max_date)
        elif date_range_option == "Last 3 Months(suggestions will be shown)":
            date_range = (max_date - pd.Timedelta(days=90), max_date)
        elif date_range_option == "Last 6 Months":
            date_range = (max_date - pd.Timedelta(days=180), max_date)
        elif date_range_option == "Last Year":
            date_range = (max_date - pd.Timedelta(days=365), max_date)
        elif date_range_option == "All Time":
            date_range = (min_date, max_date)
        else:  # Custom Range
            date_range = st.date_input(
                "Select Custom Date Range",
                value=(min_date, max_date)
            )
        
        # Get unique categories
        categories = processor.df['category'].unique()
        selected_categories = st.multiselect(
            "Select Categories",
            options=categories,
            default=categories
        )

    st.markdown('<h1 style="text-align: center; color: black;">AllOfTech Dashboard</h1>', unsafe_allow_html=True)

    # Apply filters to the data
    processor.apply_filters(date_range=date_range, categories=selected_categories)

    # Get all processed data
    metrics_data = processor.get_metrics_data()
    sales_data = processor.get_sales_trend_data()
    order_data = processor.get_order_source_data()
    product_data = processor.get_product_data()
    category_data = processor.get_category_data()
    inventory_data = processor.get_inventory_data()
    monthly_data = processor.get_customer_growth_data()
    profit_data = processor.get_profitability_data()
    customer_data = processor.get_customer_insights_data()

    # --- Decide whether to show text suggestions based on selected date range ---
    suggestion_period = "Last 3 Months(suggestions will be shown)"
    show_suggestions = (date_range_option == suggestion_period)
    # --------------------------------------------------------------------------

    # Display all charts - Pass text content only if show_suggestions is True
    text_metrics = create_text_container(TEXT_CONFIG['metrics']['title'], TEXT_CONFIG['metrics']['content'], TEXT_CONFIG['metrics']['advice']) if show_suggestions else ""
    show_metrics_chart(metrics_data, text_metrics)

    text_order = create_text_container(TEXT_CONFIG['order_analysis']['title'], TEXT_CONFIG['order_analysis']['content'], TEXT_CONFIG['order_analysis']['advice']) if show_suggestions else ""
    show_order_source_and_top_products(order_data, product_data, metrics_data['currency_symbol'], text_order)

    text_inventory = create_text_container(TEXT_CONFIG['inventory']['title'], TEXT_CONFIG['inventory']['content'], TEXT_CONFIG['inventory']['advice']) if show_suggestions else ""
    show_inventory_analysis(inventory_data, metrics_data['currency_symbol'], text_inventory)

    text_category = create_text_container(TEXT_CONFIG['category']['title'], TEXT_CONFIG['category']['content'], TEXT_CONFIG['category']['advice']) if show_suggestions else ""
    show_category_analysis(category_data, metrics_data['currency_symbol'], text_category)

    text_profit = create_text_container(TEXT_CONFIG['profitability']['title'], TEXT_CONFIG['profitability']['content'], TEXT_CONFIG['profitability']['advice']) if show_suggestions else ""
    show_profitability_analysis(profit_data, metrics_data['currency_symbol'], text_profit)

    text_sales = create_text_container(TEXT_CONFIG['sales_trend']['title'], TEXT_CONFIG['sales_trend']['content'], TEXT_CONFIG['sales_trend']['advice']) if show_suggestions else ""
    show_line_chart(sales_data, metrics_data['currency_symbol'], text_sales)

    # Only show customer insights and growth graphs for periods longer than 14 days
    if date_range_option not in ["Last 7 Days", "Last 14 Days"]:
        text_customer_insights = create_text_container(TEXT_CONFIG['customer_insights']['title'], TEXT_CONFIG['customer_insights']['content'], TEXT_CONFIG['customer_insights']['advice']) if show_suggestions else ""
        show_customer_insights(customer_data, metrics_data['currency_symbol'], text_customer_insights)

        text_growth = create_text_container(TEXT_CONFIG['growth']['title'], TEXT_CONFIG['growth']['content'], TEXT_CONFIG['growth']['advice']) if show_suggestions else ""
        show_customer_growth_and_avg_order_value(monthly_data, metrics_data['currency_symbol'], text_growth)
    else:
        st.info("Customer insights and growth analysis are only available for periods longer than 14 days.")

if __name__ == '__main__':
    main()