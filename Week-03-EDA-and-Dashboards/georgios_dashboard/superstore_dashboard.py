#!/usr/bin/env python3
"""
Superstore Business Analytics Dashboard

A simple, educational dashboard that transforms retail data into business insights.
Students will learn how to use data analytics to answer real business questions.

Author: Georgios Ioannou
Date: 2025
"""

# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Superstore Business Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_processed_data():
    """
    Load all processed datasets for the dashboard.
    Returns a dictionary containing all the data we need.
    """
    data = {}
    
    # Load all CSV files from processed_data directory
    csv_files = [
        'geographic_data.csv',
        'yearly_data.csv', 
        'monthly_data.csv',
        'category_data.csv',
        'subcategory_data.csv',
        'segment_data.csv',
        'ship_mode_data.csv'
    ]
    
    for file in csv_files:
        file_path = f"processed_data/{file}"
        if os.path.exists(file_path):
            # Extract name from filename (remove _data.csv)
            name = file.replace('_data.csv', '')
            data[name] = pd.read_csv(file_path)
    
    # Load business KPIs from JSON file
    kpis_file = "processed_data/business_kpis.json"
    if os.path.exists(kpis_file):
        with open(kpis_file, 'r') as f:
            data['kpis'] = json.load(f)
    
    # Load raw data for filtering (if available)
    raw_data_file = "superstore_data.csv"
    if os.path.exists(raw_data_file):
        raw_data = pd.read_csv(raw_data_file)
        # Convert date columns to datetime
        date_columns = ['Order Date', 'Ship Date']
        for col in date_columns:
            if col in raw_data.columns:
                raw_data[col] = pd.to_datetime(raw_data[col], errors='coerce')
        
        # Extract year for filtering
        if 'Order Date' in raw_data.columns:
            raw_data['Order Year'] = raw_data['Order Date'].dt.year
        
        data['raw_data'] = raw_data
    
    # Show simple loading status
    if data:
        st.sidebar.success("✅ Data loaded")
    
    return data

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_currency(amount):
    """
    Format numbers as currency for better display.
    """
    if amount >= 1000000:
        return f"${amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"${amount/1000:.1f}K"
    else:
        return f"${amount:.0f}"

def format_percentage(value):
    """
    Format numbers as percentages.
    """
    return f"{value:.1f}%"

