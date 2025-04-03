import pandas as pd
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import streamlit as st

# Download required NLTK resources if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Define keyword mappings for visualization types
CHART_TYPE_KEYWORDS = {
    'bar_chart': ['bar', 'bars', 'bar chart', 'bar graph', 'column', 'columns'],
    'line_chart': ['line', 'lines', 'line chart', 'line graph', 'trend', 'trends', 'time series'],
    'scatter_plot': ['scatter', 'scatterplot', 'scatter plot', 'points', 'correlation'],
    'pie_chart': ['pie', 'pie chart', 'proportion', 'percentage', 'distribution'],
    'histogram': ['histogram', 'distribution', 'frequency'],
    'box_plot': ['box', 'box plot', 'boxplot', 'whisker', 'quartile', 'median', 'box and whisker'],
    'heatmap': ['heatmap', 'heat map', 'correlation', 'matrix']
}

# Define common aggregation keywords
AGGREGATION_KEYWORDS = {
    'sum': ['sum', 'total', 'add'],
    'average': ['average', 'avg', 'mean'],
    'count': ['count', 'frequency', 'occurrences', 'number of'],
    'min': ['minimum', 'min', 'lowest', 'smallest'],
    'max': ['maximum', 'max', 'highest', 'largest'],
    'median': ['median', 'middle']
}

def process_natural_language_query(query, df):
    """
    Process a natural language query and generate a visualization configuration.
    
    Args:
        query (str): The natural language query from the user
        df (DataFrame): The pandas DataFrame containing the data
    
    Returns:
        dict: A visualization configuration object
    """
    # Convert query to lowercase
    query = query.lower()
    
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(query)
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
    
    # Get column names and types from dataframe
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    temporal_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Try to convert string columns to datetime if they're not already detected
    if not temporal_cols:
        for col in categorical_cols:
            try:
                pd.to_datetime(df[col])
                temporal_cols.append(col)
            except:
                pass
    
    # Identify visualization type based on keywords
    viz_type = identify_visualization_type(query)
    
    # Identify referenced columns
    referenced_cols = identify_referenced_columns(query, df.columns)
    
    # Identify aggregation method
    aggregation = identify_aggregation(query)
    
    # Generate configuration based on visualization type
    config = {
        "chart_type": viz_type,
        "title": query.capitalize()
    }
    
    # Try to intelligently assign axes based on column types and visualization type
    if viz_type == 'bar_chart':
        config = configure_bar_chart(config, df, referenced_cols, numeric_cols, categorical_cols, temporal_cols, aggregation)
    
    elif viz_type == 'line_chart':
        config = configure_line_chart(config, df, referenced_cols, numeric_cols, categorical_cols, temporal_cols, aggregation)
    
    elif viz_type == 'scatter_plot':
        config = configure_scatter_plot(config, df, referenced_cols, numeric_cols)
    
    elif viz_type == 'pie_chart':
        config = configure_pie_chart(config, df, referenced_cols, numeric_cols, categorical_cols, aggregation)
    
    elif viz_type == 'histogram':
        config = configure_histogram(config, df, referenced_cols, numeric_cols)
    
    elif viz_type == 'box_plot':
        config = configure_box_plot(config, df, referenced_cols, numeric_cols, categorical_cols)
    
    elif viz_type == 'heatmap':
        config = configure_heatmap(config, df, referenced_cols, numeric_cols, categorical_cols)
    
    return config

def identify_visualization_type(query):
    """Identify the visualization type from the query"""
    scores = {viz_type: 0 for viz_type in CHART_TYPE_KEYWORDS}
    
    # Calculate scores for each visualization type
    for viz_type, keywords in CHART_TYPE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in query:
                scores[viz_type] += 1
    
    # Default to bar chart if no visualization type is specified
    if max(scores.values()) == 0:
        if "over time" in query or "trend" in query or "time series" in query:
            return "line_chart"
        else:
            return "bar_chart"
    
    # Return the visualization type with the highest score
    return max(scores, key=scores.get)

