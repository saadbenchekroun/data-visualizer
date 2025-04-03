import pandas as pd
import random
import datetime
import json

def get_available_integrations():
    """
    Get list of available external tool integrations
    
    Returns:
        list: List of integration objects
    """
    integrations = [
        {
            'id': 'quickbooks',
            'name': 'QuickBooks',
            'description': 'Import financial data from QuickBooks accounting software',
            'icon': 'money-bill-wave',
            'auth_type': 'oauth',
            'required_fields': ['oauth_token'],
            'setup_instructions': 'Connect to QuickBooks to import your financial data for visualization.',
            'config_fields': [
                {
                    'id': 'company_id',
                    'label': 'Company ID',
                    'type': 'text',
                    'placeholder': 'Enter your QuickBooks Company ID'
                },
                {
                    'id': 'date_range',
                    'label': 'Default date range',
                    'type': 'select',
                    'options': ['Last month', 'Last quarter', 'Last year', 'All time']
                }
            ]
        },
        {
            'id': 'shopify',
            'name': 'Shopify',
            'description': 'Import e-commerce data from your Shopify store',
            'icon': 'shopping-cart',
            'auth_type': 'api_key',
            'required_fields': ['api_key', 'shop_name'],
            'setup_instructions': 'Connect to Shopify to import your sales, product, and customer data.',
            'config_fields': [
                {
                    'id': 'shop_name',
                    'label': 'Shop Name',
                    'type': 'text',
                    'placeholder': 'your-shop-name.myshopify.com'
                },
                {
                    'id': 'data_types',
                    'label': 'Data to import',
                    'type': 'select',
                    'options': ['Orders only', 'Orders and customers', 'All data']
                }
            ]
        },
        {
            'id': 'google_analytics',
            'name': 'Google Analytics',
            'description': 'Import website analytics data from Google Analytics',
            'icon': 'chart-line',
            'auth_type': 'oauth',
            'required_fields': ['oauth_token'],
            'setup_instructions': 'Connect to Google Analytics to import your website traffic and user behavior data.',
            'config_fields': [
                {
                    'id': 'view_id',
                    'label': 'View ID',
                    'type': 'text',
                    'placeholder': 'Enter your Google Analytics View ID'
                },
                {
                    'id': 'metrics',
                    'label': 'Default metrics',
                    'type': 'select',
                    'options': ['Page views', 'Sessions', 'Users', 'All basic metrics']
                }
            ]
        },
        {
            'id': 'salesforce',
            'name': 'Salesforce',
            'description': 'Import CRM data from Salesforce',
            'icon': 'cloud',
            'auth_type': 'oauth',
            'required_fields': ['oauth_token'],
            'setup_instructions': 'Connect to Salesforce to import your customer, opportunity, and sales data.',
            'config_fields': [
                {
                    'id': 'instance_url',
                    'label': 'Salesforce Instance URL',
                    'type': 'text',
                    'placeholder': 'https://yourinstance.salesforce.com'
                }
            ]
        },
        {
            'id': 'mailchimp',
            'name': 'Mailchimp',
            'description': 'Import email marketing data from Mailchimp',
            'icon': 'envelope',
            'auth_type': 'api_key',
            'required_fields': ['api_key'],
            'setup_instructions': 'Connect to Mailchimp to import your email campaign and subscriber data.',
            'config_fields': [
                {
                    'id': 'list_id',
                    'label': 'Default List/Audience ID',
                    'type': 'text',
                    'placeholder': 'Enter your main Mailchimp list ID'
                }
            ]
        },
        {
            'id': 'google_sheets',
            'name': 'Google Sheets',
            'description': 'Import data from Google Sheets spreadsheets',
            'icon': 'table',
            'auth_type': 'oauth',
            'required_fields': ['oauth_token'],
            'setup_instructions': 'Connect to Google Sheets to import data from your spreadsheets.',
            'config_fields': [
                {
                    'id': 'sheet_id',
                    'label': 'Spreadsheet ID',
                    'type': 'text',
                    'placeholder': 'Enter the ID from your spreadsheet URL'
                },
                {
                    'id': 'sheet_range',
                    'label': 'Cell Range (optional)',
                    'type': 'text',
                    'placeholder': 'e.g., Sheet1!A1:E100'
                }
            ]
        }
    ]
    
    return integrations

