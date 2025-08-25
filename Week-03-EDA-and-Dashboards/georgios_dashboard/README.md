# 🛒 Superstore Business Analytics Dashboard

## 🎯 **Project Objective**

This project demonstrates the transformation of raw retail data from [Kaggle](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) into actionable business insights through an interactive dashboard. The goal is to teach students how to use data analytics to make real business decisions by analyzing sales performance, customer behavior, and market trends across different dimensions.

### **Learning Objectives**
- **Data-Driven Decision Making**: Learn to use data instead of gut feelings
- **Business Intelligence**: Transform raw data into actionable insights
- **Interactive Dashboards**: Build tools that business users can actually use
- **Strategic Analysis**: Connect data insights to business strategy

---

## 📁 **Project Files and Description**

### **Core Application Files**
- **`superstore_dashboard.py`**: Main Streamlit dashboard application with interactive visualizations
- **`data_processor.py`**: Data processing module that cleans and aggregates the raw dataset
- **`examine_data.py`**: Exploratory data analysis script with detailed data insights
- **`add_state_codes.py`**: Utility script to add state codes for proper map functionality

### **Data Files**
- **`superstore_data.csv`**: Raw retail dataset containing 4 years of global superstore data
- **`processed_data/`**: Directory containing all processed and aggregated data files
  - `geographic_data.csv`: Sales data aggregated by state and region
  - `yearly_data.csv`: Annual sales trends and metrics
  - `monthly_data.csv`: Monthly sales patterns
  - `category_data.csv`: Product category performance
  - `segment_data.csv`: Customer segment analysis
  - `ship_mode_data.csv`: Shipping method analysis
  - `raw_data_data.csv`: Cleaned original dataset
  - `business_kpis.json`: Key performance indicators

### **Documentation Files**
- **`README.md`**: This comprehensive project guide
- **`DASHBOARD_QUESTIONS_README.md`**: Detailed business questions and learning outcomes
- **`requirements.txt`**: Python dependencies and versions

---

## 🚀 **Key Business Questions Answered**

### **🌍 Geographic Performance**
- Which states/regions have the highest sales?
- Which regions are growing fastest?
- Where should we expand our business?

### **📦 Product Strategy**
- What are our best-selling product categories?
- Which products generate the most revenue?
- How do different product categories perform over time?
- Which category-region combinations perform best? 🔥

### **👥 Customer Insights**
- Which customer segments are most valuable?
- How do different customers prefer different products?
- Which regions have the best customer base?

### **📈 Business Growth**
- What's our sales trend over the past 4 years?
- Which markets show the strongest growth?
- Are there seasonal patterns in our sales?

---

## ⚙️ **Technical Requirements**

### **Python Version**
- **Python 3.12.1**

### **Required Libraries**
```
numpy
pandas
plotly
plotly-express
python-dateutil
streamlit
```

---

## 🛠️ **Setup and Installation**

### **Step 1: Environment Setup**
```bash
# Create and activate virtual environment
python -m venv .ds-dev-fall-2025-venv
.\.ds-dev-fall-2025-venv\Scripts\activate  # Windows
source .ds-dev-fall-2025-venv/bin/activate  # Mac/Linux
```

### **Step 2: Install Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt
```

### **Step 3: Verify Installation**
```bash
# Check if Streamlit is installed correctly
streamlit --version
```

---

## 📋 **How to Run the Project (Step by Step)**

### **Step 1: Data Processing**
First, process the raw data to create aggregated datasets:
```bash
# Run the data processor
python data_processor.py
```
This will:
- Load and clean the `superstore_data.csv` file
- Create geographic, temporal, category, and segment aggregations
- Generate business KPIs
- Save all processed data to the `processed_data/` directory

### **Step 1.5: Add State Codes (Required for Maps)**
The choropleth map requires state codes to display properly:
```bash
# Run the state codes utility
python add_state_codes.py
```
This will:
- Add 2-letter state codes to the geographic data
- Enable proper map visualization with colors
- Fix the "white map" issue that occurs without state codes

### **Step 2: Explore the Data (Optional)**
Run the exploratory data analysis to understand the dataset:
```bash
# Run the data examination script
python examine_data.py
```
This provides detailed insights about:
- Data structure and quality
- Business metrics and patterns
- Sample data and statistics

### **Step 3: Launch the Dashboard**
Start the interactive Streamlit dashboard:
```bash
# Run the main dashboard application
streamlit run superstore_dashboard.py
```
The dashboard will open in your default web browser at `http://localhost:8501`

---

## 🎮 **Dashboard Features**

### **Interactive Visualizations**
- **📊 Key Business Metrics**: Real-time KPIs that update with filters
- **🗺️ Choropleth Maps**: Sales performance across US states
- **📈 Time Series Charts**: Sales trends over 4 years
- **🔥 Heatmaps**: Category-region performance patterns
- **📊 Bar Charts**: Category and segment comparisons
- **🏆 Top Performers**: Interactive tables with progress bars

### **Dynamic Filters**
- **📅 Year Selection**: Analyze specific time periods (2015-2018)
- **🌍 Region Filter**: Focus on specific geographic areas
- **📦 Category Filter**: Drill down into product categories
- **🔄 Reset All Filters**: Return to default view

### **Real-Time Analytics**
- **Total Sales**: Overall business performance
- **Growth Rates**: Year-over-year performance changes
- **Market Share**: Regional and category performance
- **Customer Metrics**: Segment-specific insights

---

## 🔧 **Development Process and Steps Taken**

### **Phase 1: Project Planning**
1. **Dataset Selection**: Chose Superstore retail dataset for business insights
2. **Business Questions**: Identified key questions
3. **Dashboard Structure**: Planned visualization types and layout

### **Phase 2: Data Processing**
1. **Data Cleaning**: Handled missing values and date conversions
2. **Aggregation**: Created geographic, temporal, category, and segment summaries
3. **KPI Calculation**: Generated business performance metrics
4. **Data Validation**: Ensured data quality and consistency

### **Phase 3: Dashboard Development**
1. **Core Structure**: Built main dashboard layout and navigation
2. **Visualizations**: Implemented charts, maps, and tables
3. **Interactive Filters**: Added dynamic filtering capabilities
4. **Data Integration**: Connected all visualizations to processed data

---

## 🚨 **Important Notes**

### **Map Functionality Requirement**
The `add_state_codes.py` script is **essential** for the choropleth map to work properly. Without running this script:
- The map will appear white with no colors
- Geographic data won't display correctly
- The dashboard will show map errors

**Always run `python add_state_codes.py` after `python data_processor.py`**

---

### **Learning Resources**
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Plotly Documentation**: https://plotly.com/python/
- **Pandas Documentation**: https://pandas.pydata.org/docs/

---