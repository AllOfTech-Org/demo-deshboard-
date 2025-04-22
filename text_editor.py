import streamlit as st
import json
import os
import re

def load_text_config():
    """Load the current text configuration from dashboard.py"""
    try:
        with open('dashboard.py', 'r', encoding='utf-8') as file:
            content = file.read()
            # Find the TEXT_CONFIG section
            start = content.find('TEXT_CONFIG = {')
            if start == -1:
                return {}
            
            # Use regex to find the complete dictionary including nested braces
            # This is more reliable than simple string finding
            text_config_pattern = r'TEXT_CONFIG = \{.*?\}(?=\n\n)'
            match = re.search(text_config_pattern, content, re.DOTALL)
            if not match:
                return {}
                
            # Extract the dictionary string
            config_str = match.group(0)[len('TEXT_CONFIG = '):]
            
            # Convert the string to a dictionary using safer eval
            config = eval(config_str)
            return config
    except Exception as e:
        st.error(f"Error loading text configuration: {str(e)}")
        return {}

def save_text_config(config):
    """Save the text configuration back to dashboard.py"""
    try:
        with open('dashboard.py', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Use regex to find the complete dictionary with correct handling of nested braces
        text_config_pattern = r'TEXT_CONFIG = \{.*?\}(?=\n\n)'
        match = re.search(text_config_pattern, content, re.DOTALL)
        
        if not match:
            st.error("Could not find TEXT_CONFIG in dashboard.py")
            return
        
        # Create the new configuration string with proper formatting
        new_config = "TEXT_CONFIG = {\n"
        for key, value in config.items():
            # Escape any quotes in the content
            title = value["title"].replace('"', '\\"')
            content_text = value["content"].replace('"', '\\"')
            
            new_config += f'    "{key}": {{\n'
            new_config += f'        "title": "{title}",\n'
            new_config += f'        "content": "{content_text}"\n'
            new_config += '    },\n'
        new_config = new_config.rstrip(',\n') + '\n}'
        
        # Replace the entire TEXT_CONFIG section with the new content
        new_content = re.sub(text_config_pattern, new_config, content, flags=re.DOTALL)
        
        # Save the changes
        with open('dashboard.py', 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        st.success("Text configuration saved successfully!")
        
        # Auto-refresh the page to show changes
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Error saving text configuration: {str(e)}")

def main():
    st.title("Dashboard Text Editor")
    st.write("Edit the text content for your dashboard sections below. Changes will be saved automatically.")
    
    # Load current configuration
    config = load_text_config()
    
    # Create a form for editing
    with st.form("text_editor_form"):
        # Metrics Section
        st.subheader("Metrics Section")
        metrics_title = st.text_input("Metrics Title", value=config.get('metrics', {}).get('title', ''), key='metrics_title')
        metrics_content = st.text_area("Metrics Content", value=config.get('metrics', {}).get('content', ''), key='metrics_content')
        
        # Sales Trend Section
        st.subheader("Sales Trend Section")
        sales_trend_title = st.text_input("Sales Trend Title", value=config.get('sales_trend', {}).get('title', ''), key='sales_trend_title')
        sales_trend_content = st.text_area("Sales Trend Content", value=config.get('sales_trend', {}).get('content', ''), key='sales_trend_content')
        
        # Order Analysis Section
        st.subheader("Order Analysis Section")
        order_analysis_title = st.text_input("Order Analysis Title", value=config.get('order_analysis', {}).get('title', ''), key='order_analysis_title')
        order_analysis_content = st.text_area("Order Analysis Content", value=config.get('order_analysis', {}).get('content', ''), key='order_analysis_content')
        
        # Inventory Section
        st.subheader("Inventory Section")
        inventory_title = st.text_input("Inventory Title", value=config.get('inventory', {}).get('title', ''), key='inventory_title')
        inventory_content = st.text_area("Inventory Content", value=config.get('inventory', {}).get('content', ''), key='inventory_content')
        
        # Category Section
        st.subheader("Category Section")
        category_title = st.text_input("Category Title", value=config.get('category', {}).get('title', ''), key='category_title')
        category_content = st.text_area("Category Content", value=config.get('category', {}).get('content', ''), key='category_content')
        
        # Profitability Section
        st.subheader("Profitability Section")
        profitability_title = st.text_input("Profitability Title", value=config.get('profitability', {}).get('title', ''), key='profitability_title')
        profitability_content = st.text_area("Profitability Content", value=config.get('profitability', {}).get('content', ''), key='profitability_content')
        
        # Customer Insights Section
        st.subheader("Customer Insights Section")
        customer_insights_title = st.text_input("Customer Insights Title", value=config.get('customer_insights', {}).get('title', ''), key='customer_insights_title')
        customer_insights_content = st.text_area("Customer Insights Content", value=config.get('customer_insights', {}).get('content', ''), key='customer_insights_content')
        
        # Growth Section
        st.subheader("Growth Section")
        growth_title = st.text_input("Growth Title", value=config.get('growth', {}).get('title', ''), key='growth_title')
        growth_content = st.text_area("Growth Content", value=config.get('growth', {}).get('content', ''), key='growth_content')
        
        # Submit button
        if st.form_submit_button("Save Changes"):
            # Create new configuration
            new_config = {
                'metrics': {'title': metrics_title, 'content': metrics_content},
                'sales_trend': {'title': sales_trend_title, 'content': sales_trend_content},
                'order_analysis': {'title': order_analysis_title, 'content': order_analysis_content},
                'inventory': {'title': inventory_title, 'content': inventory_content},
                'category': {'title': category_title, 'content': category_content},
                'profitability': {'title': profitability_title, 'content': profitability_content},
                'customer_insights': {'title': customer_insights_title, 'content': customer_insights_content},
                'growth': {'title': growth_title, 'content': growth_content}
            }
            
            # Save the changes
            save_text_config(new_config)

if __name__ == "__main__":
    main() 