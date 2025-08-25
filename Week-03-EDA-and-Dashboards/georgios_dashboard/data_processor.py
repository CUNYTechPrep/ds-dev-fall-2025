"""
Superstore Data Processing Module

This module processes the raw Superstore dataset and prepares it for dashboard visualization.
It includes data cleaning, aggregation, and business metrics calculation.

Author: Georgios Ioannou
Date: 2025
"""

# Import libraries
import numpy as np
import pandas as pd
import sys
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime


def load_and_clean_data(file_path: str = 'superstore_data.csv') -> pd.DataFrame:
    """
    Load and clean the Superstore dataset.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Cleaned dataset ready for analysis
    """
    print("🔄 Loading and cleaning Superstore data...")
    
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Convert date columns to datetime
    date_columns = ['Order Date', 'Ship Date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Extract year and month for analysis
    if 'Order Date' in df.columns:
        df['Order Year'] = df['Order Date'].dt.year
        df['Order Month'] = df['Order Date'].dt.month
        df['Order Quarter'] = df['Order Date'].dt.quarter
    
    # Handle missing values
    df['Postal Code'] = df['Postal Code'].fillna(0)
    
    print(f"✅ Data loaded: {len(df):,} records, {len(df.columns)} columns")
    return df


def create_geographic_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create geographic aggregation for dashboard visualization.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        
    Returns:
        pd.DataFrame: Geographic aggregation
    """
    print("🌍 Creating geographic aggregation...")
    
    # Aggregate by state
    state_agg = df.groupby(['State', 'Region']).agg({
        'Sales': ['sum', 'mean', 'count'],
        'Order ID': 'nunique'  # Unique orders
    }).round(2)
    
    # Flatten column names
    state_agg.columns = ['Total_Sales', 'Avg_Sales', 'Transaction_Count', 'Order_Count']
    state_agg = state_agg.reset_index()
    
    # Calculate additional metrics
    state_agg['Sales_Per_Order'] = (state_agg['Total_Sales'] / state_agg['Order_Count']).round(2)
    
    print(f"✅ Geographic aggregation created: {len(state_agg)} states")
    return state_agg


def create_temporal_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create temporal aggregation for time series analysis.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        
    Returns:
        pd.DataFrame: Temporal aggregation
    """
    print("📅 Creating temporal aggregation...")
    
    # Aggregate by year
    yearly_agg = df.groupby('Order Year').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Order ID': 'nunique'
    }).round(2)
    
    yearly_agg.columns = ['Total_Sales', 'Avg_Sales', 'Transaction_Count', 'Order_Count']
    yearly_agg = yearly_agg.reset_index()
    
    # Calculate year-over-year growth
    yearly_agg['Sales_Growth'] = yearly_agg['Total_Sales'].pct_change() * 100
    
    # Aggregate by year and month
    monthly_agg = df.groupby(['Order Year', 'Order Month']).agg({
        'Sales': 'sum',
        'Order ID': 'nunique'
    }).round(2)
    
    monthly_agg.columns = ['Total_Sales', 'Order_Count']
    monthly_agg = monthly_agg.reset_index()
    
    print(f"✅ Temporal aggregation created: {len(yearly_agg)} years, {len(monthly_agg)} month-year combinations")
    return yearly_agg, monthly_agg


def create_category_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create product category aggregation.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        
    Returns:
        pd.DataFrame: Category aggregation
    """
    print("📦 Creating category aggregation...")
    
    # Aggregate by category
    category_agg = df.groupby('Category').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Order ID': 'nunique'
    }).round(2)
    
    category_agg.columns = ['Total_Sales', 'Avg_Sales', 'Transaction_Count', 'Order_Count']
    category_agg = category_agg.reset_index()
    
    # Calculate market share
    total_sales = category_agg['Total_Sales'].sum()
    category_agg['Market_Share'] = (category_agg['Total_Sales'] / total_sales * 100).round(2)
    
    # Aggregate by sub-category
    subcategory_agg = df.groupby(['Category', 'Sub-Category']).agg({
        'Sales': ['sum', 'mean', 'count'],
        'Order ID': 'nunique'
    }).round(2)
    
    subcategory_agg.columns = ['Total_Sales', 'Avg_Sales', 'Transaction_Count', 'Order_Count']
    subcategory_agg = subcategory_agg.reset_index()
    
    print(f"✅ Category aggregation created: {len(category_agg)} categories, {len(subcategory_agg)} sub-categories")
    return category_agg, subcategory_agg


def create_segment_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create customer segment aggregation.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        
    Returns:
        pd.DataFrame: Segment aggregation
    """
    print("👥 Creating segment aggregation...")
    
    # Aggregate by segment
    segment_agg = df.groupby('Segment').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Order ID': 'nunique',
        'Customer ID': 'nunique'
    }).round(2)
    
    segment_agg.columns = ['Total_Sales', 'Avg_Sales', 'Transaction_Count', 'Order_Count', 'Customer_Count']
    segment_agg = segment_agg.reset_index()
    
    # Calculate additional metrics
    segment_agg['Sales_Per_Customer'] = (segment_agg['Total_Sales'] / segment_agg['Customer_Count']).round(2)
    segment_agg['Orders_Per_Customer'] = (segment_agg['Order_Count'] / segment_agg['Customer_Count']).round(2)
    
    print(f"✅ Segment aggregation created: {len(segment_agg)} segments")
    return segment_agg


