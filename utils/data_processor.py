import pandas as pd
import os
import json
from io import StringIO
import streamlit as st

# Define a simple file storage mechanism using session state
# In a real application, this would use a database or file system
def save_dataframe(filename, df):
    """Save a dataframe to the session state storage"""
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    
    st.session_state.uploaded_files[filename] = df
    return True

def get_dataframe(filename):
    """Retrieve a dataframe from session state storage"""
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    
    if filename in st.session_state.uploaded_files:
        return st.session_state.uploaded_files[filename]
    else:
        raise FileNotFoundError(f"File {filename} not found in storage")

def delete_dataframe(filename):
    """Delete a dataframe from session state storage"""
    if 'uploaded_files' in st.session_state and filename in st.session_state.uploaded_files:
        del st.session_state.uploaded_files[filename]
        return True
    return False

def list_uploaded_files():
    """List all files in the session state storage"""
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    
    return list(st.session_state.uploaded_files.keys())

def get_column_types(df):
    """Determine column types for a dataframe"""
    column_types = {}
    
    for col in df.columns:
        # Numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            column_types[col] = 'numeric'
        # Datetime
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            column_types[col] = 'datetime'
        # Boolean
        elif pd.api.types.is_bool_dtype(df[col]):
            column_types[col] = 'boolean'
        # Categorical/text - further analyze
        else:
            # Check if it's likely a categorical variable
            unique_count = df[col].nunique()
            total_count = len(df)
            
            # If less than 10% of values are unique or fewer than 20 unique values, consider categorical
            if unique_count < 20 or (unique_count / total_count) < 0.1:
                column_types[col] = 'categorical'
            else:
                column_types[col] = 'text'
    
    return column_types

def get_column_stats(df):
    """Get statistics for each column in the dataframe"""
    stats = {}
    
    for col in df.columns:
        col_stats = {}
        
        # Basic stats for all columns
        col_stats['count'] = df[col].count()
        col_stats['null_count'] = df[col].isna().sum()
        col_stats['unique_count'] = df[col].nunique()
        
        # Type-specific stats
        if pd.api.types.is_numeric_dtype(df[col]):
            col_stats['min'] = df[col].min()
            col_stats['max'] = df[col].max()
            col_stats['mean'] = df[col].mean()
            col_stats['median'] = df[col].median()
            col_stats['std'] = df[col].std()
        
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            col_stats['min'] = df[col].min().strftime('%Y-%m-%d')
            col_stats['max'] = df[col].max().strftime('%Y-%m-%d')
            
        elif not pd.api.types.is_bool_dtype(df[col]):  # Text or categorical
            if col_stats['unique_count'] <= 10:  # Show value counts for categorical variables
                col_stats['value_counts'] = df[col].value_counts().head(10).to_dict()
        
        stats[col] = col_stats
    
    return stats

def detect_time_series(df):
    """Detect if the dataframe contains time series data"""
    
    # Check for datetime columns
    datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    
    if not datetime_cols:
        # Check if any columns can be converted to datetime
        for col in df.columns:
            try:
                pd.to_datetime(df[col])
                datetime_cols.append(col)
            except:
                pass
    
    # Check if we have both datetime and numeric columns
    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    
    if datetime_cols and numeric_cols:
        return {
            'is_time_series': True,
            'datetime_cols': datetime_cols,
            'numeric_cols': numeric_cols
        }
    
    return {'is_time_series': False}