def filter_data(data, selected_year=None, selected_regions=None, selected_categories=None):
    """
    Filter the data based on selected filters.
    Returns filtered datasets and updated KPIs.
    """
    filtered_data = {}
    
    # Start with original data
    for key in data.keys():
        if key != 'kpis':
            filtered_data[key] = data[key].copy()
    
    # Apply year filter to yearly data
    if 'yearly' in filtered_data and selected_year:
        filtered_data['yearly'] = filtered_data['yearly'][
            filtered_data['yearly']['Order Year'] == selected_year
        ].copy()
    
    # Apply category filter to category data
    if 'category' in filtered_data and selected_categories:
        filtered_data['category'] = filtered_data['category'][
            filtered_data['category']['Category'].isin(selected_categories)
        ].copy()
    
    # Recalculate segment data if filters are applied
    if (selected_year or selected_regions or selected_categories) and 'raw_data' in data:
        # Start with raw data
        raw_data = data['raw_data']
        filtered_raw = raw_data.copy()
        
        # Apply year filter
        if selected_year:
            filtered_raw = filtered_raw[filtered_raw['Order Year'] == selected_year]
        
        # Apply region filter
        if selected_regions:
            filtered_raw = filtered_raw[filtered_raw['Region'].isin(selected_regions)]
        
        # Apply category filter
        if selected_categories:
            filtered_raw = filtered_raw[filtered_raw['Category'].isin(selected_categories)]
        
        # Recalculate segment data from filtered raw data
        if not filtered_raw.empty:
            segment_by_filters = filtered_raw.groupby('Segment').agg({
                'Sales': ['sum', 'mean'],
                'Order ID': 'nunique',
                'Customer ID': 'nunique'
            }).reset_index()
            
            # Flatten column names
            segment_by_filters.columns = ['Segment', 'Total_Sales', 'Avg_Sales', 'Order_Count', 'Customer_Count']
            
            # Add sales per order
            segment_by_filters['Sales_Per_Order'] = segment_by_filters['Total_Sales'] / segment_by_filters['Order_Count']
            
            # Add percentage of total sales
            total_sales = segment_by_filters['Total_Sales'].sum()
            segment_by_filters['Sales_Percentage'] = (segment_by_filters['Total_Sales'] / total_sales * 100) if total_sales > 0 else 0
            
            filtered_data['segment'] = segment_by_filters
        else:
            # No data for selected filters
            filtered_data['segment'] = pd.DataFrame()
    
    # Recalculate geographic data if year filter is applied
    if selected_year and 'raw_data' in data:
        # Filter raw data by year
        raw_data = data['raw_data']
        year_filtered = raw_data[raw_data['Order Year'] == selected_year]
        
        # Apply region filter
        if selected_regions:
            year_filtered = year_filtered[year_filtered['Region'].isin(selected_regions)]
        
        # Apply category filter
        if selected_categories:
            year_filtered = year_filtered[year_filtered['Category'].isin(selected_categories)]
        
        # Recalculate geographic data from filtered raw data
        if not year_filtered.empty:
            geographic_by_year = year_filtered.groupby(['State', 'Region']).agg({
                'Sales': ['sum', 'mean'],
                'Order ID': 'nunique',
                'Customer ID': 'nunique'
            }).reset_index()
            
            # Flatten column names
            geographic_by_year.columns = ['State', 'Region', 'Total_Sales', 'Avg_Sales', 'Order_Count', 'Customer_Count']
            
            # Add state codes
            state_code_mapping = {
                'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
                'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
                'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
                'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
                'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
                'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
                'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
                'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
                'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
                'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
                'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
            }
            geographic_by_year['states_code'] = geographic_by_year['State'].map(state_code_mapping)
            
            # Add sales per order
            geographic_by_year['Sales_Per_Order'] = geographic_by_year['Total_Sales'] / geographic_by_year['Order_Count']
            
            filtered_data['geographic'] = geographic_by_year
        else:
            # No data for selected filters
            filtered_data['geographic'] = pd.DataFrame()
    else:
        # Apply region filter to original geographic data (when no year filter)
        if 'geographic' in filtered_data and selected_regions:
            filtered_data['geographic'] = filtered_data['geographic'][
                filtered_data['geographic']['Region'].isin(selected_regions)
            ].copy()
    
    # Recalculate KPIs based on filtered data
    # Use the most restrictive filter to calculate KPIs
    kpi_data = filtered_data['geographic'].copy()
    
    # Apply year filter to KPI calculation if year is selected
    if selected_year and 'raw_data' in data:
        # We need to filter the raw data by year and recalculate
        raw_data = data['raw_data']
        year_filtered = raw_data[raw_data['Order Year'] == selected_year]
        
        # Apply region filter
        if selected_regions:
            year_filtered = year_filtered[year_filtered['Region'].isin(selected_regions)]
        
        # Apply category filter
        if selected_categories:
            year_filtered = year_filtered[year_filtered['Category'].isin(selected_categories)]
        
        # Calculate KPIs from filtered raw data
        total_sales = year_filtered['Sales'].sum()
        total_orders = year_filtered['Order ID'].nunique()
        total_customers = year_filtered['Customer ID'].nunique()
        
        filtered_kpis = {
            'total_sales': total_sales,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'avg_order_value': total_sales / total_orders if total_orders > 0 else 0,
            'avg_orders_per_customer': total_orders / total_customers if total_customers > 0 else 0,
            'avg_sales_per_customer': total_sales / total_customers if total_customers > 0 else 0
        }
        
        # Calculate top region from filtered data
        if selected_regions:
            region_sales = year_filtered.groupby('Region')['Sales'].sum()
            if not region_sales.empty:
                filtered_kpis['top_region'] = region_sales.idxmax()
                filtered_kpis['top_region_sales'] = region_sales.max()
            else:
                filtered_kpis['top_region'] = 'N/A'
                filtered_kpis['top_region_sales'] = 0
        else:
            # Use geographic data for top region
            if filtered_data['geographic'].shape[0] > 0:
                filtered_kpis['top_region'] = filtered_data['geographic']['Region'].mode().iloc[0]
                filtered_kpis['top_region_sales'] = filtered_data['geographic']['Total_Sales'].max()
            else:
                filtered_kpis['top_region'] = 'N/A'
                filtered_kpis['top_region_sales'] = 0
        
        # Keep original growth rate for comparison
        if 'kpis' in data:
            filtered_kpis['total_growth_rate'] = data['kpis'].get('total_growth_rate', 0)
    
    else:
        # Use geographic data for KPIs (when no year filter)
        if filtered_data['geographic'].shape[0] > 0:
            total_sales = filtered_data['geographic']['Total_Sales'].sum()
            total_orders = filtered_data['geographic']['Order_Count'].sum()
            
            filtered_kpis = {
                'total_sales': total_sales,
                'total_orders': total_orders,
                'avg_order_value': total_sales / total_orders if total_orders > 0 else 0,
                'top_region': filtered_data['geographic']['Region'].mode().iloc[0] if filtered_data['geographic'].shape[0] > 0 else 'N/A',
                'top_region_sales': filtered_data['geographic']['Total_Sales'].max() if filtered_data['geographic'].shape[0] > 0 else 0
            }
            
            # Add original KPIs for comparison
            if 'kpis' in data:
                filtered_kpis['total_growth_rate'] = data['kpis'].get('total_growth_rate', 0)
                filtered_kpis['total_customers'] = data['kpis'].get('total_customers', 0)
                filtered_kpis['avg_orders_per_customer'] = data['kpis'].get('avg_orders_per_customer', 0)
        else:
            filtered_kpis = data.get('kpis', {})
    
    filtered_data['kpis'] = filtered_kpis
    return filtered_data

# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def create_sales_map(geographic_data, selected_year=None):
    """
    Create a choropleth map showing sales by state.
    This helps answer: "Which states have the highest sales?"
    """
    # Ensure we have data to plot
    if geographic_data.empty:
        return None
    
    # Create title with year information
    if selected_year:
        title_text = f'Sales by State - Geographic Performance ({selected_year})'
    else:
        title_text = 'Sales by State - Geographic Performance (All Years)'
    
    # Create the choropleth map using px.choropleth like in streamlit_app.py
    fig = px.choropleth(
        geographic_data, 
        locations='states_code',  # Use state codes like the working example
        color='Total_Sales', 
        locationmode="USA-states",
        color_continuous_scale='Blues',
        range_color=(geographic_data['Total_Sales'].min(), geographic_data['Total_Sales'].max()),
        scope="usa",
        labels={'Total_Sales':'Total Sales ($)'}
    )
    
    # Update layout like in streamlit_app.py
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=50, b=0),
        height=500,
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    return fig

def create_sales_trend(yearly_data):
    """
    Create a line chart showing sales trends over time.
    This helps answer: "What's our sales trend over the past 4 years?"
    """
    fig = px.line(
        yearly_data,
        x='Order Year',
        y='Total_Sales',
        title='Sales Trend Over Time',
        markers=True
    )
    
    # Add growth rate annotations
    for i, row in yearly_data.iterrows():
        if pd.notna(row['Sales_Growth']):
            fig.add_annotation(
                x=row['Order Year'],
                y=row['Total_Sales'],
                text=f"{row['Sales_Growth']:.1f}%",
                showarrow=True,
                arrowhead=1,
                yshift=10
            )
    
    fig.update_layout(
        title_x=0.5,
        height=400,
        xaxis_title="Year",
        yaxis_title="Total Sales ($)"
    )
    
    return fig

def create_category_chart(category_data):
    """
    Create a bar chart showing sales by product category.
    This helps answer: "What are our best-selling product categories?"
    """
    fig = px.bar(
        category_data,
        x='Category',
        y='Total_Sales',
        color='Category',
        title='Sales by Product Category',
        text='Total_Sales',
        hover_data=['Market_Share', 'Order_Count']
    )
    
    # Format the text labels
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    
    fig.update_layout(
        title_x=0.5,
        height=400,
        xaxis_title="Product Category",
        yaxis_title="Total Sales ($)",
        showlegend=False
    )
    
    return fig

