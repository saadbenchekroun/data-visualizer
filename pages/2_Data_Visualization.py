import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processor import list_uploaded_files, get_dataframe
from utils.nlp_processor import process_natural_language_query
from utils.visualization import create_visualization, render_visualization, get_visualization_suggestions

st.set_page_config(
    page_title="Data Visualization - DataVizSME",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Visualization")
st.write("Create insightful visualizations from your data using drag-and-drop or natural language")

# Initialize session state for visualizations if not already done
if 'visualizations' not in st.session_state:
    st.session_state.visualizations = {}

if 'current_file' not in st.session_state:
    st.session_state.current_file = None

# Function to save visualization
def save_visualization(name, config):
    st.session_state.visualizations[name] = config
    st.success(f"Visualization '{name}' saved successfully!")

# Check if we have any datasets
available_files = list_uploaded_files()
if not available_files:
    st.warning("No datasets found. Please upload data in the Data Upload section first.")
    if st.button("Go to Data Upload"):
        st.switch_page("pages/1_Data_Upload.py")
    st.stop()

# File selection
selected_file = st.selectbox(
    "Select a dataset", 
    available_files,
    index=0 if st.session_state.current_file is None else available_files.index(st.session_state.current_file) if st.session_state.current_file in available_files else 0
)

# Load the selected dataset
try:
    df = get_dataframe(selected_file)
    st.session_state.current_file = selected_file
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")
    st.stop()

# Display dataset info
with st.expander("Dataset Preview"):
    st.dataframe(df.head(10))
    st.write(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    st.write(f"Columns: {', '.join(df.columns)}")

# Tabs for different visualization creation methods
tab1, tab2, tab3, tab4 = st.tabs(["Natural Language", "Builder", "Saved Visualizations", "Suggestions"])

# Natural Language Tab
with tab1:
    st.subheader("Create Visualizations Using Natural Language")
    st.write("Describe the visualization you want in plain English")
    
    # Examples
    st.info("""
    Examples:
    - "Show me sales by month as a line chart"
    - "Create a bar chart of revenue by product category"
    - "Scatter plot of price vs. quantity with color by category"
    - "Distribution of customer ages as a histogram"
    """)
    
    # Natural language input
    nl_query = st.text_input("Describe the visualization you want:", placeholder="e.g., Show sales trend over time as a line chart")
    
    if nl_query:
        viz_config = process_natural_language_query(nl_query, df)
        
        if viz_config:
            st.write("### Generated Visualization")
            
            try:
                fig = render_visualization(df, viz_config)
                st.plotly_chart(fig, use_container_width=True)
                
                # Save option
                viz_name = st.text_input("Visualization name (to save):", placeholder="My Visualization")
                if viz_name:
                    if st.button("Save Visualization"):
                        if viz_name in st.session_state.visualizations:
                            overwrite = st.checkbox("A visualization with this name already exists. Overwrite?")
                            if overwrite:
                                save_visualization(viz_name, viz_config)
                        else:
                            save_visualization(viz_name, viz_config)
            except Exception as e:
                st.error(f"Error generating visualization: {str(e)}")
        else:
            st.warning("Could not interpret your query. Please try a different description.")

# Builder Tab
with tab2:
    st.subheader("Visualization Builder")
    st.write("Create visualizations by selecting chart type and data fields")
    
    # Chart type selection
    chart_type = st.selectbox(
        "Select visualization type:",
        ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot", "Heatmap"]
    )
    
    # Get columns of different types
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    temporal_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    all_cols = df.columns.tolist()
    
    # Configuration based on chart type
    viz_config = {"chart_type": chart_type.lower().replace(" ", "_")}
    
    if chart_type == "Bar Chart":
        viz_config["x"] = st.selectbox("X-axis (Categories):", categorical_cols + temporal_cols if categorical_cols + temporal_cols else ["No categorical columns found"])
        viz_config["y"] = st.selectbox("Y-axis (Values):", numeric_cols if numeric_cols else ["No numeric columns found"])
        viz_config["color"] = st.selectbox("Color (Optional):", ["None"] + categorical_cols)
        viz_config["orientation"] = st.radio("Orientation:", ["Vertical", "Horizontal"])
        
    elif chart_type == "Line Chart":
        viz_config["x"] = st.selectbox("X-axis (Time/Sequence):", temporal_cols + numeric_cols if temporal_cols + numeric_cols else ["No appropriate columns found"])
        viz_config["y"] = st.selectbox("Y-axis (Values):", numeric_cols if numeric_cols else ["No numeric columns found"])
        viz_config["color"] = st.selectbox("Color/Group by (Optional):", ["None"] + categorical_cols)
        viz_config["markers"] = st.checkbox("Show markers")
        
    elif chart_type == "Scatter Plot":
        viz_config["x"] = st.selectbox("X-axis:", numeric_cols if numeric_cols else ["No numeric columns found"])
        viz_config["y"] = st.selectbox("Y-axis:", numeric_cols if numeric_cols else ["No numeric columns found"], index=min(1, len(numeric_cols)-1) if len(numeric_cols) > 1 else 0)
        viz_config["color"] = st.selectbox("Color by (Optional):", ["None"] + categorical_cols + numeric_cols)
        viz_config["size"] = st.selectbox("Size by (Optional):", ["None"] + numeric_cols)
        
    elif chart_type == "Pie Chart":
        viz_config["names"] = st.selectbox("Slice Labels:", categorical_cols if categorical_cols else ["No categorical columns found"])
        viz_config["values"] = st.selectbox("Slice Values:", numeric_cols if numeric_cols else ["No numeric columns found"])
        viz_config["hole"] = st.slider("Donut hole size (0 for pie chart):", 0.0, 0.7, 0.0)
        
    elif chart_type == "Histogram":
        viz_config["x"] = st.selectbox("Values:", numeric_cols if numeric_cols else ["No numeric columns found"])
        viz_config["bins"] = st.slider("Number of bins:", 5, 100, 20)
        viz_config["color"] = st.selectbox("Color by (Optional):", ["None"] + categorical_cols)
        
    elif chart_type == "Box Plot":
        viz_config["y"] = st.selectbox("Values:", numeric_cols if numeric_cols else ["No numeric columns found"])
        viz_config["x"] = st.selectbox("Group by (Optional):", ["None"] + categorical_cols)
        
    elif chart_type == "Heatmap":
        viz_config["x"] = st.selectbox("X-axis:", categorical_cols + temporal_cols if categorical_cols + temporal_cols else ["No categorical columns found"])
        viz_config["y"] = st.selectbox("Y-axis:", categorical_cols if categorical_cols else ["No categorical columns found"], index=min(1, len(categorical_cols)-1) if len(categorical_cols) > 1 else 0)
        viz_config["values"] = st.selectbox("Values:", numeric_cols if numeric_cols else ["No numeric columns found"])
        viz_config["color_scale"] = st.selectbox("Color Scale:", ["Viridis", "Plasma", "Inferno", "Magma", "Cividis", "Blues", "Reds", "Greens"])
    
    # Title and description
    viz_config["title"] = st.text_input("Chart Title:", placeholder="My Chart Title")
    
    # Generate visualization
    if st.button("Generate Visualization"):
        try:
            fig = render_visualization(df, viz_config)
            st.plotly_chart(fig, use_container_width=True)
            
            # Save option
            viz_name = st.text_input("Save visualization as:", placeholder="My Visualization")
            if viz_name:
                if st.button("Save"):
                    if viz_name in st.session_state.visualizations:
                        overwrite = st.checkbox("A visualization with this name already exists. Overwrite?")
                        if overwrite:
                            save_visualization(viz_name, viz_config)
                    else:
                        save_visualization(viz_name, viz_config)
        except Exception as e:
            st.error(f"Error generating visualization: {str(e)}")
            st.error("Please check your selections and try again.")

# Saved Visualizations Tab
with tab3:
    st.subheader("Saved Visualizations")
    
    if not st.session_state.visualizations:
        st.info("No visualizations saved yet. Create and save visualizations in the Builder or Natural Language tabs.")
    else:
        # Display saved visualizations
        viz_to_display = st.selectbox("Select visualization to view:", list(st.session_state.visualizations.keys()))
        
        if viz_to_display:
            viz_config = st.session_state.visualizations[viz_to_display]
            
            # Display visualization
            try:
                fig = render_visualization(df, viz_config)
                st.plotly_chart(fig, use_container_width=True)
                
                # Actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Edit Visualization"):
                        st.session_state.edit_viz_config = viz_config
                        st.rerun()
                        
                with col2:
                    if st.button("Delete Visualization"):
                        del st.session_state.visualizations[viz_to_display]
                        st.success(f"Visualization '{viz_to_display}' deleted successfully")
                        st.rerun()
            
            except Exception as e:
                st.error(f"Error displaying visualization: {str(e)}")

# Suggestions Tab
with tab4:
    st.subheader("Visualization Suggestions")
    st.write("Smart suggestions based on your dataset structure")
    
    # Generate suggestions
    suggestions = get_visualization_suggestions(df)
    
    if not suggestions:
        st.info("No suggestions available for this dataset.")
    else:
        for i, suggestion in enumerate(suggestions):
            st.write(f"### Suggestion {i+1}: {suggestion['title']}")
            st.write(suggestion['description'])
            
            try:
                fig = render_visualization(df, suggestion['config'])
                st.plotly_chart(fig, use_container_width=True)
                
                if st.button(f"Use This Visualization #{i+1}"):
                    # Set up this visualization in the builder
                    viz_name = f"Suggested Viz {i+1}"
                    save_visualization(viz_name, suggestion['config'])
                    st.success(f"Visualization saved as '{viz_name}'")
            except Exception as e:
                st.error(f"Error generating suggestion: {str(e)}")
