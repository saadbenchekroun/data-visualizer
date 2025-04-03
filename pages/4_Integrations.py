import streamlit as st
import pandas as pd
import json
from utils.integration import get_available_integrations, setup_integration, get_integration_data
from utils.data_processor import save_dataframe

st.set_page_config(
    page_title="Integrations - DataVizSME",
    page_icon="🔗",
    layout="wide"
)

st.title("🔗 External Integrations")
st.write("Connect to external business tools and import data directly")

# Initialize session state
if 'active_integrations' not in st.session_state:
    st.session_state.active_integrations = {}
if 'integration_data' not in st.session_state:
    st.session_state.integration_data = {}
    
# Get available integrations
available_integrations = get_available_integrations()

# Create tabs for setup and management
tab1, tab2 = st.tabs(["Available Integrations", "Manage Integrations"])

# Available Integrations Tab
with tab1:
    st.subheader("Connect to Business Tools")
    
    # Display available integrations in a grid
    st.write("Select a tool to connect with:")
    
    # Create three columns for the grid
    cols = st.columns(3)
    
    for i, integration in enumerate(available_integrations):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(integration['name'])
                st.write(integration['description'])
                
                # Check if already connected
                is_connected = integration['id'] in st.session_state.active_integrations
                
                if is_connected:
                    st.success("Connected")
                    if st.button(f"Manage Connection", key=f"manage_{integration['id']}"):
                        st.session_state.selected_integration = integration
                        st.session_state.integration_action = "manage"
                        st.rerun()
                else:
                    if st.button(f"Connect", key=f"connect_{integration['id']}"):
                        st.session_state.selected_integration = integration
                        st.session_state.integration_action = "setup"
                        st.rerun()

