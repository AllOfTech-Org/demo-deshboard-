import pandas as pd
import numpy as np
from github import Github
import os
import base64
import io

class DashboardDataProcessor:
    def __init__(self, repo_name='client-dashboards-data', file_path='data/Your Company/dashboard_data.csv'):
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        if not GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN not found in environment variables.")
        
        g = Github(GITHUB_TOKEN)
        user = g.get_user()
        repo = user.get_repo(repo_name)
        
        try:
            file_content = repo.get_contents(file_path)
            decoded = base64.b64decode(file_content.content)
            decoded_str = decoded.decode('utf-8', errors='ignore')
            
            if not decoded_str.strip():
                raise FileNotFoundError("Uploaded file is empty.")
            
            self.df = pd.read_csv(io.StringIO(decoded_str))
            
        except Exception as e:
            raise FileNotFoundError(f"Failed to load file from GitHub: {str(e)}")
        
        self.df['date'] = pd.to_datetime(self.df.get('date', pd.Series([], dtype='datetime64[ns]')))
        self.currency = 'USD'
        self.currency_symbol = '$'
        self.exchange_rates = {'USD': 1.0, 'BDT': 110.0}
        self.filtered_df = self.df.copy()

    def set_currency(self, currency):
        self.currency = currency
        self.currency_symbol = {
            'USD': '$',
            'BDT': '৳'
        }.get(currency, '$')

    def convert_amount(self, amount):
        return amount * self.exchange_rates.get(self.currency, 1)

    def apply_filters(self, date_range=None, categories=None):
        self.filtered_df = self.df.copy()

        if date_range:
            start_date, end_date = date_range
            self.filtered_df = self.filtered_df[
                (self.filtered_df['date'] >= pd.to_datetime(start_date)) & 
                (self.filtered_df['date'] <= pd.to_datetime(end_date))
            ]
            
        if categories and 'category' in self.df.columns:
            self.filtered_df = self.filtered_df[self.filtered_df['category'].isin(categories)]
    
    def get_metrics_data(self):
        latest_date = self.filtered_df['date'].max()
        latest_data = self.filtered_df[self.filtered_df['date'] == latest_date].iloc[0]

        total_sales = self.convert_amount(self.filtered_df['sales'].sum())
        avg_daily_sales = self.convert_amount(self.filtered_df['sales'].mean())
        total_customers = self.filtered_df.get('new_customers', pd.Series([])).sum()
        return_rate = (self.filtered_df['returns'].sum() / self.filtered_df['sales'].sum()) * 100 if 'returns' in self.df.columns else 0

        current_period = self.filtered_df[self.filtered_df['date'] >= (latest_date - pd.Timedelta(days=30))]
        previous_period = self.filtered_df[
            (self.filtered_df['date'] >= (latest_date - pd.Timedelta(days=60))) & 
            (self.filtered_df['date'] < (latest_date - pd.Timedelta(days=30)))
        ]

        sales_growth = ((current_period['sales'].sum() - previous_period['sales'].sum()) / previous_period['sales'].sum()) * 100 if len(previous_period) > 0 else 0
        daily_sales_growth = ((current_period['sales'].mean() - previous_period['sales'].mean()) / previous_period['sales'].mean()) * 100 if len(previous_period) > 0 else 0
        customer_growth = ((current_period['new_customers'].sum() - previous_period['new_customers'].sum()) / previous_period['new_customers'].sum()) * 100 if len(previous_period) > 0 else 0

        return {
            'total_sales': total_sales,
            'avg_daily_sales': avg_daily_sales,
            'total_customers': total_customers,
            'return_rate': return_rate,
            'sales_growth': round(sales_growth, 1),
            'daily_sales_growth': round(daily_sales_growth, 1),
            'customer_growth': round(customer_growth, 1),
            'currency_symbol': self.currency_symbol
        }
    
    def get_sales_trend_data(self):
        daily_data = self.filtered_df.groupby('date').agg({
            'sales': 'sum',
            'returns': 'sum'
        }).reset_index()

        daily_data['sales'] = daily_data['sales'].apply(self.convert_amount)
        daily_data['returns'] = daily_data['returns'].apply(self.convert_amount)

        return daily_data
    
    def get_category_data(self):
        category_data = self.filtered_df.groupby('category').agg({
            'sales': 'sum',
            'inventory': 'mean',
            'profit_margin': 'mean',
            'profit': 'sum'
        }).reset_index()

        category_data['sales'] = category_data['sales'].apply(self.convert_amount)
        category_data['profit'] = category_data['profit'].apply(self.convert_amount)

        return category_data

    def get_product_data(self):
        product_data = self.filtered_df.groupby('product_id').agg({
            'sales': 'sum',
            'category': 'first'
        }).reset_index()

        product_data['sales'] = product_data['sales'].apply(self.convert_amount)
        top_products = product_data.sort_values('sales', ascending=False).head(10)

        return top_products

    
    def get_category_data(self):
        """Prepare data for category analysis"""
        # Group by category and calculate metrics
        category_data = self.filtered_df.groupby('category').agg({
            'sales': 'sum',
            'inventory': 'mean',
            'profit_margin': 'mean',
            'profit': 'sum'
        }).reset_index()
        
        # Convert sales and profit to selected currency
        category_data['sales'] = category_data['sales'].apply(self.convert_amount)
        category_data['profit'] = category_data['profit'].apply(self.convert_amount)
        
        return category_data
    
    def get_inventory_data(self):
        """Prepare data for inventory analysis"""
        # Use the same category data but with additional inventory metrics
        inventory_data = self.filtered_df.groupby('category').agg({
            'inventory': 'mean',
            'sales': 'sum',
            'profit_margin': 'mean'
        }).reset_index()
        
        # Convert sales to selected currency
        inventory_data['sales'] = inventory_data['sales'].apply(self.convert_amount)
        
        return inventory_data
    
    def get_customer_growth_data(self):
        """Prepare data for customer growth analysis"""
        # Group by month and calculate metrics
        monthly_data = self.filtered_df.groupby('month').agg({
            'new_customers': 'sum',
            'sales': 'sum',
            'avg_order_value': 'mean'
        }).reset_index()
        
        # Convert sales and avg_order_value to selected currency
        monthly_data['sales'] = monthly_data['sales'].apply(self.convert_amount)
        monthly_data['avg_order_value'] = monthly_data['avg_order_value'].apply(self.convert_amount)
        
        return monthly_data
    
    def get_profitability_data(self):
        """Prepare data for profitability analysis"""
        # Group by category and calculate profit metrics
        profit_data = self.filtered_df.groupby('category').agg({
            'sales': 'sum',
            'profit': 'sum',
            'profit_margin': 'mean'
        }).reset_index()
        
        # Convert sales and profit to selected currency
        profit_data['sales'] = profit_data['sales'].apply(self.convert_amount)
        profit_data['profit'] = profit_data['profit'].apply(self.convert_amount)
        
        return profit_data
    
    def get_customer_insights_data(self):
        """Prepare data for customer insights"""
        # Group by month and calculate customer metrics
        customer_data = self.filtered_df.groupby('month').agg({
            'new_customers': 'sum',
            'avg_order_value': 'mean'
        }).reset_index()
        
        # Convert avg_order_value to selected currency
        customer_data['avg_order_value'] = customer_data['avg_order_value'].apply(self.convert_amount)
        
        return customer_data

# Example usage
if __name__ == "__main__":
    processor = DashboardDataProcessor()
    
    # Test each data preparation method
    print("Metrics Data:", processor.get_metrics_data())
    print("\nSales Trend Data Shape:", processor.get_sales_trend_data().shape)
    print("\nOrder Source Data Shape:", processor.get_order_source_data().shape)
    print("\nProduct Data Shape:", processor.get_product_data().shape)
    print("\nCategory Data Shape:", processor.get_category_data().shape)
    print("\nInventory Data Shape:", processor.get_inventory_data().shape)
    print("\nCustomer Growth Data Shape:", processor.get_customer_growth_data().shape)
    print("\nProfitability Data Shape:", processor.get_profitability_data().shape)
    print("\nCustomer Insights Data Shape:", processor.get_customer_insights_data().shape) 