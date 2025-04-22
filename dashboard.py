import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import numpy as np
from data_processor import DashboardDataProcessor

# Text Configuration - This will be automatically updated by text_editor.py
TEXT_CONFIG = {
    "metrics": {
        "title": "Key Performance Indicators",
        "content": "Based on the current data, we observe strong performance in total sales and customer acquisition. The return rate is within acceptable limits, suggesting good product quality and customer satisfaction."
    },
    "sales_trend": {
        "title": "Sales Trend Analysis",
        "content": "The sales trend shows consistent growth with some seasonal variations. Returns are stable, indicating good product quality control."
    },
    "order_analysis": {
        "title": "Order Source Analysis",
        "content": "Website and social media channels are performing well as order sources. Consider increasing marketing efforts on high-performing channels."
    },
    "inventory": {
        "title": "Inventory Management Insights",
        "content": "Current inventory levels are well-balanced across categories. Consider adjusting stock levels based on sales velocity and seasonal trends."
    },
    "category": {
        "title": "Category Performance Review",
        "content": "T-Shirts and Jeans are leading categories in terms of sales. Consider expanding these product lines and analyzing underperforming categories."
    },
    "profitability": {
        "title": "Profitability Assessment",
        "content": "Profit margins are healthy across all categories. Focus on maintaining quality while optimizing production costs."
    },
    "customer_insights": {
        "title": "Customer Behavior Analysis",
        "content": "Customer acquisition is growing steadily. Implement loyalty programs to increase customer retention and repeat purchases."
    },
    "growth": {
        "title": "Growth and Value Analysis",
        "content": "Both customer base and average order value are showing positive trends. Consider upselling strategies to further increase average order value."
    }
}

def create_text_container(title, content):
    return f"""
    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-top: 10px;'>
    <h4>{title}</h4>
    <p>{content}</p>
    </div>
    """

# Set page configuration
st.set_page_config(
    page_title="Mr. Life Okey Dashboard",
    page_icon="images/logo.png",
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
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
                ]
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
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
                ]
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
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
                ]
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
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
                ]
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
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
                ]
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
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
                ]
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
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
                ]
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
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
                ]
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
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
                ]
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
            "scrollZoom": False,
            "displayModeBar": False,
            "doubleClick": False,
            "displaylogo": False,
            "modeBarButtonsToRemove": [
                "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
            ]
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
            "scrollZoom": False,
            "displayModeBar": False,
            "doubleClick": False,
            "displaylogo": False,
            "modeBarButtonsToRemove": [
                "zoom2d", "select2d", "lasso2d", "autoScale2d", "resetScale2d"
            ]
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
        logo_encoded = base64.b64encode(open("images/logo.png", "rb").read()).decode()
        st.markdown(f'<img src="data:image/png;base64,{logo_encoded}" class="sidebar-logo"/>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<h2 style="color: black;">Filters</h2>', unsafe_allow_html=True)
        
        # Currency selector
        currency = st.selectbox(
            "Select Currency",
            options=["USD", "BDT"],
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
                "Last 3 Months",
                "Last 6 Months",
                "Last Year",
                "Custom Range"
            ],
            index=0
        )
        
        # Calculate date ranges based on selection
        if date_range_option == "Last 7 Days":
            date_range = (max_date - pd.Timedelta(days=7), max_date)
        elif date_range_option == "Last 14 Days":
            date_range = (max_date - pd.Timedelta(days=14), max_date)
        elif date_range_option == "Last 30 Days":
            date_range = (max_date - pd.Timedelta(days=30), max_date)
        elif date_range_option == "Last 3 Months":
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

    st.markdown('<h1 style="text-align: center; color: black;">Mr. Life Okey Clothing Brand Dashboard</h1>', unsafe_allow_html=True)

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

    # Display all charts
    show_metrics_chart(metrics_data, create_text_container(TEXT_CONFIG['metrics']['title'], TEXT_CONFIG['metrics']['content']))
    show_order_source_and_top_products(order_data, product_data, metrics_data['currency_symbol'], create_text_container(TEXT_CONFIG['order_analysis']['title'], TEXT_CONFIG['order_analysis']['content']))
    show_inventory_analysis(inventory_data, metrics_data['currency_symbol'], create_text_container(TEXT_CONFIG['inventory']['title'], TEXT_CONFIG['inventory']['content']))
    show_category_analysis(category_data, metrics_data['currency_symbol'], create_text_container(TEXT_CONFIG['category']['title'], TEXT_CONFIG['category']['content']))
    show_profitability_analysis(profit_data, metrics_data['currency_symbol'], create_text_container(TEXT_CONFIG['profitability']['title'], TEXT_CONFIG['profitability']['content']))
    show_line_chart(sales_data, metrics_data['currency_symbol'], create_text_container(TEXT_CONFIG['sales_trend']['title'], TEXT_CONFIG['sales_trend']['content']))
    show_customer_insights(customer_data, metrics_data['currency_symbol'], create_text_container(TEXT_CONFIG['customer_insights']['title'], TEXT_CONFIG['customer_insights']['content']))
    show_customer_growth_and_avg_order_value(monthly_data, metrics_data['currency_symbol'], create_text_container(TEXT_CONFIG['growth']['title'], TEXT_CONFIG['growth']['content']))

if __name__ == '__main__':
    main()