def identify_referenced_columns(query, columns):
    """Identify columns referenced in the query"""
    referenced_cols = []
    
    # Normalize column names for matching
    column_variations = {}
    for col in columns:
        # Original column name
        column_variations[col.lower()] = col
        
        # Without underscores and spaces
        normalized = col.lower().replace('_', ' ').replace('-', ' ')
        column_variations[normalized] = col
        
        # Plural variations
        if normalized.endswith('s'):
            column_variations[normalized[:-1]] = col
        else:
            column_variations[normalized + 's'] = col
    
    # Check for column name mentions in the query
    for variation, original in column_variations.items():
        if variation in query and original not in referenced_cols:
            referenced_cols.append(original)
    
    return referenced_cols

def identify_aggregation(query):
    """Identify aggregation method from the query"""
    for agg, keywords in AGGREGATION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in query:
                return agg
    
    # Default to sum for aggregation
    return 'sum'

def configure_bar_chart(config, df, referenced_cols, numeric_cols, categorical_cols, temporal_cols, aggregation):
    """Configure bar chart visualization"""
    if len(referenced_cols) >= 2:
        # If we have both categorical and numeric columns referenced
        cat_refs = [col for col in referenced_cols if col in categorical_cols]
        num_refs = [col for col in referenced_cols if col in numeric_cols]
        time_refs = [col for col in referenced_cols if col in temporal_cols]
        
        if cat_refs and num_refs:
            config["x"] = cat_refs[0]
            config["y"] = num_refs[0]
        elif time_refs and num_refs:
            config["x"] = time_refs[0]
            config["y"] = num_refs[0]
        else:
            # Default to first two referenced columns
            config["x"] = referenced_cols[0]
            config["y"] = referenced_cols[1]
    else:
        # Try to make a sensible choice based on available columns
        if categorical_cols and numeric_cols:
            config["x"] = categorical_cols[0]
            config["y"] = numeric_cols[0]
        elif temporal_cols and numeric_cols:
            config["x"] = temporal_cols[0]
            config["y"] = numeric_cols[0]
        elif len(numeric_cols) >= 2:
            config["x"] = numeric_cols[0]
            config["y"] = numeric_cols[1]
        elif numeric_cols:
            config["x"] = df.index.name or "index"
            config["y"] = numeric_cols[0]
        else:
            # Fallback for non-numeric data
            config["x"] = df.columns[0]
            config["y"] = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    # Add color if we have multiple categories
    if len(categorical_cols) > 1 and categorical_cols[0] != config["x"]:
        config["color"] = categorical_cols[0]
    
    # Default to vertical orientation
    config["orientation"] = "Vertical"
    
    return config

def configure_line_chart(config, df, referenced_cols, numeric_cols, categorical_cols, temporal_cols, aggregation):
    """Configure line chart visualization"""
    # For line charts, prioritize time columns for x-axis
    if temporal_cols:
        config["x"] = temporal_cols[0]
        
        # For y-axis, use referenced numeric column or first numeric column
        num_refs = [col for col in referenced_cols if col in numeric_cols]
        if num_refs:
            config["y"] = num_refs[0]
        elif numeric_cols:
            config["y"] = numeric_cols[0]
        else:
            # Fallback if no numeric columns
            config["y"] = referenced_cols[0] if referenced_cols else df.columns[0]
    else:
        # No time columns, try to use numeric columns for x and y
        if len(numeric_cols) >= 2:
            num_refs = [col for col in referenced_cols if col in numeric_cols]
            if len(num_refs) >= 2:
                config["x"] = num_refs[0]
                config["y"] = num_refs[1]
            else:
                config["x"] = numeric_cols[0]
                config["y"] = numeric_cols[1]
        elif numeric_cols:
            config["x"] = df.index.name or "index"
            config["y"] = numeric_cols[0]
        else:
            # Fallback for non-numeric data
            config["x"] = df.columns[0]
            config["y"] = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    # Add color grouping if categorical columns exist
    if categorical_cols:
        cat_refs = [col for col in referenced_cols if col in categorical_cols]
        if cat_refs:
            config["color"] = cat_refs[0]
        else:
            config["color"] = categorical_cols[0]
    
    # Enable markers for better visibility
    config["markers"] = True
    
    return config

