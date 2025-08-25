"""
Superstore Dataset Analysis Script

This module provides comprehensive analysis of the Superstore retail dataset,
including data structure exploration, quality assessment, and business insights.

The script analyzes a global superstore dataset containing 9,800 transactions
across 4 years (2015-2018) with 18 different attributes including sales,
geographic information, product categories, and customer segments.

Author: Georgios Ioannou
Date: 2025
"""

# Import libraries
import pandas as pd
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any



def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the Superstore dataset from CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing the dataset
        
    Returns:
        pd.DataFrame: Loaded dataset
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        pd.errors.EmptyDataError: If the file is empty
    """
    try:
        print(f"Loading dataset from: {file_path}")
        df = pd.read_csv(file_path)
        print(f"✅ Dataset loaded successfully!")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found!")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"❌ Error: File '{file_path}' is empty!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading dataset: {str(e)}")
        sys.exit(1)


def analyze_dataset_structure(df: pd.DataFrame) -> None:
    """
    Analyze and display the basic structure of the dataset.
    
    Args:
        df (pd.DataFrame): The dataset to analyze
    """
    print("\n" + "="*50)
    print("📊 SUPERSTORE DATASET STRUCTURE ANALYSIS")
    print("="*50)
    
    # Basic dataset information
    print(f"📈 Dataset Shape: {df.shape}")
    print(f"   • Number of rows (transactions): {df.shape[0]:,}")
    print(f"   • Number of columns (attributes): {df.shape[1]}")
    
    # Memory usage
    memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024  # Convert to MB
    print(f"💾 Memory Usage: {memory_usage:.2f} MB")


def display_column_information(df: pd.DataFrame) -> None:
    """
    Display detailed information about dataset columns.
    
    Args:
        df (pd.DataFrame): The dataset to analyze
    """
    print("\n" + "="*50)
    print("📋 COLUMN INFORMATION")
    print("="*50)
    
    print("Column List:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    print("\nData Types:")
    for col, dtype in df.dtypes.items():
        print(f"   • {col}: {dtype}")


def analyze_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze data quality including missing values and data integrity.
    
    Args:
        df (pd.DataFrame): The dataset to analyze
        
    Returns:
        Dict[str, Any]: Dictionary containing quality metrics
    """
    print("\n" + "="*50)
    print("🔍 DATA QUALITY ANALYSIS")
    print("="*50)
    
    # Missing values analysis
    missing_values = df.isnull().sum()
    total_records = len(df)
    
    print("Missing Values:")
    if missing_values.sum() == 0:
        print("   ✅ No missing values found!")
        quality_score = 100
    else:
        quality_score = ((total_records - missing_values.sum()) / total_records) * 100
        for col, missing_count in missing_values.items():
            if missing_count > 0:
                missing_percentage = (missing_count / total_records) * 100
                print(f"   ⚠️  {col}: {missing_count:,} ({missing_percentage:.2f}%)")
    
    print(f"\n📊 Data Quality Score: {quality_score:.1f}%")
    
    # Duplicate analysis
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"⚠️  Duplicate records: {duplicates:,}")
    else:
        print("✅ No duplicate records found")
    
    return {
        'quality_score': quality_score,
        'missing_values': missing_values.to_dict(),
        'duplicates': duplicates
    }


def explore_categorical_data(df: pd.DataFrame) -> None:
    """
    Explore categorical variables and their unique values.
    
    Args:
        df (pd.DataFrame): The dataset to analyze
    """
    print("\n" + "="*50)
    print("🏷️  CATEGORICAL DATA EXPLORATION")
    print("="*50)
    
    # Define key categorical columns for business analysis
    key_categorical_cols = ['Region', 'Category', 'Segment', 'Ship Mode', 'Country']
    
    for col in key_categorical_cols:
        if col in df.columns:
            unique_values = df[col].unique()
            value_counts = df[col].value_counts()
            
            print(f"\n📊 {col}:")
            print(f"   Unique values: {len(unique_values)}")
            print(f"   Values: {list(unique_values)}")
            
            print(f"   Distribution:")
            for value, count in value_counts.items():
                percentage = (count / len(df)) * 100
                print(f"     • {value}: {count:,} ({percentage:.1f}%)")


