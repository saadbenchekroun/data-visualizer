import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.data_processor import get_column_types, detect_time_series

def create_visualization(df, config):
    """
    Create a visualization based on the provided configuration
    
    Args:
        df (DataFrame): The pandas DataFrame containing the data
        config (dict): Configuration parameters for the visualization
        
    Returns:
        fig: A plotly figure object
    """
    chart_type = config.get('chart_type', 'bar_chart')
    
    # Dispatch to the appropriate visualization function
    if chart_type == 'bar_chart':
        return create_bar_chart(df, config)
    elif chart_type == 'line_chart':
        return create_line_chart(df, config)
    elif chart_type == 'scatter_plot':
        return create_scatter_plot(df, config)
    elif chart_type == 'pie_chart':
        return create_pie_chart(df, config)
    elif chart_type == 'histogram':
        return create_histogram(df, config)
    elif chart_type == 'box_plot':
        return create_box_plot(df, config)
    elif chart_type == 'heatmap':
        return create_heatmap(df, config)
    else:
        # Default to bar chart
        return create_bar_chart(df, config)

def render_visualization(df, config):
    """Wrapper around create_visualization to handle errors gracefully"""
    try:
        fig = create_visualization(df, config)
        return fig
    except Exception as e:
        # Create an error message figure
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error creating visualization:<br>{str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="red", size=14)
        )
        return fig

def create_bar_chart(df, config):
    """Create a bar chart"""
    x = config.get('x')
    y = config.get('y')
    color = config.get('color', None)
    orientation = config.get('orientation', 'Vertical')
    title = config.get('title', f'Bar Chart of {y} by {x}')
    
    # Handle orientation
    if orientation == 'Horizontal':
        # Swap x and y for horizontal orientation
        fig = px.bar(
            df, 
            y=x, 
            x=y, 
            color=color if color != 'None' else None,
            title=title,
            orientation='h'
        )
    else:
        fig = px.bar(
            df, 
            x=x, 
            y=y, 
            color=color if color != 'None' else None,
            title=title
        )
    
    # Update layout
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        legend_title=color if color and color != 'None' else None
    )
    
    return fig

def create_line_chart(df, config):
    """Create a line chart"""
    x = config.get('x')
    y = config.get('y')
    color = config.get('color', None)
    markers = config.get('markers', False)
    title = config.get('title', f'Line Chart of {y} over {x}')
    
    fig = px.line(
        df, 
        x=x, 
        y=y, 
        color=color if color != 'None' else None,
        title=title,
        markers=markers
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        legend_title=color if color and color != 'None' else None
    )
    
    return fig

def create_scatter_plot(df, config):
    """Create a scatter plot"""
    x = config.get('x')
    y = config.get('y')
    color = config.get('color', None)
    size = config.get('size', None)
    title = config.get('title', f'Scatter Plot of {y} vs {x}')
    
    fig = px.scatter(
        df, 
        x=x, 
        y=y,
        color=color if color != 'None' else None,
        size=size if size != 'None' else None,
        title=title
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        legend_title=color if color and color != 'None' else None
    )
    
    return fig

def create_pie_chart(df, config):
    """Create a pie chart"""
    names = config.get('names')
    values = config.get('values')
    hole = config.get('hole', 0)  # 0 for pie chart, > 0 for donut chart
    title = config.get('title', f'Distribution of {values} by {names}')
    
    # Group by category and sum values
    pie_data = df.groupby(names)[values].sum().reset_index()
    
    fig = px.pie(
        pie_data, 
        names=names, 
        values=values,
        title=title,
        hole=hole
    )
    
    # Update layout
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def create_histogram(df, config):
    """Create a histogram"""
    x = config.get('x')
    bins = config.get('bins', 20)
    color = config.get('color', None)
    title = config.get('title', f'Histogram of {x}')
    
    fig = px.histogram(
        df, 
        x=x,
        color=color if color != 'None' else None,
        nbins=bins,
        title=title
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title=x,
        yaxis_title='Count',
        bargap=0.1
    )
    
    return fig

def create_box_plot(df, config):
    """Create a box plot"""
    y = config.get('y')
    x = config.get('x', None)
    title = config.get('title', f'Box Plot of {y}' + (f' by {x}' if x and x != 'None' else ''))
    
    fig = px.box(
        df, 
        y=y,
        x=x if x != 'None' else None,
        title=title
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title=x if x and x != 'None' else None,
        yaxis_title=y
    )
    
    return fig

def create_heatmap(df, config):
    """Create a heatmap"""
    x = config.get('x')
    y = config.get('y')
    values = config.get('values')
    color_scale = config.get('color_scale', 'Viridis').lower()
    title = config.get('title', f'Heatmap of {values} by {x} and {y}')
    
    # Pivot data for heatmap
    pivot_data = df.pivot_table(
        index=y, 
        columns=x, 
        values=values, 
        aggfunc='mean'
    ).fillna(0)
    
    fig = px.imshow(
        pivot_data,
        labels=dict(x=x, y=y, color=values),
        x=pivot_data.columns,
        y=pivot_data.index,
        color_continuous_scale=color_scale,
        title=title
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y
    )
    
    # Add text annotations with values
    for i, row in enumerate(pivot_data.index):
        for j, col in enumerate(pivot_data.columns):
            value = pivot_data.iloc[i, j]
            text_color = "white" if value > (pivot_data.max().max() / 2) else "black"
            fig.add_annotation(
                x=col,
                y=row,
                text=str(round(value, 2)),
                showarrow=False,
                font=dict(color=text_color)
            )
    
    return fig