# Manage Integrations Tab
with tab2:
    st.subheader("Manage Your Connected Tools")
    
    if not st.session_state.active_integrations:
        st.info("No integrations are currently active. Connect to tools in the Available Integrations tab.")
    else:
        # Display active integrations and their status
        st.write("Your connected tools:")
        
        for integration_id, status in st.session_state.active_integrations.items():
            # Find the integration details
            integration_details = next((i for i in available_integrations if i['id'] == integration_id), None)
            
            if integration_details:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader(integration_details['name'])
                        st.write(f"Status: {status['status']}")
                        if 'last_sync' in status:
                            st.write(f"Last synchronized: {status['last_sync']}")
                        
                    with col2:
                        if st.button("Sync Data", key=f"sync_{integration_id}"):
                            try:
                                # Get data from integration
                                data = get_integration_data(integration_id, st.session_state.active_integrations[integration_id])
                                
                                if data and all(key in data for key in ['filename', 'data']):
                                    # Save the data as a dataframe
                                    df = pd.DataFrame(data['data'])
                                    save_dataframe(data['filename'], df)
                                    
                                    # Update status
                                    st.session_state.active_integrations[integration_id]['status'] = 'Connected'
                                    st.session_state.active_integrations[integration_id]['last_sync'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                                    
                                    st.success(f"Data from {integration_details['name']} has been synchronized!")
                                    st.rerun()
                                else:
                                    st.error("Received invalid data format from integration")
                            except Exception as e:
                                st.error(f"Error synchronizing data: {str(e)}")
                        
                        if st.button("Disconnect", key=f"disconnect_{integration_id}"):
                            # Confirm disconnection
                            if st.checkbox(f"Confirm disconnection from {integration_details['name']}?", key=f"confirm_{integration_id}"):
                                del st.session_state.active_integrations[integration_id]
                                st.success(f"Disconnected from {integration_details['name']}")
                                st.rerun()

# Handle integration setup/management if selected
if 'selected_integration' in st.session_state and 'integration_action' in st.session_state:
    integration = st.session_state.selected_integration
    action = st.session_state.integration_action
    
    st.markdown("---")
    
    if action == "setup":
        st.subheader(f"Connect to {integration['name']}")
        st.write(integration['setup_instructions'])
        
        # Display authentication fields based on integration type
        auth_fields = {}
        
        if integration['auth_type'] == 'api_key':
            auth_fields['api_key'] = st.text_input("API Key", type="password")
            
        elif integration['auth_type'] == 'oauth':
            st.info("This integration requires OAuth authentication. Click the button below to authorize.")
            if st.button("Authorize"):
                # In a real app, this would redirect to the OAuth flow
                # For this demo, we'll simulate successful authorization
                auth_fields['oauth_token'] = "simulated_oauth_token"
                auth_fields['oauth_secret'] = "simulated_oauth_secret"
                st.success("Authorization successful!")
                
        elif integration['auth_type'] == 'credentials':
            auth_fields['username'] = st.text_input("Username")
            auth_fields['password'] = st.text_input("Password", type="password")
            
        # Additional configuration fields
        st.subheader("Configuration")
        
        if 'config_fields' in integration:
            for field in integration['config_fields']:
                if field['type'] == 'text':
                    auth_fields[field['id']] = st.text_input(field['label'], placeholder=field.get('placeholder', ''))
                elif field['type'] == 'select':
                    auth_fields[field['id']] = st.selectbox(field['label'], field['options'])
                elif field['type'] == 'number':
                    auth_fields[field['id']] = st.number_input(field['label'], min_value=field.get('min', 0))
        
        # Connect button
        if st.button("Connect to Service"):
            # Validate required fields
            required_fields = integration.get('required_fields', [])
            missing_fields = [field for field in required_fields if field not in auth_fields or not auth_fields[field]]
            
            if missing_fields:
                st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
            else:
                try:
                    # Set up the integration
                    result = setup_integration(integration['id'], auth_fields)
                    
                    if result['success']:
                        # Store connection info
                        st.session_state.active_integrations[integration['id']] = {
                            'status': 'Connected',
                            'auth': auth_fields,
                            'last_sync': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                        }
                        
                        st.success(f"Successfully connected to {integration['name']}!")
                        
                        # Clean up session state
                        del st.session_state.selected_integration
                        del st.session_state.integration_action
                        
                        st.rerun()
                    else:
                        st.error(f"Connection failed: {result['message']}")
                except Exception as e:
                    st.error(f"Error setting up integration: {str(e)}")
        
        # Cancel button
        if st.button("Cancel"):
            del st.session_state.selected_integration
            del st.session_state.integration_action
            st.rerun()
            
    elif action == "manage":
        st.subheader(f"Manage {integration['name']} Connection")
        
        # Display connection details
        connection_info = st.session_state.active_integrations[integration['id']]
        
        st.write(f"Status: {connection_info['status']}")
        if 'last_sync' in connection_info:
            st.write(f"Last synchronized: {connection_info['last_sync']}")
        
        # Data sync options
        st.subheader("Data Synchronization")
        
        # For demo purposes, show some dummy data options based on the integration type
        if integration['id'] == 'quickbooks':
            data_types = ["Invoices", "Expenses", "Profit & Loss", "Balance Sheet", "Sales by Customer"]
        elif integration['id'] == 'shopify':
            data_types = ["Orders", "Products", "Customers", "Inventory", "Sales by Product"]
        elif integration['id'] == 'google_analytics':
            data_types = ["Website Traffic", "User Behavior", "Conversion Rates", "Referrers", "Page Performance"]
        else:
            data_types = ["All Data"]
        
        selected_data = st.multiselect("Select data to import:", data_types, default=data_types[0])
        
        date_range = st.date_input("Date range:", value=[pd.Timestamp.now() - pd.Timedelta(days=30), pd.Timestamp.now()])
        
        if st.button("Sync Selected Data"):
            if not selected_data:
                st.warning("Please select at least one data type to import.")
            else:
                try:
                    # Get data from integration
                    with st.spinner(f"Syncing data from {integration['name']}..."):
                        # Simulate API call delay
                        import time
                        time.sleep(2)
                        
                        # For each selected data type, create a mock dataset
                        for data_type in selected_data:
                            # Generate a sensible filename
                            filename = f"{integration['id']}_{data_type.lower().replace(' ', '_').replace('&', 'and')}.csv"
                            
                            # Generate mock data based on the data type
                            mock_data = get_integration_data(
                                integration['id'], 
                                connection_info, 
                                data_type=data_type, 
                                start_date=date_range[0], 
                                end_date=date_range[1]
                            )
                            
                            if mock_data and 'data' in mock_data:
                                # Save the data as a dataframe
                                df = pd.DataFrame(mock_data['data'])
                                save_dataframe(filename, df)
                                
                                st.success(f"Imported {len(df)} records of {data_type} data from {integration['name']}")
                            else:
                                st.warning(f"No {data_type} data available for the selected period")
                        
                        # Update the last sync time
                        st.session_state.active_integrations[integration['id']]['last_sync'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                        
                except Exception as e:
                    st.error(f"Error synchronizing data: {str(e)}")
        
        # Disconnect option
        st.subheader("Connection Management")
        
        if st.button("Disconnect from Service"):
            # Confirm disconnection
            if st.checkbox(f"Confirm disconnection from {integration['name']}?"):
                del st.session_state.active_integrations[integration['id']]
                st.success(f"Disconnected from {integration['name']}")
                
                # Clean up session state
                del st.session_state.selected_integration
                del st.session_state.integration_action
                
                st.rerun()
        
        # Go back button
        if st.button("Back to Integrations"):
            del st.session_state.selected_integration
            del st.session_state.integration_action
            st.rerun()