def create_segment_chart(segment_data):
    """
    Create a bar chart showing sales by customer segment.
    This helps answer: "Which customer segments are most valuable?"
    """
    # Check if Sales_Per_Customer column exists, if not calculate it
    if 'Sales_Per_Customer' not in segment_data.columns and 'Customer_Count' in segment_data.columns:
        segment_data = segment_data.copy()
        segment_data['Sales_Per_Customer'] = segment_data['Total_Sales'] / segment_data['Customer_Count']
    
    # Use available columns for hover data
    hover_columns = []
    if 'Sales_Per_Customer' in segment_data.columns:
        hover_columns.append('Sales_Per_Customer')
    if 'Customer_Count' in segment_data.columns:
        hover_columns.append('Customer_Count')
    if 'Order_Count' in segment_data.columns:
        hover_columns.append('Order_Count')
    
    fig = px.bar(
        segment_data,
        x='Segment',
        y='Total_Sales',
        color='Segment',
        title='Sales by Customer Segment',
        text='Total_Sales',
        hover_data=hover_columns
    )
    
    # Format the text labels
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    
    fig.update_layout(
        title_x=0.5,
        height=400,
        xaxis_title="Customer Segment",
        yaxis_title="Total Sales ($)",
        showlegend=False
    )
    
    return fig

def create_region_comparison(geographic_data):
    """
    Create a bar chart comparing regions.
    This helps answer: "Which regions are performing best?"
    """
    # Aggregate by region
    region_data = geographic_data.groupby('Region').agg({
        'Total_Sales': 'sum',
        'Order_Count': 'sum'
    }).reset_index()
    
    fig = px.bar(
        region_data,
        x='Region',
        y='Total_Sales',
        color='Region',
        title='Sales by Region',
        text='Total_Sales',
        hover_data=['Order_Count']
    )
    
    # Format the text labels
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    
    fig.update_layout(
        title_x=0.5,
        height=400,
        xaxis_title="Region",
        yaxis_title="Total Sales ($)",
        showlegend=False
    )
    
    return fig

def create_sales_heatmap(raw_data, selected_year=None):
    """
    Create a heatmap showing sales by category and region.
    This helps answer: "Which category-region combinations perform best?"
    """
    # Filter data by year if specified
    if selected_year:
        data = raw_data[raw_data['Order Year'] == selected_year]
    else:
        data = raw_data
    
    # Create pivot table for heatmap
    heatmap_data = data.groupby(['Category', 'Region'])['Sales'].sum().reset_index()
    pivot_data = heatmap_data.pivot(index='Category', columns='Region', values='Sales').fillna(0)
    
    # Create heatmap
    fig = px.imshow(
        pivot_data,
        title='Sales Heatmap: Category vs Region',
        labels=dict(x="Region", y="Category", color="Sales ($)"),
        color_continuous_scale='Blues',
        aspect="auto"
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        height=400,
        xaxis_title="Region",
        yaxis_title="Category"
    )
    
    return fig

# =============================================================================
# MAIN DASHBOARD
# =============================================================================

