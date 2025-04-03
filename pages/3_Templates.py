import streamlit as st
import pandas as pd
from utils.data_processor import list_uploaded_files, get_dataframe
from utils.templates import get_industry_templates, apply_template
from utils.visualization import render_visualization

st.set_page_config(
    page_title="Industry Templates - DataVizSME",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Industry Templates")
st.write("Pre-built visualization templates tailored to common business needs")

# Initialize session state
if 'current_file' not in st.session_state:
    st.session_state.current_file = None
if 'visualizations' not in st.session_state:
    st.session_state.visualizations = {}

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

# Industry selection
industries = [
    "Retail & E-commerce",
    "Financial Services",
    "Manufacturing",
    "Healthcare",
    "Professional Services",
    "Hospitality & Food Service",
    "Real Estate & Construction"
]

selected_industry = st.selectbox("Select your industry:", industries)

# Get templates for selected industry
templates = get_industry_templates(selected_industry)

# Display templates
if not templates:
    st.info(f"No templates available for {selected_industry} yet.")
else:
    # Display as cards in a grid
    st.subheader(f"Available Templates for {selected_industry}")
    
    # Use columns to create a grid layout
    cols = st.columns(2)
    
    for i, template in enumerate(templates):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(template['name'])
                st.write(template['description'])
                st.write(f"**Required fields:** {', '.join(template['required_fields'])}")
                
                # Check if dataset has required fields
                missing_fields = [field for field in template['required_fields'] 
                                 if not any(col.lower().replace('_', ' ').replace('-', ' ') == field.lower().replace('_', ' ').replace('-', ' ') 
                                           for col in df.columns)]
                
                if missing_fields:
                    st.warning(f"Missing fields: {', '.join(missing_fields)}")
                    st.info("To use this template, your dataset needs to have fields with similar names or you'll need to map your fields to the template.")
                    can_use = False
                else:
                    st.success("Your dataset has all required fields!")
                    can_use = True
                
                if st.button(f"Use Template: {template['name']}", key=f"use_template_{i}", disabled=not can_use):
                    st.session_state.selected_template = template
                    st.rerun()

# If a template is selected, show the mapping and preview
if 'selected_template' in st.session_state:
    template = st.session_state.selected_template
    
    st.markdown("---")
    st.subheader(f"Applying Template: {template['name']}")
    
    # Field mapping (if needed)
    st.write("### Map Your Data Fields")
    st.write("Match your dataset columns to the template's required fields")
    
    field_mapping = {}
    for required_field in template['required_fields']:
        # Try to find closest match in dataset
        matches = [col for col in df.columns 
                  if col.lower().replace('_', ' ').replace('-', ' ') == required_field.lower().replace('_', ' ').replace('-', ' ')]
        
        default_value = matches[0] if matches else None
        field_mapping[required_field] = st.selectbox(
            f"Map '{required_field}' to:", 
            options=[""] + list(df.columns),
            index=0 if default_value is None else list(df.columns).index(default_value) + 1
        )
    
    # Check if all fields are mapped
    all_mapped = all(field_mapping.values())
    
    if not all_mapped:
        st.warning("Please map all required fields to continue.")
    else:
        # Apply template and show preview
        try:
            visualizations = apply_template(template, df, field_mapping)
            
            st.write("### Template Preview")
            
            # Display each visualization from the template
            for i, viz in enumerate(visualizations):
                st.write(f"#### {viz['title']}")
                
                try:
                    fig = render_visualization(df, viz['config'])
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error rendering visualization: {str(e)}")
            
            # Save template option
            if st.button("Save All Template Visualizations"):
                for viz in visualizations:
                    viz_name = f"{template['name']} - {viz['title']}"
                    st.session_state.visualizations[viz_name] = viz['config']
                
                st.success(f"Saved {len(visualizations)} visualizations from the {template['name']} template!")
                
        except Exception as e:
            st.error(f"Error applying template: {str(e)}")
    
    # Option to clear selected template
    if st.button("Cancel Template Application"):
        del st.session_state.selected_template
        st.rerun()

# Information about templates
with st.expander("About Industry Templates"):
    st.write("""
    ### What are Industry Templates?
    
    Industry templates are pre-designed sets of visualizations tailored to common business needs in specific industries. 
    They help you quickly create meaningful insights without having to design each visualization from scratch.
    
    ### Benefits of Using Templates:
    
    - **Save Time**: Get started with analytics faster
    - **Industry Best Practices**: Leverage proven visualization approaches
    - **Comprehensive View**: See multiple dimensions of your data at once
    - **Consistent Reporting**: Establish standardized reporting formats
    
    ### How to Use Templates:
    
    1. Select your industry
    2. Choose a template that matches your business needs
    3. Map your data fields to the template requirements
    4. Save the visualizations to your dashboard
    
    ### Template Types Available:
    
    - **Performance Dashboards**: Track KPIs and overall business performance
    - **Trend Analysis**: Visualize changes and patterns over time
    - **Comparative Analysis**: Compare different segments, products, or time periods
    - **Distribution Analysis**: Understand the spread and composition of your data
    """)
