import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def get_industry_templates(industry):
    """
    Get visualization templates for a specific industry
    
    Args:
        industry (str): The industry to get templates for
        
    Returns:
        list: List of template objects with configuration
    """
    # Retail & E-commerce templates
    if industry == "Retail & E-commerce":
        return [
            {
                'name': 'Sales Performance Dashboard',
                'description': 'Track sales performance over time with breakdowns by product category and customer segments',
                'required_fields': ['Date', 'Sales', 'Product Category', 'Customer Segment'],
                'visualizations': [
                    {
                        'title': 'Sales Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Sales',
                            'markers': True,
                            'title': 'Sales Trend Over Time'
                        }
                    },
                    {
                        'title': 'Sales by Category',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Product Category',
                            'y': 'Sales',
                            'title': 'Sales by Product Category'
                        }
                    },
                    {
                        'title': 'Customer Segment Distribution',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Customer Segment',
                            'values': 'Sales',
                            'title': 'Sales by Customer Segment'
                        }
                    }
                ]
            },
            {
                'name': 'Customer Insights Dashboard',
                'description': 'Analyze customer behavior, demographics, and purchasing patterns',
                'required_fields': ['Customer ID', 'Age', 'Gender', 'Purchase Amount', 'Date'],
                'visualizations': [
                    {
                        'title': 'Customer Age Distribution',
                        'config': {
                            'chart_type': 'histogram',
                            'x': 'Age',
                            'bins': 15,
                            'title': 'Customer Age Distribution'
                        }
                    },
                    {
                        'title': 'Purchase Amount by Gender',
                        'config': {
                            'chart_type': 'box_plot',
                            'y': 'Purchase Amount',
                            'x': 'Gender',
                            'title': 'Purchase Amount by Gender'
                        }
                    },
                    {
                        'title': 'Purchase Trends',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Purchase Amount',
                            'title': 'Purchase Trends Over Time'
                        }
                    }
                ]
            },
            {
                'name': 'Inventory Analysis',
                'description': 'Monitor inventory levels, turnover rates, and stock efficiency',
                'required_fields': ['Product', 'Stock Level', 'Reorder Point', 'Cost', 'Sales'],
                'visualizations': [
                    {
                        'title': 'Stock Levels vs Reorder Points',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Product',
                            'y': 'Stock Level',
                            'title': 'Current Stock vs Reorder Points'
                        }
                    },
                    {
                        'title': 'Inventory Value Distribution',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Product',
                            'values': 'Cost',
                            'title': 'Inventory Value by Product'
                        }
                    },
                    {
                        'title': 'Sales to Stock Ratio',
                        'config': {
                            'chart_type': 'scatter_plot',
                            'x': 'Stock Level',
                            'y': 'Sales',
                            'title': 'Sales to Stock Level Correlation'
                        }
                    }
                ]
            }
        ]
    
    # Financial Services templates
    elif industry == "Financial Services":
        return [
            {
                'name': 'Financial Performance Overview',
                'description': 'Track revenue, expenses, and profitability over time',
                'required_fields': ['Date', 'Revenue', 'Expenses', 'Profit', 'Department'],
                'visualizations': [
                    {
                        'title': 'Profit & Loss Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Profit',
                            'markers': True,
                            'title': 'Profit Trend Over Time'
                        }
                    },
                    {
                        'title': 'Revenue vs Expenses',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Date',
                            'y': 'Revenue',
                            'title': 'Revenue vs Expenses by Period'
                        }
                    },
                    {
                        'title': 'Department Profitability',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Department',
                            'values': 'Profit',
                            'title': 'Profit by Department'
                        }
                    }
                ]
            },
            {
                'name': 'Cash Flow Analysis',
                'description': 'Visualize cash inflows, outflows, and net cash position',
                'required_fields': ['Date', 'Cash In', 'Cash Out', 'Category', 'Net Cash'],
                'visualizations': [
                    {
                        'title': 'Cash Flow Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Net Cash',
                            'markers': True,
                            'title': 'Net Cash Position Over Time'
                        }
                    },
                    {
                        'title': 'Cash Inflows vs Outflows',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Date',
                            'y': 'Cash In',
                            'title': 'Cash Inflows vs Outflows by Period'
                        }
                    },
                    {
                        'title': 'Cash Flow by Category',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Category',
                            'values': 'Cash In',
                            'title': 'Cash Inflows by Category'
                        }
                    }
                ]
            },
            {
                'name': 'Client Portfolio Analysis',
                'description': 'Analyze client portfolios, asset allocation, and performance',
                'required_fields': ['Client', 'Asset Class', 'Investment Amount', 'Return', 'Risk Score'],
                'visualizations': [
                    {
                        'title': 'Asset Allocation',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Asset Class',
                            'values': 'Investment Amount',
                            'title': 'Asset Allocation by Class'
                        }
                    },
                    {
                        'title': 'Risk vs Return',
                        'config': {
                            'chart_type': 'scatter_plot',
                            'x': 'Risk Score',
                            'y': 'Return',
                            'title': 'Risk vs Return by Asset Class'
                        }
                    },
                    {
                        'title': 'Client Investment Distribution',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Client',
                            'y': 'Investment Amount',
                            'color': 'Asset Class',
                            'title': 'Investment Distribution by Client'
                        }
                    }
                ]
            }
        ]
    
    # Manufacturing templates
    elif industry == "Manufacturing":
        return [
            {
                'name': 'Production Performance',
                'description': 'Track production output, efficiency, and quality metrics',
                'required_fields': ['Date', 'Production Output', 'Efficiency', 'Defect Rate', 'Product Line'],
                'visualizations': [
                    {
                        'title': 'Production Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Production Output',
                            'color': 'Product Line',
                            'markers': True,
                            'title': 'Production Output Over Time'
                        }
                    },
                    {
                        'title': 'Efficiency Analysis',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Product Line',
                            'y': 'Efficiency',
                            'title': 'Production Efficiency by Product Line'
                        }
                    },
                    {
                        'title': 'Quality Control',
                        'config': {
                            'chart_type': 'scatter_plot',
                            'x': 'Production Output',
                            'y': 'Defect Rate',
                            'color': 'Product Line',
                            'title': 'Defect Rate vs Production Output'
                        }
                    }
                ]
            },
            {
                'name': 'Supply Chain Overview',
                'description': 'Analyze supplier performance, material costs, and inventory levels',
                'required_fields': ['Supplier', 'Material', 'Cost', 'Lead Time', 'Quality Score'],
                'visualizations': [
                    {
                        'title': 'Supplier Performance',
                        'config': {
                            'chart_type': 'scatter_plot',
                            'x': 'Lead Time',
                            'y': 'Quality Score',
                            'color': 'Supplier',
                            'size': 'Cost',
                            'title': 'Supplier Performance Matrix'
                        }
                    },
                    {
                        'title': 'Material Cost Distribution',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Material',
                            'values': 'Cost',
                            'title': 'Material Cost Distribution'
                        }
                    },
                    {
                        'title': 'Supplier Lead Times',
                        'config': {
                            'chart_type': 'box_plot',
                            'y': 'Lead Time',
                            'x': 'Supplier',
                            'title': 'Lead Time Distribution by Supplier'
                        }
                    }
                ]
            },
            {
                'name': 'Equipment Effectiveness',
                'description': 'Monitor equipment performance, downtime, and maintenance metrics',
                'required_fields': ['Equipment', 'Uptime', 'Downtime', 'Maintenance Cost', 'Date'],
                'visualizations': [
                    {
                        'title': 'Equipment Uptime',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Equipment',
                            'y': 'Uptime',
                            'title': 'Equipment Uptime Percentage'
                        }
                    },
                    {
                        'title': 'Maintenance Cost Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Maintenance Cost',
                            'color': 'Equipment',
                            'title': 'Maintenance Costs Over Time'
                        }
                    },
                    {
                        'title': 'Downtime Analysis',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Equipment',
                            'values': 'Downtime',
                            'title': 'Downtime Distribution by Equipment'
                        }
                    }
                ]
            }
        ]
    
    # Healthcare templates
    elif industry == "Healthcare":
        return [
            {
                'name': 'Patient Analytics',
                'description': 'Analyze patient demographics, visits, and treatment outcomes',
                'required_fields': ['Patient ID', 'Age', 'Gender', 'Diagnosis', 'Treatment', 'Outcome'],
                'visualizations': [
                    {
                        'title': 'Patient Age Distribution',
                        'config': {
                            'chart_type': 'histogram',
                            'x': 'Age',
                            'color': 'Gender',
                            'bins': 20,
                            'title': 'Patient Age Distribution'
                        }
                    },
                    {
                        'title': 'Diagnosis Breakdown',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Diagnosis',
                            'values': 'Patient ID',
                            'title': 'Patient Distribution by Diagnosis'
                        }
                    },
                    {
                        'title': 'Treatment Outcomes',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Treatment',
                            'y': 'Outcome',
                            'title': 'Treatment Effectiveness Analysis'
                        }
                    }
                ]
            },
            {
                'name': 'Practice Performance',
                'description': 'Track practice revenue, patient volume, and operational metrics',
                'required_fields': ['Date', 'Revenue', 'Patient Visits', 'Department', 'Cost'],
                'visualizations': [
                    {
                        'title': 'Revenue Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Revenue',
                            'markers': True,
                            'title': 'Revenue Trend Over Time'
                        }
                    },
                    {
                        'title': 'Patient Visit Volume',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Date',
                            'y': 'Patient Visits',
                            'color': 'Department',
                            'title': 'Patient Visits by Department'
                        }
                    },
                    {
                        'title': 'Department Profitability',
                        'config': {
                            'chart_type': 'scatter_plot',
                            'x': 'Cost',
                            'y': 'Revenue',
                            'color': 'Department',
                            'title': 'Revenue vs Cost by Department'
                        }
                    }
                ]
            }
        ]
    
    # Professional Services templates
    elif industry == "Professional Services":
        return [
            {
                'name': 'Client Engagement Analysis',
                'description': 'Analyze client engagements, billable hours, and project profitability',
                'required_fields': ['Client', 'Project', 'Billable Hours', 'Revenue', 'Cost', 'Date'],
                'visualizations': [
                    {
                        'title': 'Billable Hours Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Billable Hours',
                            'color': 'Client',
                            'markers': True,
                            'title': 'Billable Hours Over Time'
                        }
                    },
                    {
                        'title': 'Project Profitability',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Project',
                            'y': 'Revenue',
                            'title': 'Revenue vs Cost by Project'
                        }
                    },
                    {
                        'title': 'Client Revenue Distribution',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Client',
                            'values': 'Revenue',
                            'title': 'Revenue Distribution by Client'
                        }
                    }
                ]
            },
            {
                'name': 'Staff Utilization Dashboard',
                'description': 'Track staff utilization, billable rates, and efficiency',
                'required_fields': ['Employee', 'Billable Hours', 'Available Hours', 'Billable Rate', 'Department'],
                'visualizations': [
                    {
                        'title': 'Utilization Rates',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Employee',
                            'y': 'Billable Hours',
                            'title': 'Utilization Rate by Employee'
                        }
                    },
                    {
                        'title': 'Department Utilization',
                        'config': {
                            'chart_type': 'box_plot',
                            'y': 'Billable Hours',
                            'x': 'Department',
                            'title': 'Utilization Distribution by Department'
                        }
                    },
                    {
                        'title': 'Billable Rate Analysis',
                        'config': {
                            'chart_type': 'scatter_plot',
                            'x': 'Billable Hours',
                            'y': 'Billable Rate',
                            'color': 'Department',
                            'title': 'Billable Rate vs Hours'
                        }
                    }
                ]
            }
        ]
    
    # Hospitality & Food Service templates
    elif industry == "Hospitality & Food Service":
        return [
            {
                'name': 'Sales & Revenue Dashboard',
                'description': 'Track sales, revenue, and customer metrics for hospitality businesses',
                'required_fields': ['Date', 'Sales', 'Customer Count', 'Average Check', 'Product Category'],
                'visualizations': [
                    {
                        'title': 'Daily Sales Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Sales',
                            'markers': True,
                            'title': 'Sales Trend Over Time'
                        }
                    },
                    {
                        'title': 'Sales by Category',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Product Category',
                            'values': 'Sales',
                            'title': 'Sales Distribution by Category'
                        }
                    },
                    {
                        'title': 'Customer Volume vs Average Check',
                        'config': {
                            'chart_type': 'scatter_plot',
                            'x': 'Customer Count',
                            'y': 'Average Check',
                            'color': 'Product Category',
                            'title': 'Customer Volume vs Average Check'
                        }
                    }
                ]
            },
            {
                'name': 'Menu Performance Analysis',
                'description': 'Analyze menu item performance, popularity, and profitability',
                'required_fields': ['Menu Item', 'Orders', 'Revenue', 'Food Cost', 'Category'],
                'visualizations': [
                    {
                        'title': 'Item Popularity',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Menu Item',
                            'y': 'Orders',
                            'color': 'Category',
                            'title': 'Most Popular Menu Items'
                        }
                    },
                    {
                        'title': 'Item Profitability',
                        'config': {
                            'chart_type': 'scatter_plot',
                            'x': 'Food Cost',
                            'y': 'Revenue',
                            'color': 'Category',
                            'title': 'Menu Item Profitability'
                        }
                    },
                    {
                        'title': 'Revenue by Category',
                        'config': {
                            'chart_type': 'pie_chart',
                            'names': 'Category',
                            'values': 'Revenue',
                            'title': 'Revenue Distribution by Category'
                        }
                    }
                ]
            }
        ]
    
    # Real Estate & Construction templates
    elif industry == "Real Estate & Construction":
        return [
            {
                'name': 'Property Performance Dashboard',
                'description': 'Analyze property performance, occupancy rates, and rental income',
                'required_fields': ['Property', 'Rental Income', 'Occupancy Rate', 'Expenses', 'Date'],
                'visualizations': [
                    {
                        'title': 'Income Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Rental Income',
                            'color': 'Property',
                            'markers': True,
                            'title': 'Rental Income Over Time'
                        }
                    },
                    {
                        'title': 'Occupancy Analysis',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Property',
                            'y': 'Occupancy Rate',
                            'title': 'Occupancy Rate by Property'
                        }
                    },
                    {
                        'title': 'Income vs Expenses',
                        'config': {
                            'chart_type': 'scatter_plot',
                            'x': 'Expenses',
                            'y': 'Rental Income',
                            'color': 'Property',
                            'title': 'Income vs Expenses by Property'
                        }
                    }
                ]
            },
            {
                'name': 'Construction Project Tracking',
                'description': 'Monitor construction project progress, costs, and timelines',
                'required_fields': ['Project', 'Actual Cost', 'Budgeted Cost', 'Completion Percentage', 'Date'],
                'visualizations': [
                    {
                        'title': 'Project Progress',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Project',
                            'y': 'Completion Percentage',
                            'title': 'Project Completion Status'
                        }
                    },
                    {
                        'title': 'Budget vs Actual',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Project',
                            'y': 'Actual Cost',
                            'title': 'Budget vs Actual Cost'
                        }
                    },
                    {
                        'title': 'Cost Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Actual Cost',
                            'color': 'Project',
                            'title': 'Project Cost Over Time'
                        }
                    }
                ]
            }
        ]
    
    # Default templates if industry doesn't match
    else:
        return [
            {
                'name': 'General Business Performance',
                'description': 'Track key business metrics and performance indicators',
                'required_fields': ['Date', 'Revenue', 'Expenses', 'Profit'],
                'visualizations': [
                    {
                        'title': 'Revenue & Profit Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Revenue',
                            'markers': True,
                            'title': 'Revenue & Profit Over Time'
                        }
                    },
                    {
                        'title': 'Profit Margin Analysis',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Date',
                            'y': 'Profit',
                            'title': 'Profit Margin Analysis'
                        }
                    }
                ]
            },
            {
                'name': 'Customer Analysis',
                'description': 'Analyze customer data and purchasing behavior',
                'required_fields': ['Customer', 'Purchase Amount', 'Date', 'Product'],
                'visualizations': [
                    {
                        'title': 'Top Customers',
                        'config': {
                            'chart_type': 'bar_chart',
                            'x': 'Customer',
                            'y': 'Purchase Amount',
                            'title': 'Top Customers by Purchase Amount'
                        }
                    },
                    {
                        'title': 'Purchase Trend',
                        'config': {
                            'chart_type': 'line_chart',
                            'x': 'Date',
                            'y': 'Purchase Amount',
                            'title': 'Purchase Trend Over Time'
                        }
                    }
                ]
            }
        ]

def apply_template(template, df, field_mapping):
    """
    Apply a template to a dataframe using field mapping
    
    Args:
        template (dict): The template configuration
        df (DataFrame): The pandas DataFrame to apply the template to
        field_mapping (dict): Mapping from template fields to dataframe columns
        
    Returns:
        list: List of visualization configurations
    """
    # Create a copy of the dataframe with mapped columns
    mapped_df = df.copy()
    
    # Generate visualizations based on the template
    visualizations = []
    
    for viz in template['visualizations']:
        # Create a copy of the config
        config = viz['config'].copy()
        
        # Map the fields in the config
        for key, value in config.items():
            if isinstance(value, str) and value in field_mapping:
                # Replace template field with actual column name
                config[key] = field_mapping[value]
        
        # Add to visualizations list
        visualizations.append({
            'title': viz['title'],
            'config': config
        })
    
    return visualizations