def get_visualization_suggestions(df):
    """
    Generate smart visualization suggestions based on the dataset structure
    
    Args:
        df (DataFrame): The pandas DataFrame to analyze
        
    Returns:
        list: List of suggestion objects with visualization configs
    """
    suggestions = []
    column_types = get_column_types(df)
    
    # Get lists of different column types
    numeric_cols = [col for col, type in column_types.items() if type == 'numeric']
    categorical_cols = [col for col, type in column_types.items() if type == 'categorical']
    datetime_cols = [col for col, type in column_types.items() if type == 'datetime']
    
    # Try to detect date/time columns if none were found
    if not datetime_cols:
        for col in df.columns:
            if col not in numeric_cols and col not in categorical_cols:
                try:
                    pd.to_datetime(df[col])
                    datetime_cols.append(col)
                except:
                    pass
    
    # Suggestion 1: If time series data is available, suggest a line chart
    if datetime_cols and numeric_cols:
        suggestions.append({
            'title': 'Time Series Analysis',
            'description': f'Track how {numeric_cols[0]} changes over time',
            'config': {
                'chart_type': 'line_chart',
                'x': datetime_cols[0],
                'y': numeric_cols[0],
                'markers': True,
                'title': f'{numeric_cols[0]} Over Time'
            }
        })
    
    # Suggestion 2: If multiple numeric columns, suggest a scatter plot
    if len(numeric_cols) >= 2:
        suggestions.append({
            'title': 'Correlation Analysis',
            'description': f'Explore relationship between {numeric_cols[0]} and {numeric_cols[1]}',
            'config': {
                'chart_type': 'scatter_plot',
                'x': numeric_cols[0],
                'y': numeric_cols[1],
                'color': categorical_cols[0] if categorical_cols else None,
                'title': f'Correlation: {numeric_cols[0]} vs {numeric_cols[1]}'
            }
        })
    
    # Suggestion 3: If categorical and numeric columns, suggest a bar chart
    if categorical_cols and numeric_cols:
        suggestions.append({
            'title': 'Category Comparison',
            'description': f'Compare {numeric_cols[0]} across different {categorical_cols[0]} categories',
            'config': {
                'chart_type': 'bar_chart',
                'x': categorical_cols[0],
                'y': numeric_cols[0],
                'color': categorical_cols[1] if len(categorical_cols) > 1 else None,
                'title': f'{numeric_cols[0]} by {categorical_cols[0]}'
            }
        })
    
    # Suggestion 4: Distribution analysis with histogram
    if numeric_cols:
        suggestions.append({
            'title': 'Distribution Analysis',
            'description': f'Examine the distribution of {numeric_cols[0]} values',
            'config': {
                'chart_type': 'histogram',
                'x': numeric_cols[0],
                'bins': min(30, max(10, df[numeric_cols[0]].nunique() // 2)),
                'color': categorical_cols[0] if categorical_cols else None,
                'title': f'Distribution of {numeric_cols[0]}'
            }
        })
    
    # Suggestion 5: If categorical column with few unique values and numeric column, suggest pie chart
    if categorical_cols and numeric_cols and df[categorical_cols[0]].nunique() <= 8:
        suggestions.append({
            'title': 'Proportion Analysis',
            'description': f'See the relative proportions of {numeric_cols[0]} by {categorical_cols[0]}',
            'config': {
                'chart_type': 'pie_chart',
                'names': categorical_cols[0],
                'values': numeric_cols[0],
                'hole': 0.4,
                'title': f'Distribution of {numeric_cols[0]} by {categorical_cols[0]}'
            }
        })
    
    # Suggestion 6: Box plot for numeric distributions by category 
    if categorical_cols and numeric_cols:
        suggestions.append({
            'title': 'Statistical Distribution by Category',
            'description': f'Compare statistical distributions of {numeric_cols[0]} across {categorical_cols[0]} categories',
            'config': {
                'chart_type': 'box_plot',
                'y': numeric_cols[0],
                'x': categorical_cols[0],
                'title': f'Distribution of {numeric_cols[0]} by {categorical_cols[0]}'
            }
        })
    
    # Suggestion 7: Heatmap for relationships between two categorical variables and a numeric value
    if len(categorical_cols) >= 2 and numeric_cols:
        # Only suggest if the combination of categories isn't too large
        if df[categorical_cols[0]].nunique() * df[categorical_cols[1]].nunique() <= 100:
            suggestions.append({
                'title': 'Cross-Category Analysis',
                'description': f'Analyze how {numeric_cols[0]} varies across combinations of {categorical_cols[0]} and {categorical_cols[1]}',
                'config': {
                    'chart_type': 'heatmap',
                    'x': categorical_cols[0],
                    'y': categorical_cols[1],
                    'values': numeric_cols[0],
                    'color_scale': 'Viridis',
                    'title': f'{numeric_cols[0]} by {categorical_cols[0]} and {categorical_cols[1]}'
                }
            })
    
    return suggestions