def analyze_temporal_data(df: pd.DataFrame) -> None:
    """
    Analyze temporal aspects of the dataset including date ranges.
    
    Args:
        df (pd.DataFrame): The dataset to analyze
    """
    print("\n" + "="*50)
    print("📅 TEMPORAL DATA ANALYSIS")
    print("="*50)
    
    # Find date columns
    date_cols = [col for col in df.columns if 'date' in col.lower() or 'Date' in col]
    
    if not date_cols:
        print("⚠️  No date columns found in the dataset")
        return
    
    for col in date_cols:
        if col in df.columns:
            print(f"\n📅 {col}:")
            
            # Convert to datetime for analysis
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                min_date = df[col].min()
                max_date = df[col].max()
                date_range = max_date - min_date
                
                print(f"   Date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
                print(f"   Total span: {date_range.days} days")
                print(f"   Years covered: {date_range.days / 365.25:.1f} years")
                
                # Yearly distribution
                yearly_counts = df[col].dt.year.value_counts().sort_index()
                print(f"   Yearly distribution:")
                for year, count in yearly_counts.items():
                    print(f"     • {year}: {count:,} records")
                    
            except Exception as e:
                print(f"   ⚠️  Error processing dates: {str(e)}")


def analyze_numerical_data(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Analyze numerical variables with descriptive statistics.
    
    Args:
        df (pd.DataFrame): The dataset to analyze
        
    Returns:
        Dict[str, Dict[str, float]]: Dictionary containing numerical summaries
    """
    print("\n" + "="*50)
    print("📊 NUMERICAL DATA ANALYSIS")
    print("="*50)
    
    # Select numerical columns
    numerical_cols = df.select_dtypes(include=['number']).columns
    numerical_summary = {}
    
    if len(numerical_cols) == 0:
        print("⚠️  No numerical columns found")
        return numerical_summary
    
    for col in numerical_cols:
        print(f"\n📈 {col}:")
        
        # Basic statistics
        min_val = df[col].min()
        max_val = df[col].max()
        mean_val = df[col].mean()
        median_val = df[col].median()
        std_val = df[col].std()
        
        print(f"   • Minimum: {min_val:,.2f}")
        print(f"   • Maximum: {max_val:,.2f}")
        print(f"   • Mean: {mean_val:,.2f}")
        print(f"   • Median: {median_val:,.2f}")
        print(f"   • Standard Deviation: {std_val:,.2f}")
        
        # Store summary for potential further analysis
        numerical_summary[col] = {
            'min': min_val,
            'max': max_val,
            'mean': mean_val,
            'median': median_val,
            'std': std_val
        }
    
    return numerical_summary


def generate_business_insights(df: pd.DataFrame) -> None:
    """
    Generate initial business insights from the dataset.
    
    Args:
        df (pd.DataFrame): The dataset to analyze
    """
    print("\n" + "="*50)
    print("💡 INITIAL BUSINESS INSIGHTS")
    print("="*50)
    
    # Sales analysis
    if 'Sales' in df.columns:
        total_sales = df['Sales'].sum()
        avg_order_value = df['Sales'].mean()
        print(f"💰 Total Sales: ${total_sales:,.2f}")
        print(f"💰 Average Order Value: ${avg_order_value:.2f}")
    
    # Geographic insights
    if 'Region' in df.columns:
        region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        print(f"\n🌍 Sales by Region:")
        for region, sales in region_sales.items():
            print(f"   • {region}: ${sales:,.2f}")
    
    # Product category insights
    if 'Category' in df.columns:
        category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
        print(f"\n📦 Sales by Category:")
        for category, sales in category_sales.items():
            print(f"   • {category}: ${sales:,.2f}")
    
    # Customer segment insights
    if 'Segment' in df.columns:
        segment_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
        print(f"\n👥 Sales by Customer Segment:")
        for segment, sales in segment_sales.items():
            print(f"   • {segment}: ${sales:,.2f}")


def display_sample_data(df: pd.DataFrame, n_samples: int = 3) -> None:
    """
    Display sample data from the dataset.
    
    Args:
        df (pd.DataFrame): The dataset to display
        n_samples (int): Number of sample rows to display
    """
    print("\n" + "="*50)
    print(f"📋 SAMPLE DATA (First {n_samples} rows)")
    print("="*50)
    
    # Display sample data with better formatting
    sample_df = df.head(n_samples)
    
    # Select key columns for display if dataset is large
    key_cols = ['Order ID', 'Order Date', 'Region', 'State', 'Category', 'Segment', 'Sales']
    display_cols = [col for col in key_cols if col in df.columns]
    
    if len(display_cols) < len(df.columns):
        print(f"Showing key columns: {', '.join(display_cols)}")
        sample_df = sample_df[display_cols]
    
    print(sample_df.to_string(index=False))


def main() -> None:
    """
    Main function to orchestrate the complete dataset analysis.
    
    This function loads the dataset and performs comprehensive analysis
    including structure exploration, quality assessment, and business insights.
    """
    print("🚀 Starting Superstore Dataset Analysis...")
    print("="*60)
    
    # Load dataset
    df = load_dataset('superstore_data.csv')
    
    # Perform comprehensive analysis
    analyze_dataset_structure(df)
    display_column_information(df)
    quality_metrics = analyze_data_quality(df)
    explore_categorical_data(df)
    analyze_temporal_data(df)
    numerical_summary = analyze_numerical_data(df)
    generate_business_insights(df)
    display_sample_data(df)
    
    # Summary
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE!")
    print("="*60)
    print(f"📊 Dataset successfully analyzed with {quality_metrics['quality_score']:.1f}% quality score")
    print("🎯 Ready for dashboard development and business intelligence applications")
    print("="*60)


if __name__ == "__main__":
    # Execute the main analysis
    main()