def create_ship_mode_aggregation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create shipping mode aggregation.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        
    Returns:
        pd.DataFrame: Ship mode aggregation
    """
    print("🚚 Creating ship mode aggregation...")
    
    # Aggregate by ship mode
    ship_mode_agg = df.groupby('Ship Mode').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Order ID': 'nunique'
    }).round(2)
    
    ship_mode_agg.columns = ['Total_Sales', 'Avg_Sales', 'Transaction_Count', 'Order_Count']
    ship_mode_agg = ship_mode_agg.reset_index()
    
    # Calculate percentage of total
    total_orders = ship_mode_agg['Order_Count'].sum()
    ship_mode_agg['Order_Percentage'] = (ship_mode_agg['Order_Count'] / total_orders * 100).round(2)
    
    print(f"✅ Ship mode aggregation created: {len(ship_mode_agg)} ship modes")
    return ship_mode_agg


def calculate_business_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate key business performance indicators.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        
    Returns:
        Dict[str, Any]: Dictionary containing KPIs
    """
    print("📊 Calculating business KPIs...")
    
    kpis = {}
    
    # Overall metrics
    kpis['total_sales'] = df['Sales'].sum()
    kpis['total_orders'] = df['Order ID'].nunique()
    kpis['total_customers'] = df['Customer ID'].nunique()
    kpis['total_transactions'] = len(df)
    
    # Average metrics
    kpis['avg_order_value'] = kpis['total_sales'] / kpis['total_orders']
    kpis['avg_sales_per_customer'] = kpis['total_sales'] / kpis['total_customers']
    kpis['avg_orders_per_customer'] = kpis['total_orders'] / kpis['total_customers']
    
    # Growth metrics (if multiple years)
    if 'Order Year' in df.columns:
        years = sorted(df['Order Year'].unique())
        if len(years) > 1:
            first_year_sales = df[df['Order Year'] == years[0]]['Sales'].sum()
            last_year_sales = df[df['Order Year'] == years[-1]]['Sales'].sum()
            kpis['total_growth_rate'] = ((last_year_sales - first_year_sales) / first_year_sales * 100)
    
    # Regional metrics
    if 'Region' in df.columns:
        region_sales = df.groupby('Region')['Sales'].sum()
        kpis['top_region'] = region_sales.idxmax()
        kpis['top_region_sales'] = region_sales.max()
    
    # Category metrics
    if 'Category' in df.columns:
        category_sales = df.groupby('Category')['Sales'].sum()
        kpis['top_category'] = category_sales.idxmax()
        kpis['top_category_sales'] = category_sales.max()
    
    # Segment metrics
    if 'Segment' in df.columns:
        segment_sales = df.groupby('Segment')['Sales'].sum()
        kpis['top_segment'] = segment_sales.idxmax()
        kpis['top_segment_sales'] = segment_sales.max()
    
    print("✅ Business KPIs calculated")
    return kpis


def create_dashboard_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create all aggregated datasets for dashboard visualization.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        
    Returns:
        Dict[str, Any]: Dictionary containing all aggregated datasets
    """
    print("🎯 Creating dashboard datasets...")
    
    dashboard_data = {}
    
    # Create all aggregations
    dashboard_data['geographic'] = create_geographic_aggregation(df)
    yearly_agg, monthly_agg = create_temporal_aggregation(df)
    dashboard_data['yearly'] = yearly_agg
    dashboard_data['monthly'] = monthly_agg
    category_agg, subcategory_agg = create_category_aggregation(df)
    dashboard_data['category'] = category_agg
    dashboard_data['subcategory'] = subcategory_agg
    dashboard_data['segment'] = create_segment_aggregation(df)
    dashboard_data['ship_mode'] = create_ship_mode_aggregation(df)
    
    # Calculate KPIs
    dashboard_data['kpis'] = calculate_business_kpis(df)
    
    # Store original data for detailed analysis
    dashboard_data['raw_data'] = df
    
    print("✅ All dashboard datasets created successfully!")
    return dashboard_data


def save_processed_data(dashboard_data: Dict[str, Any], output_dir: str = 'processed_data') -> None:
    """
    Save processed datasets to CSV files for dashboard use.
    
    Args:
        dashboard_data (Dict[str, Any]): Processed dashboard data
        output_dir (str): Output directory for saved files
    """
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"💾 Saving processed data to {output_dir}/...")
    
    # Save each dataset
    for name, data in dashboard_data.items():
        if isinstance(data, pd.DataFrame):
            file_path = f"{output_dir}/{name}_data.csv"
            data.to_csv(file_path, index=False)
            print(f"   ✅ Saved {name}_data.csv")
    
    # Save KPIs as JSON
    import json
    kpis_file = f"{output_dir}/business_kpis.json"
    with open(kpis_file, 'w') as f:
        json.dump(dashboard_data['kpis'], f, indent=2, default=str)
    print(f"   ✅ Saved business_kpis.json")
    
    print(f"✅ All data saved to {output_dir}/")


def main() -> None:
    """
    Main function to process Superstore data for dashboard.
    """
    print("🚀 Starting Superstore Data Processing...")
    print("="*60)
    
    # Load and clean data
    df = load_and_clean_data()
    
    # Create dashboard datasets
    dashboard_data = create_dashboard_data(df)
    
    # Save processed data
    save_processed_data(dashboard_data)
    
    # Summary
    print("\n" + "="*60)
    print("✅ DATA PROCESSING COMPLETE!")
    print("="*60)
    print("📊 Datasets created:")
    print("   • Geographic data (states, regions)")
    print("   • Temporal data (yearly, monthly)")
    print("   • Category data (categories, sub-categories)")
    print("   • Segment data (customer segments)")
    print("   • Ship mode data (delivery methods)")
    print("   • Business KPIs")
    print("\n🎯 Ready for dashboard development!")
    print("="*60)


if __name__ == "__main__":
    main()
