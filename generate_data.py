import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

# Define the date range
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date)

# Define categories and their profit margins
categories = {
    'Jeans': 0.35,
    'Shirts': 0.25,
    'T-Shirts': 0.30,
    'Jackets': 0.40,
    'Accessories': 0.45
}

# Define order sources
order_sources = ['Website', 'Instagram', 'Facebook', 'Direct', 'Other']

# Generate product IDs
product_ids = [
    'Drop Shoulder T-shirt',
    'Baggy Pants',
    'Polo Shirt',
    'Full-Sleeve Shirt',
    'Half-Sleeve Shirt',
    'Watch',
    'Sneakers',
    'Trousers',
    'Baggy Trousers',
    'Oversized Hoodie',
    'Slim Fit Jeans',
    'Denim Jacket',
    'Leather Jacket',
    'Loafers',
    'Sweatshirt',
    'Crop Top',
    'Tank Top',
    'Graphic Tee',
    'Cargo Pants',
    'Joggers'
]

# Function to generate realistic sales data
def generate_sales_data(n_rows=10000):
    data = []
    
    for _ in range(n_rows):
        # Generate random date
        date = random.choice(date_range)
        
        # Generate random category and get its profit margin
        category = random.choice(list(categories.keys()))
        profit_margin = categories[category]
        
        # Generate sales amount (between 500 and 2000)
        sales = np.random.uniform(500, 2000)
        
        # Generate return rate (between 5% and 15%)
        return_rate = np.random.uniform(5, 15)
        returns = sales * (return_rate / 100)
        
        # Generate number of new customers (between 5 and 35)
        new_customers = np.random.randint(5, 36)
        
        # Calculate average order value
        avg_order_value = sales / new_customers if new_customers > 0 else sales
        
        # Generate random order source
        order_source = random.choice(order_sources)
        
        # Generate random product ID
        product_id = random.choice(product_ids)
        
        # Generate inventory (between 50 and 500)
        inventory = np.random.randint(50, 501)
        
        # Calculate profit
        profit = sales * profit_margin
        
        # Create row
        row = {
            'date': date.strftime('%Y-%m-%d'),
            'sales': round(sales, 2),
            'returns': round(returns, 2),
            'return_rate': round(return_rate, 2),
            'new_customers': new_customers,
            'avg_order_value': round(avg_order_value, 2),
            'order_source': order_source,
            'category': category,
            'product_id': product_id,
            'inventory': inventory,
            'profit_margin': profit_margin,
            'profit': round(profit, 2),
            'month': date.strftime('%Y-%m')
        }
        
        data.append(row)
    
    return pd.DataFrame(data)

# Generate the data
df = generate_sales_data(10000)

# Save to CSV
df.to_csv('data/dashboard_data.csv', index=False)
print("Generated 10,000 rows of data and saved to data/dashboard_data.csv") 