import streamlit as st
import pandas as pd
import io
import os
from utils.data_processor import save_dataframe, list_uploaded_files, get_dataframe, delete_dataframe

st.set_page_config(
    page_title="Data Upload - DataVizSME",
    page_icon="📤",
    layout="wide"
)

st.title("📤 Data Upload")
st.write("Upload your business data files or connect to external data sources")

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}

tab1, tab2, tab3 = st.tabs(["File Upload", "Sample Data", "Manage Data"])

# File Upload Tab
with tab1:
    st.subheader("Upload Data Files")
    
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel files", 
        type=["csv", "xlsx", "xls"],
        help="Supported formats: CSV, Excel (.xlsx, .xls)"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        file_name = st.text_input("Save file as (optional):", 
                                  placeholder="Leave blank to use original filename")
    
    with col2:
        file_format = st.selectbox("File format:", ["Auto-detect", "CSV", "Excel"])
    
    if uploaded_file is not None:
        try:
            # Determine file format
            if file_format == "Auto-detect":
                if uploaded_file.name.lower().endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            elif file_format == "CSV":
                df = pd.read_csv(uploaded_file)
            else:  # Excel
                df = pd.read_excel(uploaded_file)
            
            # Save with custom name if provided
            if file_name:
                save_name = file_name
            else:
                save_name = uploaded_file.name
                
            # Preview data
            st.subheader(f"Preview of {save_name}")
            st.dataframe(df.head(10))
            
            # Show data statistics
            st.subheader("Data Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Rows: {df.shape[0]}")
                st.write(f"Columns: {df.shape[1]}")
            with col2:
                st.write(f"Missing values: {df.isna().sum().sum()}")
                st.write(f"Duplicate rows: {df.duplicated().sum()}")
            
            # Save button
            if st.button("Save Dataset"):
                save_dataframe(save_name, df)
                st.success(f"Dataset '{save_name}' has been successfully saved!")
                st.session_state.current_file = save_name
        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.info("Please check that your file is properly formatted and try again.")