def main():
    """
    Main dashboard function - this is where everything comes together.
    """
    
    # =============================================================================
    # HEADER SECTION
    # =============================================================================
    st.title("🛒 Superstore Business Analytics Dashboard")
    st.markdown("---")
    
    # =============================================================================
    # SIDEBAR - FILTERS AND CONTROLS
    # =============================================================================
    
    # Load data
    st.sidebar.subheader("📊 Data Loading")
    data = load_processed_data()
    
    if not data:
        st.error("❌ No data found! Please run the data processor first.")
        st.stop()
    
    # Year filter
    st.sidebar.subheader("📅 Time Filter")
    if 'yearly' in data:
        available_years = sorted(data['yearly']['Order Year'].unique())
        
        # Initialize session state for year filter
        if 'selected_year' not in st.session_state:
            st.session_state.selected_year = None
        
        # Add "All Years" option
        year_options = ["All Years"] + available_years
        
        selected_year = st.sidebar.selectbox(
            "Select Year:",
            year_options,
            index=0 if st.session_state.selected_year is None else (0 if st.session_state.selected_year == "All Years" else year_options.index(st.session_state.selected_year)),
            key='year_selectbox'
        )
        
        # Convert "All Years" to None for processing
        if selected_year == "All Years":
            selected_year = None
        st.session_state.selected_year = selected_year
    else:
        selected_year = None
    
    # Region filter
    st.sidebar.subheader("🌍 Region Filter")
    if 'geographic' in data:
        available_regions = sorted(data['geographic']['Region'].unique())
        
        # Initialize session state for region filter
        if 'selected_regions' not in st.session_state:
            st.session_state.selected_regions = available_regions
        
        selected_regions = st.sidebar.multiselect(
            "Select Regions:",
            available_regions,
            default=st.session_state.selected_regions,
            key='region_multiselect'
        )
        st.session_state.selected_regions = selected_regions
    else:
        selected_regions = []
    
    # Category filter
    st.sidebar.subheader("📦 Category Filter")
    if 'category' in data:
        available_categories = sorted(data['category']['Category'].unique())
        
        # Initialize session state for category filter
        if 'selected_categories' not in st.session_state:
            st.session_state.selected_categories = available_categories
        
        selected_categories = st.sidebar.multiselect(
            "Select Categories:",
            available_categories,
            default=st.session_state.selected_categories,
            key='category_multiselect'
        )
        st.session_state.selected_categories = selected_categories
    else:
        selected_categories = []
    
    # Reset filters button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset All Filters"):
        # Reset to default values
        st.session_state.selected_year = "All Years"  # Reset to "All Years" option
        if 'geographic' in data:
            available_regions = sorted(data['geographic']['Region'].unique())
            st.session_state.selected_regions = available_regions
        if 'category' in data:
            available_categories = sorted(data['category']['Category'].unique())
            st.session_state.selected_categories = available_categories
        st.rerun()
    
    # =============================================================================
    # APPLY FILTERS TO DATA
    # =============================================================================
    # Apply the selected filters to the data
    filtered_data = filter_data(data, selected_year, selected_regions, selected_categories)
    

    
    # =============================================================================
    # KEY METRICS SECTION
    # =============================================================================
    st.header("📊 Key Business Metrics")
    
    if 'kpis' in filtered_data:
        kpis = filtered_data['kpis']
        
        # Create 4 columns for key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Total Sales",
                value=format_currency(kpis['total_sales']),
                delta=format_percentage(kpis.get('total_growth_rate', 0))
            )
        
        with col2:
            st.metric(
                label="📦 Total Orders",
                value=f"{kpis['total_orders']:,}",
                delta=f"{kpis['avg_order_value']:.0f} avg"
            )
        
        with col3:
            st.metric(
                label="👥 Total Customers",
                value=f"{kpis['total_customers']:,}",
                delta=f"{kpis['avg_orders_per_customer']:.1f} orders/customer"
            )
        
        with col4:
            st.metric(
                label="🏆 Top Region",
                value=kpis['top_region'],
                delta=format_currency(kpis['top_region_sales'])
            )
    
    st.markdown("---")
    
    # =============================================================================
    # MAIN VISUALIZATIONS SECTION
    # =============================================================================
    st.header("📈 Business Insights")
    
    # Sales trend over time
    if 'yearly' in filtered_data and filtered_data['yearly'].shape[0] > 0:
        st.subheader("📈 Sales Trend Analysis")
        st.markdown("*What's our sales trend over the past 4 years?*")
        trend_fig = create_sales_trend(filtered_data['yearly'])
        st.plotly_chart(trend_fig, use_container_width=True)
    else:
        st.subheader("📈 Sales Trend Analysis")
        st.info("No data available for selected filters")
    
    # Product category performance
    if 'category' in filtered_data and filtered_data['category'].shape[0] > 0:
        st.subheader("📦 Product Category Analysis")
        st.markdown("*What are our best-selling product categories?*")
        category_fig = create_category_chart(filtered_data['category'])
        st.plotly_chart(category_fig, use_container_width=True)
    else:
        st.subheader("📦 Product Category Analysis")
        st.info("No data available for selected filters")
    
    # Customer segment analysis
    if 'segment' in filtered_data and filtered_data['segment'].shape[0] > 0:
        st.subheader("👥 Customer Segment Analysis")
        st.markdown("*Which customer segments are most valuable?*")
        segment_fig = create_segment_chart(filtered_data['segment'])
        st.plotly_chart(segment_fig, use_container_width=True)
    else:
        st.subheader("👥 Customer Segment Analysis")
        st.info("No data available for selected filters")
    
    # =============================================================================
    # GEOGRAPHIC PERFORMANCE SECTION
    # =============================================================================
    st.header("🌍 Geographic Performance")
    
    # Geographic performance
    if 'geographic' in filtered_data and filtered_data['geographic'].shape[0] > 0:
        st.markdown("*Which states have the highest sales?*")
        map_fig = create_sales_map(filtered_data['geographic'], selected_year)
        if map_fig is not None:
            st.plotly_chart(map_fig, use_container_width=True)
        else:
            st.info("Unable to create map visualization")
    else:
        st.info("No data available for selected filters")
    
    # =============================================================================
    # DETAILED ANALYSIS SECTION
    # =============================================================================
    st.header("🔍 Detailed Analysis")
    
    # Top performers
    st.subheader("🏆 Top Performers")
    
    # Top states by sales
    if 'geographic' in filtered_data and filtered_data['geographic'].shape[0] > 0:
        top_states = filtered_data['geographic'].nlargest(5, 'Total_Sales')[['State', 'Total_Sales']]
        st.markdown("**Top 5 States by Sales:**")
        st.dataframe(
            top_states,
            column_order=("State", "Total_Sales"),
            hide_index=True,
            width=None,
            column_config={
                "State": st.column_config.TextColumn(
                    "State",
                ),
                "Total_Sales": st.column_config.ProgressColumn(
                    "Total Sales ($)",
                    format="$%f",
                    min_value=0,
                    max_value=max(top_states['Total_Sales']),
                )
            }
        )
    else:
        st.markdown("**Top 5 States by Sales:**")
        st.info("No data available for selected filters")
    
    # Top categories
    if 'category' in filtered_data and filtered_data['category'].shape[0] > 0:
        top_categories = filtered_data['category'].nlargest(3, 'Total_Sales')[['Category', 'Total_Sales']]
        st.markdown("**Top Categories:**")
        st.dataframe(
            top_categories,
            column_order=("Category", "Total_Sales"),
            hide_index=True,
            width=None,
            column_config={
                "Category": st.column_config.TextColumn(
                    "Category",
                ),
                "Total_Sales": st.column_config.ProgressColumn(
                    "Total Sales ($)",
                    format="$%f",
                    min_value=0,
                    max_value=max(top_categories['Total_Sales']),
                )
            }
        )
    else:
        st.markdown("**Top Categories:**")
        st.info("No data available for selected filters")
    
    # Regional comparison
    st.subheader("📊 Regional Comparison")
    
    # Region comparison chart
    if 'geographic' in filtered_data and filtered_data['geographic'].shape[0] > 0:
        region_fig = create_region_comparison(filtered_data['geographic'])
        st.plotly_chart(region_fig, use_container_width=True)
    else:
        st.info("No data available for selected filters")
    
    # Sales heatmap
    st.subheader("🔥 Sales Performance Heatmap")
    
    # Heatmap showing category vs region performance
    if 'raw_data' in data:
        heatmap_fig = create_sales_heatmap(data['raw_data'], selected_year)
        st.plotly_chart(heatmap_fig, use_container_width=True)
        st.markdown("*Which category-region combinations perform best?*")
    else:
        st.info("No data available for heatmap visualization")
    
    
    
    # =============================================================================
    # EDUCATIONAL SECTION
    # =============================================================================
    st.header("🎓 Learning Insights")
    
    with st.expander("💡 Key Business Questions This Dashboard Answers", expanded=False):
        st.markdown("""
        **Geographic Performance:**
        - Which states/regions have the highest sales?
        - Where should we expand our business?
        
        **Product Strategy:**
        - What are our best-selling product categories?
        - Which products generate the most revenue?
        
        **Customer Insights:**
        - Which customer segments are most valuable?
        - How do different customers prefer different products?
        
        **Business Growth:**
        - What's our sales trend over the past 4 years?
        - Which markets show the strongest growth?
        
        **Operations & Efficiency:**
        - How do different shipping methods affect sales?
        - What's our average order value by region?
        """)
    
    with st.expander("📚 How to Use This Dashboard", expanded=False):
        st.markdown("""
        1. **Start with the Key Metrics** - Get an overview of business performance
        2. **Explore the Charts** - Click and hover to see detailed information
        3. **Use the Filters** - Focus on specific years, regions, or categories
        4. **Ask Questions** - Use the data to answer business questions
        5. **Draw Conclusions** - Identify patterns and make recommendations
        """)
    


# =============================================================================
# RUN THE DASHBOARD
# =============================================================================
if __name__ == "__main__":
    main()