def configure_scatter_plot(config, df, referenced_cols, numeric_cols):
    """Configure scatter plot visualization"""
    # Scatter plots need at least two numeric columns
    if len(numeric_cols) >= 2:
        num_refs = [col for col in referenced_cols if col in numeric_cols]
        if len(num_refs) >= 2:
            config["x"] = num_refs[0]
            config["y"] = num_refs[1]
        else:
            config["x"] = numeric_cols[0]
            config["y"] = numeric_cols[1]
        
        # Add color by a third numeric column if available
        if len(numeric_cols) > 2 and len(num_refs) > 2:
            config["color"] = num_refs[2]
        elif len(numeric_cols) > 2:
            config["color"] = numeric_cols[2]
    else:
        # Not enough numeric columns for a scatter plot, default to something sensible
        config["chart_type"] = "bar_chart"
        config["x"] = df.columns[0]
        config["y"] = numeric_cols[0] if numeric_cols else df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    return config

def configure_pie_chart(config, df, referenced_cols, numeric_cols, categorical_cols, aggregation):
    """Configure pie chart visualization"""
    # Pie charts need categorical labels and numeric values
    if categorical_cols and numeric_cols:
        cat_refs = [col for col in referenced_cols if col in categorical_cols]
        num_refs = [col for col in referenced_cols if col in numeric_cols]
        
        if cat_refs and num_refs:
            config["names"] = cat_refs[0]
            config["values"] = num_refs[0]
        else:
            config["names"] = categorical_cols[0]
            config["values"] = numeric_cols[0]
        
        # Set hole=0 for a pie chart (not donut)
        config["hole"] = 0
    else:
        # Not enough of the right column types, default to something else
        config["chart_type"] = "bar_chart"
        config["x"] = df.columns[0]
        config["y"] = numeric_cols[0] if numeric_cols else df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    return config

def configure_histogram(config, df, referenced_cols, numeric_cols):
    """Configure histogram visualization"""
    # Histograms need numeric data
    if numeric_cols:
        num_refs = [col for col in referenced_cols if col in numeric_cols]
        if num_refs:
            config["x"] = num_refs[0]
        else:
            config["x"] = numeric_cols[0]
        
        # Set a reasonable number of bins
        config["bins"] = 20
    else:
        # No numeric columns, default to bar chart
        config["chart_type"] = "bar_chart"
        config["x"] = df.columns[0]
        config["y"] = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    return config

def configure_box_plot(config, df, referenced_cols, numeric_cols, categorical_cols):
    """Configure box plot visualization"""
    # Box plots need numeric values and optionally categories for grouping
    if numeric_cols:
        num_refs = [col for col in referenced_cols if col in numeric_cols]
        cat_refs = [col for col in referenced_cols if col in categorical_cols]
        
        if num_refs:
            config["y"] = num_refs[0]
        else:
            config["y"] = numeric_cols[0]
        
        # Add categorical grouping if available
        if cat_refs:
            config["x"] = cat_refs[0]
        elif categorical_cols:
            config["x"] = categorical_cols[0]
        else:
            config["x"] = "None"
    else:
        # No numeric columns, default to bar chart
        config["chart_type"] = "bar_chart"
        config["x"] = df.columns[0]
        config["y"] = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    return config

def configure_heatmap(config, df, referenced_cols, numeric_cols, categorical_cols):
    """Configure heatmap visualization"""
    # Heatmaps need two categorical dimensions and one numeric value
    if len(categorical_cols) >= 2 and numeric_cols:
        cat_refs = [col for col in referenced_cols if col in categorical_cols]
        num_refs = [col for col in referenced_cols if col in numeric_cols]
        
        if len(cat_refs) >= 2 and num_refs:
            config["x"] = cat_refs[0]
            config["y"] = cat_refs[1]
            config["values"] = num_refs[0]
        elif len(cat_refs) >= 2:
            config["x"] = cat_refs[0]
            config["y"] = cat_refs[1]
            config["values"] = numeric_cols[0]
        elif cat_refs and num_refs:
            config["x"] = cat_refs[0]
            config["y"] = categorical_cols[0] if categorical_cols[0] != cat_refs[0] else categorical_cols[1]
            config["values"] = num_refs[0]
        else:
            config["x"] = categorical_cols[0]
            config["y"] = categorical_cols[1]
            config["values"] = numeric_cols[0]
        
        # Set a nice color scale
        config["color_scale"] = "Viridis"
    else:
        # Not enough of the right column types, default to something else
        config["chart_type"] = "bar_chart"
        config["x"] = categorical_cols[0] if categorical_cols else df.columns[0]
        config["y"] = numeric_cols[0] if numeric_cols else df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    return config