# Sample Data Tab
with tab2:
    st.subheader("Sample Datasets")
    st.write("Don't have data ready? Use one of our sample datasets to explore the platform capabilities.")
    
    sample_data = {
        "Retail Sales": "Retail transactions with customer demographics and product categories",
        "Inventory Management": "Stock levels, reorder points, and inventory turnover data",
        "Financial Performance": "Revenue, expenses, and profit metrics over time",
        "Marketing Campaign": "Campaign performance metrics including ROI and conversion rates",
        "Customer Feedback": "Customer satisfaction scores and feedback categories"
    }
    
    selected_sample = st.selectbox("Choose a sample dataset:", list(sample_data.keys()))
    
    if selected_sample:
        st.info(sample_data[selected_sample])
        
        if st.button("Load Sample Dataset"):
            # Generate appropriate sample data based on selection
            if selected_sample == "Retail Sales":
                # Create realistic retail sales data
                data = {
                    "Date": pd.date_range(start="2023-01-01", periods=100),
                    "Product_Category": pd.Series(["Electronics", "Clothing", "Home Goods", "Groceries", "Beauty"]).sample(100, replace=True).values,
                    "Customer_Age": pd.Series(range(18, 75)).sample(100, replace=True).values,
                    "Customer_Gender": pd.Series(["Male", "Female", "Non-Binary"]).sample(100, replace=True, weights=[0.48, 0.48, 0.04]).values,
                    "Sale_Amount": (pd.Series(range(10, 500)) * pd.Series([0.1, 1, 10]).sample(100, replace=True)).values.round(2),
                    "Items_Purchased": pd.Series(range(1, 10)).sample(100, replace=True).values,
                }
                df = pd.DataFrame(data)
                
            elif selected_sample == "Inventory Management":
                data = {
                    "Product_ID": [f"PROD{i:04d}" for i in range(1, 101)],
                    "Product_Name": [f"Product {i}" for i in range(1, 101)],
                    "Category": pd.Series(["Electronics", "Clothing", "Home Goods", "Office", "Food"]).sample(100, replace=True).values,
                    "Stock_Level": pd.Series(range(0, 500)).sample(100, replace=True).values,
                    "Reorder_Point": pd.Series(range(5, 100)).sample(100, replace=True).values,
                    "Lead_Time_Days": pd.Series(range(1, 30)).sample(100, replace=True).values,
                    "Cost_Per_Unit": (pd.Series(range(5, 200)) * pd.Series([0.1, 1, 10]).sample(100, replace=True)).values.round(2),
                }
                df = pd.DataFrame(data)
                
            elif selected_sample == "Financial Performance":
                data = {
                    "Month": pd.date_range(start="2020-01-01", periods=36, freq="M"),
                    "Revenue": (pd.Series(range(10000, 50000)) + pd.Series(range(0, 36)) * 500).values,
                    "Cost_of_Goods": (pd.Series(range(5000, 25000)) + pd.Series(range(0, 36)) * 200).values,
                    "Operating_Expenses": pd.Series(range(2000, 10000)).sample(36, replace=True).values,
                    "Marketing_Spend": pd.Series(range(1000, 5000)).sample(36, replace=True).values,
                    "Department": pd.Series(["Sales", "Marketing", "Operations", "IT"]).sample(36, replace=True).values
                }
                df = pd.DataFrame(data)
                df["Profit"] = df["Revenue"] - df["Cost_of_Goods"] - df["Operating_Expenses"] - df["Marketing_Spend"]
                
            elif selected_sample == "Marketing Campaign":
                data = {
                    "Campaign_ID": [f"CAMP{i:03d}" for i in range(1, 51)],
                    "Campaign_Type": pd.Series(["Email", "Social Media", "Search", "Display", "Content"]).sample(50, replace=True).values,
                    "Start_Date": pd.date_range(start="2022-01-01", periods=50, freq="W"),
                    "Budget": pd.Series(range(1000, 10000, 500)).sample(50, replace=True).values,
                    "Impressions": pd.Series(range(1000, 100000, 1000)).sample(50, replace=True).values,
                    "Clicks": pd.Series(range(50, 5000, 50)).sample(50, replace=True).values,
                    "Conversions": pd.Series(range(1, 500, 10)).sample(50, replace=True).values,
                }
                df = pd.DataFrame(data)
                df["CTR"] = (df["Clicks"] / df["Impressions"] * 100).round(2)
                df["Conversion_Rate"] = (df["Conversions"] / df["Clicks"] * 100).round(2)
                df["Cost_Per_Conversion"] = (df["Budget"] / df["Conversions"]).round(2)
                
            elif selected_sample == "Customer Feedback":
                data = {
                    "Date": pd.date_range(start="2023-01-01", periods=200),
                    "Customer_ID": [f"CUST{i:04d}" for i in range(1, 201)],
                    "Product_Purchased": pd.Series(["Product A", "Product B", "Product C", "Product D"]).sample(200, replace=True).values,
                    "Satisfaction_Score": pd.Series(range(1, 6)).sample(200, replace=True).values,
                    "Feedback_Category": pd.Series(["Quality", "Price", "Service", "Usability", "Delivery"]).sample(200, replace=True).values,
                    "Recommendation_Likely": pd.Series(range(1, 11)).sample(200, replace=True).values,
                }
                df = pd.DataFrame(data)
            
            # Save the dataset
            filename = f"{selected_sample.replace(' ', '_')}_Sample.csv"
            save_dataframe(filename, df)
            st.success(f"Sample dataset '{selected_sample}' has been loaded as '{filename}'")
            st.session_state.current_file = filename
            
            # Preview data
            st.subheader("Data Preview")
            st.dataframe(df.head(10))

# Manage Data Tab
with tab3:
    st.subheader("Manage Datasets")
    
    available_files = list_uploaded_files()
    
    if not available_files:
        st.info("No datasets uploaded yet. Use the File Upload tab to add data.")
    else:
        selected_file = st.selectbox("Select a dataset to manage:", available_files)
        
        if selected_file:
            try:
                df = get_dataframe(selected_file)
                
                # Dataset actions
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Rows", df.shape[0])
                    st.metric("Columns", df.shape[1])
                
                with col2:
                    if st.button("Set as Active Dataset"):
                        st.session_state.current_file = selected_file
                        st.success(f"{selected_file} set as the active dataset")
                        
                    if st.button("Delete Dataset", type="primary", help="This action cannot be undone"):
                        delete_dataframe(selected_file)
                        if st.session_state.current_file == selected_file:
                            st.session_state.current_file = None
                        st.success(f"Dataset {selected_file} has been deleted")
                        st.rerun()
                
                # Display dataset info
                st.subheader("Dataset Preview")
                st.dataframe(df.head(10))
                
                # Column info
                st.subheader("Column Information")
                col_info = pd.DataFrame({
                    "Data Type": df.dtypes,
                    "Non-Null Values": df.count(),
                    "Null Values": df.isna().sum(),
                    "Unique Values": [df[col].nunique() for col in df.columns]
                })
                st.dataframe(col_info)
                
            except Exception as e:
                st.error(f"Error loading dataset: {str(e)}")
