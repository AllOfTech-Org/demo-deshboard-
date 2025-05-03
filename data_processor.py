import pandas as pd
import numpy as np
from github import Github
import os
import base64
import io
import requests
from io import StringIO
import streamlit as st

token = st.secrets["DATA_TOKEN"]
class DashboardDataProcessor:
    def __init__(self, folder_name='Your_Company'):
        folder_url = f'https://api.github.com/repos/AllOfTech-Org/client-dashboards-data/contents/data/{folder_name}'

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.get(folder_url, headers=headers)
        if response.status_code != 200:
            raise Exception("Failed to fetch folder content")

        file_list = response.json()

        all_dataframes = []

        for file in file_list:
            if file['name'].endswith('.csv'):
                file_url = file['download_url']
                csv_response = requests.get(file_url, headers=headers)
                if csv_response.status_code == 200:
                    csv_content = StringIO(csv_response.text)
                    df = pd.read_csv(csv_content)
                    all_dataframes.append(df)
                else:
                    print(f"Failed to fetch: {file['name']}")

        if not all_dataframes:
            raise Exception("No CSV files found in the GitHub folder.")

        self.df = pd.concat(all_dataframes, ignore_index=True)

        # Convert 'date' column to datetime if it exists
        self.df['date'] = pd.to_datetime(self.df.get('date', pd.Series([], dtype='datetime64[ns]')))
        self.currency = 'USD'
        self.currency_symbol = '$'
        self.exchange_rates = {'USD': 1.0, 'BDT': 110.0}
        self.filtered_df = self.df.copy()



    def set_currency(self, currency):
        self.currency = currency
        self.currency_symbol = {'USD': '$', 'BDT': '৳'}.get(currency, '$')

    def convert_amount(self, amount):
        return amount * self.exchange_rates.get(self.currency, 1)

    def apply_filters(self, date_range=None, categories=None):
        self.filtered_df = self.df.copy()
        if date_range:
            start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
            self.filtered_df = self.filtered_df[(self.filtered_df['date'] >= start) & (self.filtered_df['date'] <= end)]
        if categories and 'category' in self.filtered_df.columns:
            self.filtered_df = self.filtered_df[self.filtered_df['category'].isin(categories)]

    def get_metrics_data(self):
        latest_date = self.filtered_df['date'].max()
        total_sales = self.convert_amount(self.filtered_df['sales'].sum())
        avg_daily_sales = self.convert_amount(self.filtered_df['sales'].mean())
        total_customers = self.filtered_df['new_customers'].sum()
        return_rate = (self.filtered_df['returns'].sum() / self.filtered_df['sales'].sum()) * 100 if self.filtered_df['sales'].sum() > 0 else 0

        current = self.filtered_df[self.filtered_df['date'] >= latest_date - pd.Timedelta(days=30)]
        previous = self.filtered_df[(self.filtered_df['date'] >= latest_date - pd.Timedelta(days=60)) & (self.filtered_df['date'] < latest_date - pd.Timedelta(days=30))]

        def safe_growth(curr, prev):
            return ((curr - prev) / prev) * 100 if prev else 0

        current_return_rate = (current['returns'].sum() / current['sales'].sum()) * 100 if current['sales'].sum() > 0 else 0
        previous_return_rate = (previous['returns'].sum() / previous['sales'].sum()) * 100 if previous['sales'].sum() > 0 else 0
        return_rate_change = safe_growth(current_return_rate, previous_return_rate)

        return {
            'total_sales': total_sales,
            'avg_daily_sales': avg_daily_sales,
            'total_customers': total_customers,
            'return_rate': round(return_rate, 2),
            'return_rate_change': round(return_rate_change, 2),
            'sales_growth': round(safe_growth(current['sales'].sum(), previous['sales'].sum()), 1),
            'daily_sales_growth': round(safe_growth(current['sales'].mean(), previous['sales'].mean()), 1),
            'customer_growth': round(safe_growth(current['new_customers'].sum(), previous['new_customers'].sum()), 1),
            'currency_symbol': self.currency_symbol
        }

    def get_sales_trend_data(self):
        daily = self.filtered_df.groupby('date')[['sales', 'returns']].sum().reset_index()
        daily['sales'] = daily['sales'].apply(self.convert_amount)
        daily['returns'] = daily['returns'].apply(self.convert_amount)
        return daily

    def get_order_source_data(self):
        order_source_data = self.filtered_df.groupby('order_source').agg({'sales': 'sum'}).reset_index()
        order_source_data['sales'] = order_source_data['sales'].apply(self.convert_amount)
        return order_source_data

    def get_product_data(self):
        product_data = self.filtered_df.groupby('product_id').agg({'sales': 'sum', 'category': 'first'}).reset_index()
        product_data['sales'] = product_data['sales'].apply(self.convert_amount)
        return product_data.sort_values('sales', ascending=False).head(10)

    def get_category_data(self):
        cat = self.filtered_df.groupby('category').agg({
            'sales': 'sum', 'inventory': 'mean', 'profit_margin': 'mean', 'profit': 'sum'
        }).reset_index()
        cat['sales'] = cat['sales'].apply(self.convert_amount)
        cat['profit'] = cat['profit'].apply(self.convert_amount)
        return cat

    def get_inventory_data(self):
        inv = self.filtered_df.groupby('category').agg({
            'inventory': 'mean', 'sales': 'sum', 'profit_margin': 'mean'
        }).reset_index()
        inv['sales'] = inv['sales'].apply(self.convert_amount)
        return inv

    def get_customer_growth_data(self):
        df = self.filtered_df.groupby('month').agg({
            'new_customers': 'sum', 'sales': 'sum', 'avg_order_value': 'mean'
        }).reset_index()
        df['sales'] = df['sales'].apply(self.convert_amount)
        df['avg_order_value'] = df['avg_order_value'].apply(self.convert_amount)
        return df

    def get_profitability_data(self):
        df = self.filtered_df.groupby('category').agg({
            'sales': 'sum', 'profit': 'sum', 'profit_margin': 'mean'
        }).reset_index()
        df['sales'] = df['sales'].apply(self.convert_amount)
        df['profit'] = df['profit'].apply(self.convert_amount)
        return df

    def get_customer_insights_data(self):
        df = self.filtered_df.groupby('month').agg({
            'new_customers': 'sum', 'avg_order_value': 'mean'
        }).reset_index()
        df['avg_order_value'] = df['avg_order_value'].apply(self.convert_amount)
        return df

# Example usage
if __name__ == "__main__":
    processor = DashboardDataProcessor()
    print("Metrics Data:", processor.get_metrics_data())
    print("\nSales Trend:", processor.get_sales_trend_data().head())
    print("\nOrder Source:", processor.get_order_source_data().head())
    print("\nTop Products:", processor.get_product_data().head())
    print("\nCategories:", processor.get_category_data().head())
    print("\nInventory Info:", processor.get_inventory_data().head())
    print("\nCustomer Growth:", processor.get_customer_growth_data().head())
    print("\nProfitability:", processor.get_profitability_data().head())
    print("\nCustomer Insights:", processor.get_customer_insights_data().head())
    print(processor.df.shape)
