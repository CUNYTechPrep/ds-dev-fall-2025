# Data Lineage for tickets


tickets-per-price-per-day.csv

format column names
convert time to datetime


`/workspaces/ds-dev-fall-2025/Week-03-EDA-and-Dashboards/data/tickets/ParkingViolationCodes_January2020.xlsx` 
data dict // lookup table is excel
pip install openpyxl

standardize col names

merge tickets to tickets to data dict on violation_code



keep only columns needed, order them as date, description, n tickets

cols_to_keep = ['dt_issue_date', 'violation_description', 'tickets_issued']

Save that file to new csv `processed_tickets_per_day_with_description.csv`
