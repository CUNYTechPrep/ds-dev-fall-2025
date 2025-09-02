# NYPD Arrests Dashboard

A comprehensive interactive dashboard for analyzing NYPD arrest data from 2006 onwards, built with Streamlit and Plotly. This dashboard provides geographic, temporal, and demographic analysis of arrest patterns across New York City's five boroughs.

## Project Structure

### Files Overview

- **`nypd_dashboard.py`** - Main dashboard application built with Streamlit
  - Interactive visualizations for geographic, temporal, and demographic analysis
  - Date filtering and data sampling capabilities
  - Interactive maps, charts, and statistical summaries
  
- **`download_dataset.py`** - Data acquisition script
  - Downloads NYPD arrest data from NYC Open Data API
  - Downloads approximately 6 million arrest records
  - Saves data as CSV file
  
- **`nypd_arrests_dataset.csv`** - Dataset file (downloaded by download script)
  - Contains arrest records with location, demographics, and offense details
  - Approximately 6 million rows of arrest data
  
- **`requirements.txt`** - Python dependencies for the project

## Setup and Installation


### Installation Steps

- Python 3.12.1

1. **Navigate to the project directory**:
   ```bash
   cd nypd_arrests_dashboard
   ```

2. **Install required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the dataset** (if not already present):
   ```bash
   python download_dataset.py
   ```

## Dependencies

The project requires the following Python packages:

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
plotly-express>=0.4.1
numpy>=1.24.0
python-dateutil>=2.8.0
requests>=2.31.0
tqdm>=4.66.0
```

## How to Run

1. **First, download the dataset**:
   ```bash
   python download_dataset.py
   ```
   - This will download approximately 6 million arrest records
   - Creates `nypd_arrests_dataset.csv` in the project directory

2. **Launch the dashboard**:
   ```bash
   streamlit run nypd_dashboard.py
   ```

### Dashboard Features

- **Geographic Analysis**: Interactive maps showing arrest locations by borough and offense type
- **Temporal Analysis**: Yearly, monthly, and day-of-week arrest patterns
- **Demographic Analysis**: Age, gender, and race distribution of arrestees
- **Interactive Controls**: Borough and offense type filtering for detailed analysis
- **Data Filtering**: Date range selection and data sampling options

## Crime Analysis Questions

### Geographic Analysis
1. **Which borough is the most dangerous based on per capita arrest rates?** - Compare arrest rates per 100,000 residents across all five boroughs
2. **Where are the crime hotspots in Manhattan?** - Use the interactive map to identify high-concentration areas
3. **Which borough has the most diverse crime types?** - Analyze the distribution of different offense categories by location

### Temporal Patterns
4. **What time of year sees the highest crime rates?** - Examine monthly arrest patterns to identify seasonal trends
5. **Are weekends more dangerous than weekdays?** - Compare day-of-week arrest patterns across different boroughs
6. **How have crime rates changed since 2006?** - Analyze yearly trends to see if the city is getting safer or more dangerous

### Demographic Insights
7. **Which ethnic group has the highest arrest rates?** - Compare arrest numbers across different racial categories
8. **What age group is most likely to be arrested?** - Analyze age distribution patterns and identify risk factors
9. **Is there a gender difference in crime patterns?** - Compare male vs. female arrest rates by offense type

### Specific Crime Types
10. **Are pickpocketing crimes concentrated in tourist areas?** - Filter for theft-related offenses and analyze their geographic distribution, particularly around Manhattan tourist destinations

## Data Sources

- **NYC Open Data Dataset**: https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u/about_data
