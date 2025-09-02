# Import libraries.
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import warnings

from datetime import datetime, timedelta
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Optional, Any, Union


# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")


def validate_and_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean the dataset to prevent data type errors.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset that needs validation and cleaning.

    Returns
    -------
    pd.DataFrame
        Cleaned dataset with validated data types and standardized formats.

    Purpose
    -------
    This function ensures data quality by validating data types, handling missing values,
    and standardizing categorical columns to prevent errors in downstream analysis.
    """
    try:
        # Create a copy to avoid modifying the original
        clean_df = df.copy()

        # Ensure all categorical columns are strings
        categorical_cols = [
            "ARREST_BORO",
            "PERP_SEX",
            "LAW_CAT_CD",
            "OFNS_DESC",
            "PERP_RACE",
            "AGE_GROUP",
        ]
        for col in categorical_cols:
            if col in clean_df.columns:
                clean_df[col] = clean_df[col].fillna("Unknown").astype(str)

        # Handle coordinate columns
        if "latitude" in clean_df.columns:
            clean_df["latitude"] = pd.to_numeric(clean_df["latitude"], errors="coerce")
        if "longitude" in clean_df.columns:
            clean_df["longitude"] = pd.to_numeric(
                clean_df["longitude"], errors="coerce"
            )

        return clean_df

    except Exception as e:
        st.warning(f"Data validation warning: {str(e)}")
        return df


# Page configuration
st.set_page_config(
    page_title="NYPD Arrests Dashboard",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1F77B4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1F77B4;
    }
    .info-box {
        background-color: #E8F4FD;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17A2B8;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_full_nypd_data(file_path: str) -> pd.DataFrame:
    """Load the full NYPD arrests dataset from CSV file with caching.

    Parameters
    ----------
    file_path : str
        Path to the CSV file containing the NYPD arrests dataset.

    Returns
    -------
    pd.DataFrame
        Full dataset with optimized data types, processed columns, and temporal features.

    Purpose
    -------
    This function loads the entire NYPD arrests dataset once and caches it for performance.
    It processes column names, converts dates, creates temporal features, and standardizes
    categorical data. The cached result prevents reloading the same data multiple times.
    """
    try:
        # Load the full dataset
        df = pd.read_csv(file_path)
        st.info(f"Loaded full dataset: {len(df):,} rows")

        # Map actual column names to expected names for consistency
        column_mapping = {
            "arrest_date": "ARREST_DATE",
            "arrest_boro": "ARREST_BORO",
            "age_group": "AGE_GROUP",
            "perp_sex": "PERP_SEX",
            "perp_race": "PERP_RACE",
            "ofns_desc": "OFNS_DESC",
            "law_cat_cd": "LAW_CAT_CD",
            "jurisdiction_code": "JURISDICTION_CODE",
            "latitude": "latitude",
            "longitude": "longitude",
        }

        # Rename columns to match expected names
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df[new_name] = df[old_name]

        # Process arrest date
        if "ARREST_DATE" in df.columns:
            try:
                # Convert date column to datetime with error handling
                df["ARREST_DATE"] = pd.to_datetime(df["ARREST_DATE"], errors="coerce")

                # Only create temporal features for valid dates
                valid_dates = df["ARREST_DATE"].dropna()
                if len(valid_dates) > 0:
                    # Extract additional temporal features only for valid dates
                    df["YEAR"] = df["ARREST_DATE"].dt.year.fillna(2024)
                    df["MONTH"] = df["ARREST_DATE"].dt.month.fillna(1)
                    df["DAY_OF_WEEK"] = (
                        df["ARREST_DATE"].dt.day_name().fillna("Unknown")
                    )
                    df["QUARTER"] = df["ARREST_DATE"].dt.quarter.fillna(1)
                else:
                    # Create dummy temporal features if no valid dates
                    df["YEAR"] = 2024
                    df["MONTH"] = 1
                    df["DAY_OF_WEEK"] = "Unknown"
                    df["QUARTER"] = 1
            except Exception as e:
                st.warning(f"Date processing warning: {str(e)}")
                # Create dummy temporal features if date parsing fails
                df["YEAR"] = 2024
                df["MONTH"] = 1
                df["DAY_OF_WEEK"] = "Unknown"
                df["QUARTER"] = 1
        else:
            # Create dummy temporal features if no date column
            df["YEAR"] = 2024
            df["MONTH"] = 1
            df["DAY_OF_WEEK"] = "Unknown"
            df["QUARTER"] = 1

        # Clean and standardize categorical columns
        try:
            if "ARREST_BORO" in df.columns:
                df["ARREST_BORO"] = (
                    df["ARREST_BORO"].fillna("Unknown").astype(str).str.upper()
                )
            if "PERP_SEX" in df.columns:
                df["PERP_SEX"] = (
                    df["PERP_SEX"].fillna("Unknown").astype(str).str.upper()
                )
            if "LAW_CAT_CD" in df.columns:
                df["LAW_CAT_CD"] = (
                    df["LAW_CAT_CD"].fillna("Unknown").astype(str).str.upper()
                )
            if "OFNS_DESC" in df.columns:
                df["OFNS_DESC"] = df["OFNS_DESC"].fillna("Unknown").astype(str)

        except Exception as e:
            st.warning(f"Some categorical columns could not be standardized: {e}")

        # Create age group mapping for better analysis
        try:
            if "AGE_GROUP" in df.columns:
                age_mapping = {
                    "18-24": "18-24",
                    "25-44": "25-44",
                    "45-64": "45-64",
                    "65+": "65+",
                    "<18": "<18",
                }
                df["AGE_GROUP_CLEAN"] = (
                    df["AGE_GROUP"].astype(str).map(age_mapping).fillna("Unknown")
                )
            else:
                df["AGE_GROUP_CLEAN"] = "Unknown"
        except Exception as e:
            st.warning(f"Age group mapping failed: {e}")
            df["AGE_GROUP_CLEAN"] = "Unknown"

        # Validate and clean the data before returning
        clean_df = validate_and_clean_data(df)
        return clean_df

    except FileNotFoundError:
        st.error(f"Error: File '{file_path}' not found!")
        st.stop()
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        st.stop()


def filter_and_sample_data(
    df: pd.DataFrame,
    sample_size: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> pd.DataFrame:
    """Filter and sample data from a pre-loaded dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Pre-loaded full dataset to be filtered and sampled.
    sample_size : int
        Number of rows to sample from the filtered data.
    start_date : Optional[datetime]
        Start date for filtering (inclusive). If None, no start date filtering is applied.
    end_date : Optional[datetime]
        End date for filtering (inclusive). If None, no end date filtering is applied.

    Returns
    -------
    pd.DataFrame
        Filtered and sampled dataset based on the specified parameters.

    Purpose
    -------
    This function applies date filtering and sampling to a pre-loaded dataset without
    reloading the source data. It first filters by date range if specified, then
    samples the filtered data to the requested size for performance optimization.
    """
    try:
        # Create a copy to avoid modifying the original
        filtered_df = df.copy()

        # Apply date filtering if dates are provided
        if start_date is not None and end_date is not None:
            # Filter data to the specified date range
            filtered_df = filtered_df[
                (filtered_df["ARREST_DATE"] >= start_date)
                & (filtered_df["ARREST_DATE"] <= end_date)
            ]
            st.info(
                f"Filtered to date range: {start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')} - {len(filtered_df)} rows remaining"
            )

        # Apply sampling AFTER date filtering
        if sample_size > 0 and len(filtered_df) > sample_size:
            filtered_df = filtered_df.sample(
                n=sample_size, random_state=42
            )  # Use fixed random state for reproducibility
            st.info(f"Sampled {sample_size:,} rows from the date-filtered data")
        elif sample_size > 0:
            st.info(
                f"Date-filtered data contains {len(filtered_df):,} rows (less than requested sample size)"
            )

        return filtered_df

    except Exception as e:
        st.error(f"Error filtering and sampling data: {str(e)}")
        return df


def display_dataset_overview(df: pd.DataFrame) -> None:
    """Display comprehensive overview of the dataset including basic statistics.

    Parameters
    ----------
    df : pd.DataFrame
        The NYPD arrests dataset to be displayed and analyzed.

    Returns
    -------
    None
        This function displays information to the Streamlit interface.

    Purpose
    -------
    This function creates the main dashboard interface showing dataset metrics,
    borough information, date ranges, and creates tabs for different types of
    analysis (geographic, temporal, demographics, and dataset information).
    """
    st.markdown(
        '<h1 class="main-header">NYPD Arrests Dashboard</h1>', unsafe_allow_html=True
    )

    # Dataset overview metrics
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        <div style="font-size: 1.5rem; font-weight: bold; color: white;">Total Arrests</div>
        <div style="font-size: 2rem; font-weight: bold; color: #FF0000;">{len(df):,}</div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        # Check if ARREST_BORO exists
        if "ARREST_BORO" in df.columns:
            borough_count = df["ARREST_BORO"].nunique()
        else:
            borough_count = "N/A"

        st.markdown(
            f"""
        <div style="font-size: 1.5rem; font-weight: bold; color: white;">Boroughs</div>
        <div style="font-size: 2rem; font-weight: bold; color: #FF0000;">{borough_count}</div>
        """,
            unsafe_allow_html=True,
        )

    # Boroughs list above the date range
    if "ARREST_BORO" in df.columns:
        try:
            # Clean borough data and ensure it's string type
            boroughs_raw = df["ARREST_BORO"].dropna().astype(str)
            boroughs = sorted(boroughs_raw.unique())
            borough_names = {
                "B": "Bronx",
                "K": "Brooklyn",
                "M": "Manhattan",
                "Q": "Queens",
                "S": "Staten Island",
            }
            borough_list = [borough_names.get(b, b) for b in boroughs]
            boroughs_text = ", ".join(borough_list)
        except Exception as e:
            st.warning(f"Borough processing warning: {str(e)}")
            boroughs_text = "N/A"
    else:
        boroughs_text = "N/A"

    st.markdown(
        f"<div style='font-size: 1.5rem; margin-bottom: 1rem;'><strong>Boroughs: </strong><span style='color: #FF0000; font-weight: bold;'>{boroughs_text}</span></div>",
        unsafe_allow_html=True,
    )

    # Date range below the metrics
    if "ARREST_DATE" in df.columns:
        try:
            # Ensure ARREST_DATE is datetime type
            if df["ARREST_DATE"].dtype == "object":
                # Convert string dates to datetime, handling errors
                df["ARREST_DATE"] = pd.to_datetime(df["ARREST_DATE"], errors="coerce")

            # Check if we have valid dates after conversion
            valid_dates = df["ARREST_DATE"].dropna()
            if len(valid_dates) > 0:
                min_date = valid_dates.min()
                max_date = valid_dates.max()
                if pd.notna(min_date) and pd.notna(max_date):
                    date_range = f"{min_date.strftime('%m/%d/%Y')} to {max_date.strftime('%m/%d/%Y')}"
                    days_diff = (max_date - min_date).days
                    date_range_with_days = f"{date_range} <span style='color: white;'>({days_diff} days)</span>"

                else:
                    date_range_with_days = "N/A"
            else:
                date_range_with_days = "N/A"
        except Exception as e:
            st.warning(f"Date processing warning: {str(e)}")
            date_range_with_days = "N/A"
    else:
        date_range_with_days = "N/A"

    st.markdown(
        f"<div style='font-size: 1.5rem; margin-bottom: 2rem;'><strong>Date Range: </strong><span style='color: #FF0000; font-weight: bold;'>{date_range_with_days}</span></div>",
        unsafe_allow_html=True,
    )

    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "**Geographic Analysis**",
            "**Temporal Analysis**",
            "**Demographics**",
            "**Dataset Information**",
        ]
    )

    with tab1:
        create_geographic_analysis(df)

    with tab2:
        create_temporal_analysis(df)

    with tab3:
        create_demographic_analysis(df)

    with tab4:
        # Dataset information
        st.markdown(
            """
        This dashboard analyzes NYPD arrest data from 2006 onwards. The dataset contains detailed information about:
        - **Arrest Details**: Date, location, and jurisdiction
        - **Demographics**: Age, race, and gender of arrestees
        - **Crime Information**: Offense descriptions and legal categories
        - **Geographic Data**: Borough, precinct, and coordinates
        
        **Date Filtering**: Use the sidebar controls to filter the dataset by date range. This allows you to:
        - Focus on specific time periods for analysis
        - Compare arrest patterns across different years
        - Analyze seasonal trends within selected date ranges
        - Reduce data size for faster processing
        """
        )

        # Data preview
        st.markdown("### Data Preview")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**First 5 rows:**")
            st.dataframe(df.head(), use_container_width=True)

        with col2:
            st.markdown("**Data types:**")
            dtype_info = pd.DataFrame(
                {
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str),
                    "Non-Null Count": df.count(),
                }
            )
            st.dataframe(dtype_info, use_container_width=True)

        # Data quality metrics
        st.markdown("### Data Quality Metrics For The Current Sample Size")
        col1, col2, col3 = st.columns(3)

        with col1:
            missing_data = df.isnull().sum().sum()
            st.metric("Missing Values", f"{missing_data:,}")

        with col2:
            memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024
            st.metric("Memory Usage", f"{memory_usage:.1f} MB")

        with col3:
            duplicate_rows = df.duplicated().sum()
            st.metric("Duplicate Rows", f"{duplicate_rows:,}")


def create_temporal_analysis(df: pd.DataFrame) -> None:
    """Create temporal analysis visualizations showing arrest patterns over time.

    Parameters
    ----------
    df : pd.DataFrame
        The NYPD arrests dataset to analyze for temporal patterns.

    Returns
    -------
    None
        This function displays visualizations to the Streamlit interface.

    Purpose
    -------
    This function creates interactive temporal analysis including yearly trends,
    monthly patterns, and day-of-week analysis. It provides filters for borough
    and offense type selection, allowing users to analyze time patterns for
    specific subsets of the data.
    """
    # Add filters for borough and offense type
    st.markdown("### Filter Temporal Analysis")
    st.markdown("*Select specific boroughs and offense types to analyze time patterns*")

    # Filter controls
    col1, col2 = st.columns(2)

    with col1:
        try:
            # Create borough options with full names for display
            borough_codes = sorted(df["ARREST_BORO"].dropna().astype(str).unique())
            borough_names = {
                "B": "Bronx",
                "K": "Brooklyn",
                "M": "Manhattan",
                "Q": "Queens",
                "S": "Staten Island",
            }

            # Create display options with full names, including "All Boroughs" option
            borough_display_options = ["All Boroughs"] + [
                borough_names.get(code, code) for code in borough_codes
            ]

            selected_borough_display = st.selectbox(
                "Select Borough:",
                options=borough_display_options,
                index=0,
                key="temporal_borough_select",
                help="Choose which borough to analyze, or select 'All Boroughs' for city-wide view",
            )

            # Convert display name back to code for filtering
            if selected_borough_display == "All Boroughs":
                selected_boroughs_filter = borough_codes  # Include all boroughs
            else:
                selected_borough_code = [
                    code
                    for code, name in borough_names.items()
                    if name == selected_borough_display
                ][0]
                selected_boroughs_filter = [selected_borough_code]

        except Exception as e:
            st.error(f"Error loading borough options: {str(e)}")
            selected_boroughs_filter = []

    with col2:
        try:
            # Create offense options with "All Incidents" option
            offense_options = sorted(df["OFNS_DESC"].dropna().astype(str).unique())
            offense_display_options = ["All Incidents"] + offense_options

            selected_offense_display = st.selectbox(
                "Select Offense Type:",
                options=offense_display_options,
                index=0,
                key="temporal_offense_select",
                help="Choose which offense type to analyze, or select 'All Incidents' for all offense types",
            )

            # Convert selection to list for filtering
            if selected_offense_display == "All Incidents":
                selected_offenses_filter = offense_options  # Include all offense types
            else:
                selected_offenses_filter = [selected_offense_display]

        except Exception as e:
            st.error(f"Error loading offense options: {str(e)}")
            selected_offenses_filter = []

    # Apply filters to the data
    if selected_boroughs_filter and selected_offenses_filter:
        filtered_df = df[
            (df["ARREST_BORO"].isin(selected_boroughs_filter))
            & (df["OFNS_DESC"].isin(selected_offenses_filter))
        ]

        # Show filter summary
        st.success(
            f"Showing temporal patterns for {len(filtered_df):,} arrests from {len(selected_boroughs_filter)} borough(s) and {len(selected_offenses_filter)} offense type(s)"
        )

        # Use filtered data for all temporal visualizations
        df_to_analyze = filtered_df
    else:
        st.info("Select filters above to customize the temporal analysis")
        df_to_analyze = df

    # Yearly trends
    st.markdown("### Annual Arrest Trends")
    try:
        # Filter out invalid years and create yearly data
        valid_years = df_to_analyze[
            df_to_analyze["YEAR"].notna()
            & (df_to_analyze["YEAR"] >= 1900)
            & (df_to_analyze["YEAR"] <= 2030)
        ]
        if len(valid_years) > 0:
            yearly_arrests = (
                valid_years.groupby("YEAR").size().reset_index(name="Arrests")
            )

            fig_yearly = px.line(
                yearly_arrests,
                x="YEAR",
                y="Arrests",
                title="Arrests by Year (2006-Present)",
                labels={"YEAR": "Year", "Arrests": "Number of Arrests"},
                markers=True,
                color_discrete_sequence=["#FF6B6B"],
            )
            fig_yearly.update_layout(height=400)
            st.plotly_chart(fig_yearly, use_container_width=True)
        else:
            st.warning("No valid year data available for temporal analysis")
    except Exception as e:
        st.error(f"Error creating yearly trends: {str(e)}")
        st.info("This may be due to date parsing issues in the dataset")

    # Monthly patterns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Monthly Patterns")
        try:
            # Filter out invalid months
            valid_months = df_to_analyze[
                df_to_analyze["MONTH"].notna()
                & (df_to_analyze["MONTH"] >= 1)
                & (df_to_analyze["MONTH"] <= 12)
            ]
            if len(valid_months) > 0:
                monthly_arrests = (
                    valid_months.groupby("MONTH").size().reset_index(name="Arrests")
                )
                monthly_arrests["Month_Name"] = monthly_arrests["MONTH"].map(
                    {
                        1: "Jan",
                        2: "Feb",
                        3: "Mar",
                        4: "Apr",
                        5: "May",
                        6: "Jun",
                        7: "Jul",
                        8: "Aug",
                        9: "Sep",
                        10: "Oct",
                        11: "Nov",
                        12: "Dec",
                    }
                )

                # Define distinct colors for each month
                month_colors = {
                    "Jan": "#FF5733",
                    "Feb": "#33FF57",
                    "Mar": "#3357FF",
                    "Apr": "#F1C40F",
                    "May": "#8E44AD",
                    "Jun": "#13EDDD",
                    "Jul": "#ED13E9",
                    "Aug": "#F7F005",
                    "Sep": "#3498DB",
                    "Oct": "#E67E22",
                    "Nov": "#05F75E",
                    "Dec": "#34495E",
                }

                # Create the bar chart with different colors for each month
                fig_monthly = go.Figure()

                for _, row in monthly_arrests.iterrows():
                    month_name = row["Month_Name"]
                    arrests = row["Arrests"]
                    color = month_colors.get(
                        month_name, "#808080"
                    )  # Default gray if month not found

                    fig_monthly.add_trace(
                        go.Bar(
                            x=[month_name],
                            y=[arrests],
                            name=month_name,
                            marker_color=color,
                            showlegend=False,
                        )
                    )

                fig_monthly.update_layout(
                    title="Number of Arrests Per Month",
                    xaxis_title="Month",
                    yaxis_title="Number of Arrests",
                    height=400,
                    showlegend=False,
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
            else:
                st.warning("No valid month data available")
        except Exception as e:
            st.error(f"Error creating monthly patterns: {str(e)}")

    with col2:
        st.markdown("### Day of Week Patterns")
        try:
            # Filter out invalid day names
            valid_days = df_to_analyze[
                df_to_analyze["DAY_OF_WEEK"].notna()
                & (df_to_analyze["DAY_OF_WEEK"] != "Unknown")
            ]
            if len(valid_days) > 0:
                dow_arrests = (
                    valid_days.groupby("DAY_OF_WEEK").size().reset_index(name="Arrests")
                )
                dow_order = [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]
                dow_arrests["DAY_OF_WEEK"] = pd.Categorical(
                    dow_arrests["DAY_OF_WEEK"], categories=dow_order, ordered=True
                )
                dow_arrests = dow_arrests.sort_values("DAY_OF_WEEK")

                # Define distinct colors for each day of the week
                dow_colors = {
                    "Monday": "#3498DB",
                    "Tuesday": "#2ECC71",
                    "Wednesday": "#F1C40F",
                    "Thursday": "#E67E22",
                    "Friday": "#9B59B6",
                    "Saturday": "#E74C3C",
                    "Sunday": "#34495E",
                }

                # Create the bar chart with different colors for each day
                fig_dow = go.Figure()

                for _, row in dow_arrests.iterrows():
                    day_name = row["DAY_OF_WEEK"]
                    arrests = row["Arrests"]
                    color = dow_colors.get(
                        day_name, "#808080"
                    )  # Default gray if day not found

                    fig_dow.add_trace(
                        go.Bar(
                            x=[day_name],
                            y=[arrests],
                            name=day_name,
                            marker_color=color,
                            showlegend=False,
                        )
                    )

                fig_dow.update_layout(
                    title="Number of Arrests Per Day",
                    xaxis_title="Day of Week",
                    yaxis_title="Number of Arrests",
                    height=400,
                    showlegend=False,
                )
                st.plotly_chart(fig_dow, use_container_width=True)
            else:
                st.warning("No valid day of week data available")
        except Exception as e:
            st.error(f"Error creating day of week patterns: {str(e)}")


def create_geographic_analysis(df: pd.DataFrame) -> None:
    """Create geographic analysis visualizations showing arrest patterns by location.

    Parameters
    ----------
    df : pd.DataFrame
        The NYPD arrests dataset to analyze for geographic patterns.

    Returns
    -------
    None
        This function displays visualizations to the Streamlit interface.

    Purpose
    -------
    This function creates interactive geographic analysis including an interactive
    map showing arrest locations and a borough distribution pie chart. It provides
    filters for borough and offense type selection, and includes options to display
    all data or sampled data for performance optimization.
    """

    # Geographic coordinates visualization (if coordinates are available)
    if "latitude" in df.columns and "longitude" in df.columns:
        st.markdown("### Map View")
        st.markdown(
            "*Customize the map view by selecting specific boroughs and offense types*"
        )

        # Filter controls for the custom map
        col1, col2 = st.columns(2)

        with col1:
            try:
                # Create borough options with full names for display
                borough_codes = sorted(df["ARREST_BORO"].dropna().astype(str).unique())
                borough_names = {
                    "B": "Bronx",
                    "K": "Brooklyn",
                    "M": "Manhattan",
                    "Q": "Queens",
                    "S": "Staten Island",
                }

                # Create display options with full names, including "All Boroughs" option
                borough_display_options = ["All Boroughs"] + [
                    borough_names.get(code, code) for code in borough_codes
                ]

                selected_borough_display = st.selectbox(
                    "Select Borough:",
                    options=borough_display_options,
                    index=0,
                    key="geographic_borough_select",
                    help="Choose which borough to display on the filtered map, or select 'All Boroughs' for city-wide view",
                )

                # Convert display name back to code for filtering
                if selected_borough_display == "All Boroughs":
                    selected_boroughs_filter = borough_codes  # Include all boroughs
                else:
                    selected_borough_code = [
                        code
                        for code, name in borough_names.items()
                        if name == selected_borough_display
                    ][0]
                    selected_boroughs_filter = [selected_borough_code]

            except Exception as e:
                st.error(f"Error loading borough options: {str(e)}")
                selected_boroughs_filter = []

        with col2:
            try:
                # Create offense options with "All Incidents" option
                offense_options = sorted(df["OFNS_DESC"].dropna().astype(str).unique())
                offense_display_options = ["All Incidents"] + offense_options

                selected_offense_display = st.selectbox(
                    "Select Offense Type:",
                    options=offense_display_options,
                    index=0,
                    key="geographic_offense_select",
                    help="Choose which offense type to display on the filtered map, or select 'All Incidents' for all offense types",
                )

                # Convert selection to list for filtering
                if selected_offense_display == "All Incidents":
                    selected_offenses_filter = (
                        offense_options  # Include all offense types
                    )
                else:
                    selected_offenses_filter = [selected_offense_display]

            except Exception as e:
                st.error(f"Error loading offense options: {str(e)}")
                selected_offenses_filter = []

        # Add Filter Map button and data display options
        col1, col2, col3 = st.columns([10, 5, 0.1])
        with col1:
            show_all_data = st.checkbox(
                "Display all data (may be slower and crash the app)",
                value=False,
                help="Check this to display all incidents instead of sampling",
            )
        with col2:
            filter_button = st.button(
                "Filter Map",
                type="primary",
                use_container_width=True,
                key="filter_map_button",
            )

        st.markdown("---")

        # Filter the data based on selections only when button is clicked
        if filter_button and selected_boroughs_filter and selected_offenses_filter:
            with st.spinner("Filtering map data..."):
                filtered_df = df[
                    (df["ARREST_BORO"].isin(selected_boroughs_filter))
                    & (df["OFNS_DESC"].isin(selected_offenses_filter))
                ]

                # Handle data sampling based on user preference
                if show_all_data:
                    # Show all data with coordinates
                    filtered_sample_df = filtered_df.dropna(
                        subset=["latitude", "longitude"]
                    )
                    if len(filtered_sample_df) > 100000:
                        st.warning(
                            "`Map View: Showing all data may be slow with large datasets. Consider unchecking 'Show all data' for better performance."
                        )
                else:
                    # Sample data for performance - show more data when fewer filters are applied
                    max_points = (
                        50000
                        if (
                            len(selected_boroughs_filter) == len(borough_codes)
                            and len(selected_offenses_filter) == len(offense_options)
                        )
                        else 10000
                    )
                    filtered_sample_df = filtered_df.dropna(
                        subset=["latitude", "longitude"]
                    ).sample(n=min(max_points, len(filtered_df)))

                if len(filtered_sample_df) > 0:
                    # Create filtered map with full borough names
                    filtered_map_df = filtered_sample_df.copy()
                    filtered_map_df["Borough_Name"] = filtered_map_df[
                        "ARREST_BORO"
                    ].map(borough_names)

                    # Use the same borough colors for consistency
                    borough_colors = {
                        "Bronx": "#FF0000",
                        "Brooklyn": "#FF8C00",
                        "Manhattan": "#32CD32",
                        "Queens": "#0000FF",
                        "Staten Island": "#FF69B4",
                    }

                    # Show filter summary
                    st.success(
                        f"Map View: Showing {len(filtered_sample_df):,} arrests from {len(selected_boroughs_filter)} borough(s) and {len(selected_offenses_filter)} offense type(s)"
                    )

                    # Create the filtered map
                    filtered_fig_map = px.scatter_mapbox(
                        filtered_map_df,
                        lat="latitude",
                        lon="longitude",
                        color="Borough_Name",
                        color_discrete_map=borough_colors,
                        hover_data=["ARREST_DATE", "OFNS_DESC"],
                        title="Arrest Locations (Filtered View)",
                        mapbox_style="carto-positron",
                        zoom=10,
                    )
                    filtered_fig_map.update_layout(height=800)
                    st.plotly_chart(filtered_fig_map, use_container_width=True)
                else:
                    st.warning(
                        "No data available for the selected filters. Please adjust your selection."
                    )
        elif filter_button:
            if not selected_boroughs_filter:
                st.error("Please select a borough")
            if not selected_offenses_filter:
                st.error("Please select an offense type")
        else:
            pass

    # Always use the complete dataset for borough distribution
    pie_chart_data = df

    # Count actual boroughs and offense types in the data
    borough_count = pie_chart_data["ARREST_BORO"].nunique()
    offense_count = pie_chart_data["OFNS_DESC"].nunique()

    chart_title = (
        "Arrest Distribution by Borough - Per Capita Rates (per 100,000 residents)"
    )
    st.success(
        f"Pie Chart: Showing {len(pie_chart_data):,} arrests from {borough_count} borough(s) and {offense_count} offense type(s)"
    )

    # Create borough distribution from the selected dataset
    boro_arrests = pie_chart_data["ARREST_BORO"].value_counts().reset_index()
    boro_arrests.columns = ["Borough", "Arrests"]

    # Map borough codes to full names
    boro_names = {
        "B": "Bronx",
        "K": "Brooklyn",
        "M": "Manhattan",
        "Q": "Queens",
        "S": "Staten Island",
    }
    boro_arrests["Borough_Name"] = boro_arrests["Borough"].map(boro_names)

    # Clean borough names and ensure they match exactly
    boro_arrests["Borough_Name"] = boro_arrests["Borough_Name"].str.strip()

    # Borough population data (July 2023 estimates, except Staten Island from 2020 Census)
    borough_populations = {
        "Bronx": 1356476,
        "Brooklyn": 2561225,
        "Manhattan": 1597451,
        "Queens": 2252196,
        "Staten Island": 495747,
    }

    # Calculate per capita arrest rates (per 100,000 residents)
    boro_arrests["Population"] = boro_arrests["Borough_Name"].map(borough_populations)
    boro_arrests["Arrests_Per_100k"] = (
        boro_arrests["Arrests"] / boro_arrests["Population"]
    ) * 100000
    boro_arrests["Arrests_Per_100k"] = boro_arrests["Arrests_Per_100k"].round(1)

    # Define consistent borough colors for pie chart
    borough_colors = {
        "Bronx": "#FF0000",
        "Brooklyn": "#FF8C00",
        "Manhattan": "#32CD32",
        "Queens": "#0000FF",
        "Staten Island": "#FF69B4",
    }

    fig_boro = go.Figure(
        data=[
            go.Pie(
                labels=boro_arrests["Borough_Name"],
                values=boro_arrests["Arrests_Per_100k"],
                marker_colors=[
                    borough_colors.get(boro, "#808080")
                    for boro in boro_arrests["Borough_Name"]
                ],
                hovertemplate="<b>%{label}</b><br>"
                + "Arrests per 100k: %{value}<br>"
                + "Total Arrests: %{customdata[0]:,}<br>"
                + "Population: %{customdata[1]:,}<extra></extra>",
                customdata=np.stack(
                    [boro_arrests["Arrests"].values, boro_arrests["Population"].values],
                    axis=-1,
                ),
            )
        ]
    )

    fig_boro.update_layout(title=chart_title, height=400)
    st.plotly_chart(fig_boro, use_container_width=True)

    # Display the per capita data table
    st.markdown("### Per Capita Arrest Rates by Borough")
    display_df = boro_arrests[
        ["Borough_Name", "Arrests", "Population", "Arrests_Per_100k"]
    ].copy()
    display_df.columns = [
        "Borough",
        "Total Arrests",
        "Population",
        "Arrests per 100k Residents",
    ]
    st.dataframe(display_df, use_container_width=True)


def create_demographic_analysis(df: pd.DataFrame) -> None:
    """Create demographic analysis visualizations showing arrest patterns by demographics.

    Parameters
    ----------
    df : pd.DataFrame
        The NYPD arrests dataset to analyze for demographic patterns.

    Returns
    -------
    None
        This function displays visualizations to the Streamlit interface.

    Purpose
    -------
    This function creates interactive demographic analysis including age group
    distributions, gender analysis, and race analysis. It provides filters for
    borough and offense type selection, allowing users to analyze demographic
    patterns for specific subsets of the data.
    """
    # Add filters for borough and offense type
    st.markdown("### Filter Demographics")
    st.markdown(
        "*Select specific boroughs and offense types to analyze demographic patterns*"
    )

    # Filter controls
    col1, col2 = st.columns(2)

    with col1:
        try:
            # Create borough options with full names for display
            borough_codes = sorted(df["ARREST_BORO"].dropna().astype(str).unique())
            borough_names = {
                "B": "Bronx",
                "K": "Brooklyn",
                "M": "Manhattan",
                "Q": "Queens",
                "S": "Staten Island",
            }

            # Create display options with full names, including "All Boroughs" option
            borough_display_options = ["All Boroughs"] + [
                borough_names.get(code, code) for code in borough_codes
            ]

            selected_borough_display = st.selectbox(
                "Select Borough:",
                options=borough_display_options,
                index=0,
                key="demographic_borough_select",
                help="Choose which borough to analyze, or select 'All Boroughs' for city-wide view",
            )

            # Convert display name back to code for filtering
            if selected_borough_display == "All Boroughs":
                selected_boroughs_filter = borough_codes  # Include all boroughs
            else:
                selected_borough_code = [
                    code
                    for code, name in borough_names.items()
                    if name == selected_borough_display
                ][0]
                selected_boroughs_filter = [selected_borough_code]

        except Exception as e:
            st.error(f"Error loading borough options: {str(e)}")
            selected_boroughs_filter = []

    with col2:
        try:
            # Create offense options with "All Incidents" option
            offense_options = sorted(df["OFNS_DESC"].dropna().astype(str).unique())
            offense_display_options = ["All Incidents"] + offense_options

            selected_offense_display = st.selectbox(
                "Select Offense Type:",
                options=offense_display_options,
                index=0,
                key="demographic_offense_select",
                help="Choose which offense type to analyze, or select 'All Incidents' for all offense types",
            )

            # Convert selection to list for filtering
            if selected_offense_display == "All Incidents":
                selected_offenses_filter = offense_options  # Include all offense types
            else:
                selected_offenses_filter = [selected_offense_display]

        except Exception as e:
            st.error(f"Error loading offense options: {str(e)}")
            selected_offenses_filter = []

    # Apply filters to the data
    if selected_boroughs_filter and selected_offenses_filter:
        filtered_df = df[
            (df["ARREST_BORO"].isin(selected_boroughs_filter))
            & (df["OFNS_DESC"].isin(selected_offenses_filter))
        ]

        # Show filter summary
        st.success(
            f"Showing demographics for {len(filtered_df):,} arrests from {len(selected_boroughs_filter)} borough(s) and {len(selected_offenses_filter)} offense type(s)"
        )

        # Use filtered data for all demographic visualizations
        df_to_analyze = filtered_df
    else:
        st.info("Select filters above to customize the demographic analysis")
        df_to_analyze = df

    # Age group analysis
    col1, col2 = st.columns(2)

    with col1:
        age_arrests = df_to_analyze["AGE_GROUP_CLEAN"].value_counts().reset_index()
        age_arrests.columns = ["Age_Group", "Arrests"]

        # Define distinct colors for age groups
        age_colors = {
            "18-24": "#FF5733",
            "25-44": "#33FF57",
            "45-64": "#3357FF",
            "65+": "#F1C40F",
            "<18": "#8E44AD",
            "Unknown": "#1ABC9C",
        }

        # Create the bar chart with different colors for each age group
        fig_age = go.Figure()

        for _, row in age_arrests.iterrows():
            age_group = row["Age_Group"]
            arrests = row["Arrests"]
            color = age_colors.get(
                age_group, "#E74C3C"
            )  # Default to Red if age group not found

            fig_age.add_trace(
                go.Bar(
                    x=[age_group],
                    y=[arrests],
                    name=age_group,
                    marker_color=color,
                    showlegend=False,
                )
            )

        fig_age.update_layout(
            title="Arrests by Age Group",
            xaxis_title="Age Group",
            yaxis_title="Number of Arrests",
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col2:
        gender_arrests = df_to_analyze["PERP_SEX"].value_counts().reset_index()
        gender_arrests.columns = ["Gender", "Arrests"]

        # Define gender colors
        gender_colors = {"M": "#0000FF", "F": "#FF0000", "UNKNOWN": "#00FF00"}

        # Create the pie chart with explicit color control using go.Figure
        fig_gender = go.Figure(
            data=[
                go.Pie(
                    labels=gender_arrests["Gender"],
                    values=gender_arrests["Arrests"],
                    marker_colors=[
                        gender_colors.get(gender, "#00FF00")
                        for gender in gender_arrests["Gender"]
                    ],
                )
            ]
        )

        fig_gender.update_layout(title="Arrest Distribution by Gender", height=400)
        st.plotly_chart(fig_gender, use_container_width=True)

    # Race analysis
    race_arrests = df_to_analyze["PERP_RACE"].value_counts().reset_index()
    race_arrests.columns = ["Race", "Arrests"]

    # Show top 10 races
    top_races = race_arrests.head(10)

    # Define distinct colors for races
    race_colors = {
        "BLACK": "#FF5733",
        "WHITE": "#FFF0D0",
        "HISPANIC": "#9D33FF",
        "ASIAN": "#33FF57",
        "OTHER": "#FFC733",
        "UNKNOWN": "#FF33A8",
        "AMERICAN INDIAN": "#334BFF",
        "BLACK HISPANIC": "#FFC733",
        "WHITE HISPANIC": "#33C1FF",
        "ASIAN / PACIFIC ISLANDER": "#33FF57",
        "AMERICAN INDIAN/ALASKAN NATIVE": "#334BFF",
    }

    # Create the bar chart with different colors for each race
    # Use Plotly Express for more reliable color handling
    fig_race = px.bar(
        top_races,
        x="Race",
        y="Arrests",
        title="Top 10 Races by Number of Arrests",
        color="Race",
        color_discrete_map=race_colors,
    )

    fig_race.update_layout(
        xaxis_title="Race",
        yaxis_title="Number of Arrests",
        height=400,
        showlegend=False,
    )

    # Ensure colors are applied correctly - force color assignment
    for i, race in enumerate(top_races["Race"]):
        if race in race_colors:
            fig_race.data[i].marker.color = race_colors[race]
        else:
            # Fallback to cycling through colors
            fallback_colors = [
                "#FF5733",
                "#33C1FF",
                "#9D33FF",
                "#33FF57",
                "#FFC733",
                "#FF33A8",
                "#334BFF",
            ]
            fig_race.data[i].marker.color = fallback_colors[i % len(fallback_colors)]

    # Additional styling
    fig_race.update_traces(marker_line_width=0, opacity=0.8)

    st.plotly_chart(fig_race, use_container_width=True)


def main() -> None:
    """Main function to run the NYPD arrests dashboard.

    Parameters
    ----------
    None
        This function takes no parameters.

    Returns
    -------
    None
        This function runs the dashboard application.

    Purpose
    -------
    This function serves as the entry point for the NYPD arrests dashboard application.
    It handles data loading, sidebar controls, and orchestrates the creation of
    all dashboard sections including overview, geographic analysis, temporal analysis,
    and demographic analysis.
    """
    try:
        # Load data
        st.sidebar.markdown("### Data Loading")

        start_date_str = st.sidebar.date_input(
            "Start Date:",
            value=datetime(2006, 1, 1),
            min_value=datetime(2006, 1, 1),
            max_value=datetime.now(),
            key="start_date_input",
            help="Select the start date for filtering arrests (inclusive)",
        )
        end_date_str = st.sidebar.date_input(
            "End Date:",
            value=datetime.now(),
            min_value=datetime(2006, 1, 1),
            max_value=datetime.now(),
            key="end_date_input",
            help="Select the end date for filtering arrests (inclusive)",
        )

        # Sample size option for testing
        sample_size = st.sidebar.selectbox(
            "Sample Size:",
            options=[
                100000,
                500000,
                1000000,
                1500000,
                2000000,
                2500000,
                3000000,
                3500000,
                4000000,
                4500000,
                5000000,
                5500000,
                6000000,
            ],
            index=0,
            key="sample_size_select",
            help="Number of rows to sample from the date-filtered data",
        )

        if st.sidebar.button("Load Data", key="load_data_button"):
            try:
                # Validate date range
                if start_date_str >= end_date_str:
                    st.sidebar.error("Start date must be before end date!")
                    return

                # Convert date inputs to datetime objects
                start_date = datetime.combine(start_date_str, datetime.min.time())
                end_date = datetime.combine(end_date_str, datetime.max.time())

                # Load full dataset only once (cached)
                if "full_df" not in st.session_state:
                    st.session_state.full_df = load_full_nypd_data(
                        "nypd_arrests_dataset.csv"
                    )

                # Apply filters and sampling to the cached full dataset
                st.session_state.df = filter_and_sample_data(
                    st.session_state.full_df, sample_size, start_date, end_date
                )

                # Store the filtered date range for display purposes
                st.session_state.filtered_date_range = f"{start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')}"
                st.success("Data loaded successfully!")
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                st.stop()

        # Check if data is loaded
        if "df" not in st.session_state:
            st.info("Please load the dataset using the sidebar controls.")
            st.stop()

        df = st.session_state.df

        # Create dashboard sections
        display_dataset_overview(df)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your data file and try again.")


if __name__ == "__main__":
    main()