def setup_integration(integration_id, auth_fields):
    """
    Set up an integration with the provided authentication fields
    
    Args:
        integration_id (str): ID of the integration to set up
        auth_fields (dict): Authentication fields for the integration
        
    Returns:
        dict: Setup result with success flag and message
    """
    # This would be implemented to actually authenticate with the service
    # For the demo, we'll simulate a successful setup
    return {
        'success': True,
        'message': 'Integration set up successfully',
        'integration_id': integration_id
    }

def get_integration_data(integration_id, connection_info, data_type=None, start_date=None, end_date=None):
    """
    Retrieve data from an external integration
    
    Args:
        integration_id (str): ID of the integration to get data from
        connection_info (dict): Connection information for the integration
        data_type (str, optional): Specific type of data to retrieve
        start_date (datetime, optional): Start date for the data range
        end_date (datetime, optional): End date for the data range
        
    Returns:
        dict: Data from the integration or error message
    """
    # This would be implemented to actually fetch data from the service
    # For the demo, we'll generate mock data based on the integration and data type
    
    # Set default dates if not provided
    if not start_date:
        start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    if not end_date:
        end_date = datetime.datetime.now()
    
    # Generate date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # QuickBooks data
    if integration_id == 'quickbooks':
        if data_type == "Profit & Loss":
            # Generate P&L statement data
            data = []
            categories = ["Sales", "Cost of Goods Sold", "Operating Expenses", "Marketing", "Rent", "Utilities", "Salaries"]
            
            for date in date_range:
                for category in categories:
                    # Generate sensible values based on category
                    if category == "Sales":
                        amount = random.uniform(1000, 5000)
                    elif category == "Cost of Goods Sold":
                        amount = random.uniform(500, 2000)
                    else:
                        amount = random.uniform(100, 1000)
                    
                    data.append({
                        "Date": date.strftime("%Y-%m-%d"),
                        "Category": category,
                        "Amount": round(amount, 2),
                        "Department": random.choice(["Sales", "Marketing", "Operations", "Admin"])
                    })
            
            return {
                'filename': 'quickbooks_profit_loss.csv',
                'data': data
            }
            
        elif data_type == "Balance Sheet":
            # Generate balance sheet data
            data = []
            asset_categories = ["Cash", "Accounts Receivable", "Inventory", "Equipment", "Real Estate"]
            liability_categories = ["Accounts Payable", "Short-term Loans", "Long-term Debt", "Taxes Payable"]
            equity_categories = ["Owner's Equity", "Retained Earnings"]
            
            for date in date_range[::7]:  # Weekly snapshots
                for category in asset_categories + liability_categories + equity_categories:
                    # Generate type based on category
                    if category in asset_categories:
                        type = "Asset"
                        amount = random.uniform(5000, 100000)
                    elif category in liability_categories:
                        type = "Liability"
                        amount = random.uniform(1000, 50000)
                    else:
                        type = "Equity"
                        amount = random.uniform(10000, 200000)
                    
                    data.append({
                        "Date": date.strftime("%Y-%m-%d"),
                        "Category": category,
                        "Type": type,
                        "Amount": round(amount, 2)
                    })
            
            return {
                'filename': 'quickbooks_balance_sheet.csv',
                'data': data
            }
            
        elif data_type == "Invoices":
            # Generate invoice data
            data = []
            customers = ["Customer A", "Customer B", "Customer C", "Customer D", "Customer E"]
            statuses = ["Paid", "Unpaid", "Overdue", "Partially Paid"]
            
            for i in range(100):
                invoice_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
                due_date = invoice_date + datetime.timedelta(days=30)
                amount = random.uniform(100, 5000)
                paid_amount = amount if random.random() > 0.3 else random.uniform(0, amount)
                
                data.append({
                    "Invoice_Number": f"INV-{1000+i}",
                    "Customer": random.choice(customers),
                    "Invoice_Date": invoice_date.strftime("%Y-%m-%d"),
                    "Due_Date": due_date.strftime("%Y-%m-%d"),
                    "Amount": round(amount, 2),
                    "Paid_Amount": round(paid_amount, 2),
                    "Status": "Paid" if paid_amount >= amount else "Unpaid" if paid_amount == 0 else "Partially Paid",
                    "Days_Outstanding": (datetime.datetime.now() - invoice_date).days
                })
            
            return {
                'filename': 'quickbooks_invoices.csv',
                'data': data
            }
        
        else:
            # Default financial data
            data = []
            categories = ["Revenue", "Expenses", "Profit"]
            
            for date in date_range:
                revenue = random.uniform(1000, 5000)
                expenses = random.uniform(500, 3000)
                profit = revenue - expenses
                
                for category in categories:
                    value = revenue if category == "Revenue" else expenses if category == "Expenses" else profit
                    data.append({
                        "Date": date.strftime("%Y-%m-%d"),
                        "Category": category,
                        "Amount": round(value, 2)
                    })
            
            return {
                'filename': 'quickbooks_financial_data.csv',
                'data': data
            }
    
    # Shopify data
    elif integration_id == 'shopify':
        if data_type == "Orders":
            # Generate order data
            data = []
            products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
            payment_methods = ["Credit Card", "PayPal", "Shop Pay", "Apple Pay", "Google Pay"]
            
            for i in range(200):
                order_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
                num_items = random.randint(1, 5)
                item_price = random.uniform(10, 100)
                total = num_items * item_price
                discount = total * random.uniform(0, 0.2) if random.random() > 0.7 else 0
                
                data.append({
                    "Order_ID": f"ORD-{10000+i}",
                    "Date": order_date.strftime("%Y-%m-%d"),
                    "Customer_Email": f"customer{i}@example.com",
                    "Product": random.choice(products),
                    "Quantity": num_items,
                    "Price_Per_Item": round(item_price, 2),
                    "Discount": round(discount, 2),
                    "Total": round(total - discount, 2),
                    "Payment_Method": random.choice(payment_methods),
                    "Status": random.choice(["Fulfilled", "Unfulfilled", "Cancelled"]) if random.random() > 0.8 else "Fulfilled"
                })
            
            return {
                'filename': 'shopify_orders.csv',
                'data': data
            }
            
        elif data_type == "Products":
            # Generate product data
            data = []
            categories = ["Clothing", "Electronics", "Home Goods", "Beauty", "Food"]
            
            for i in range(50):
                data.append({
                    "Product_ID": f"PROD-{1000+i}",
                    "Product_Name": f"Product {chr(65+i%26)}{i//26}",
                    "Category": random.choice(categories),
                    "Price": round(random.uniform(10, 200), 2),
                    "Cost": round(random.uniform(5, 100), 2),
                    "Inventory_Quantity": random.randint(0, 100),
                    "Published": random.choice([True, False]) if random.random() > 0.9 else True
                })
            
            return {
                'filename': 'shopify_products.csv',
                'data': data
            }
            
        elif data_type == "Customers":
            # Generate customer data
            data = []
            locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego"]
            
            for i in range(100):
                signup_date = start_date + datetime.timedelta(days=random.randint(-365, (end_date - start_date).days))
                orders_count = random.randint(0, 20)
                
                data.append({
                    "Customer_ID": f"CUST-{1000+i}",
                    "Email": f"customer{i}@example.com",
                    "First_Name": f"First{i}",
                    "Last_Name": f"Last{i}",
                    "City": random.choice(locations),
                    "Signup_Date": signup_date.strftime("%Y-%m-%d"),
                    "Orders_Count": orders_count,
                    "Total_Spent": round(orders_count * random.uniform(50, 200), 2),
                    "Last_Order_Date": (signup_date + datetime.timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d") if orders_count > 0 else None
                })
            
            return {
                'filename': 'shopify_customers.csv',
                'data': data
            }
        
        else:
            # Default to sales data
            data = []
            
            for date in date_range:
                daily_orders = random.randint(5, 30)
                avg_order_value = random.uniform(50, 200)
                
                data.append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Orders": daily_orders,
                    "Sales": round(daily_orders * avg_order_value, 2),
                    "Customers": random.randint(daily_orders, daily_orders + 10),
                    "Refunds": round(daily_orders * random.uniform(0, 0.1)),
                    "Discount_Amount": round(daily_orders * avg_order_value * random.uniform(0, 0.2), 2)
                })
            
            return {
                'filename': 'shopify_sales_data.csv',
                'data': data
            }
    
    # Google Analytics data
    elif integration_id == 'google_analytics':
        if data_type == "Website Traffic":
            # Generate website traffic data
            data = []
            
            for date in date_range:
                traffic_multiplier = 1 + 0.5 * math.sin(date.day_of_year * 0.1)  # Create some seasonality
                
                data.append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Sessions": int(random.uniform(500, 2000) * traffic_multiplier),
                    "Users": int(random.uniform(400, 1500) * traffic_multiplier),
                    "Pageviews": int(random.uniform(1000, 5000) * traffic_multiplier),
                    "Bounce_Rate": round(random.uniform(0.2, 0.6), 2),
                    "Avg_Session_Duration": round(random.uniform(60, 360), 2),
                    "Pages_Per_Session": round(random.uniform(1.5, 4.5), 2)
                })
            
            return {
                'filename': 'google_analytics_traffic.csv',
                'data': data
            }
            
        elif data_type == "Referrers":
            # Generate referral source data
            data = []
            referrers = ["Google", "Facebook", "Twitter", "Instagram", "LinkedIn", "Direct", "Email", "Other"]
            
            for date in date_range[::3]:  # Every third day
                for referrer in referrers:
                    sessions = random.randint(10, 500)
                    bounce_rate = random.uniform(0.2, 0.8)
                    
                    data.append({
                        "Date": date.strftime("%Y-%m-%d"),
                        "Source": referrer,
                        "Sessions": sessions,
                        "New_Users": int(sessions * random.uniform(0.5, 0.9)),
                        "Bounce_Rate": round(bounce_rate, 2),
                        "Avg_Session_Duration": round(random.uniform(30, 300), 2),
                        "Conversions": int(sessions * (1 - bounce_rate) * random.uniform(0.01, 0.2))
                    })
            
            return {
                'filename': 'google_analytics_referrers.csv',
                'data': data
            }
        
        else:
            # Default to page performance
            data = []
            pages = ["/home", "/products", "/about", "/contact", "/blog", "/cart", "/checkout"]
            
            for page in pages:
                views = random.randint(100, 10000)
                avg_time = random.uniform(10, 180)
                
                data.append({
                    "Page_Path": page,
                    "Pageviews": views,
                    "Unique_Pageviews": int(views * random.uniform(0.7, 0.95)),
                    "Avg_Time_on_Page": round(avg_time, 2),
                    "Entrances": int(views * random.uniform(0.1, 0.5)),
                    "Bounce_Rate": round(random.uniform(0.1, 0.8), 2),
                    "Exit_Rate": round(random.uniform(0.1, 0.7), 2)
                })
            
            return {
                'filename': 'google_analytics_pages.csv',
                'data': data
            }
    
    # Default fallback for any other integration
    else:
        # Generate generic time series data
        data = []
        metrics = ["Metric A", "Metric B", "Metric C"]
        
        for date in date_range:
            for metric in metrics:
                value = random.uniform(100, 1000)
                data.append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Metric": metric,
                    "Value": round(value, 2)
                })
        
        return {
            'filename': f'{integration_id}_data.csv',
            'data': data
        }

# Helper for Google Analytics data generation
import math
