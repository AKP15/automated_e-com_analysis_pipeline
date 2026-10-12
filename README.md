# Automated E-commerce Data Analysis Pipeline

## Project Overview

This project is a Python-based automated data analysis pipeline designed to simulate a real-world data analyst internship project.

The pipeline automatically loads raw e-commerce data, validates data quality, cleans and standardizes the data, calculates business KPIs, performs sales analysis, generates CSV outputs and charts, verifies the results, logs the execution process, and runs automatically on a schedule using APScheduler.

The main goal of this project is to move from one-time data analysis toward a reusable and automated analytics workflow.

## Objectives

The main objectives of this project are:

- Build a complete data analysis pipeline using Python
- Detect data-quality problems automatically
- Clean and standardize raw data
- Calculate important business KPIs
- Perform business analysis
- Generate automated analysis outputs
- Generate charts
- Implement logging and error handling
- Automate pipeline execution
- Organize the project using a modular structure
- Practice a real-world data analyst workflow

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- APScheduler
- Python Logging
- pathlib
- CSV

## Project Structure

project/
│
├── data/
│   ├── raw/
│   │   └── ecommerce_orders_raw.csv
│   │
│   └── outputs/
│       ├── kpis.csv
│       ├── sales_by_product.csv
│       ├── sales_by_category.csv
│       ├── sales_by_channel.csv
│       └── sales_by_month.csv
│
├── src/
│   ├── load.py
│   ├── validation.py
│   ├── cleaner.py
│   ├── analyzer.py
│   └── logger.py
│
├── main.py
│
└── README.md

## Pipeline Workflow

Raw Data
   ↓
Load Data
    ↓
First Validation
    ↓
Data Cleaning
    ↓
Second Validation 
    ↓
KPI Calculation
    ↓
Business Analysis
    ↓
Generate CSV Outputs
    ↓
Generate Charts
    ↓
Verify Outputs
    ↓
Pipeline Completed

## Generated Output

data/outputs/
│
├── kpis.csv
├── sales_by_product.csv
├── sales_by_category.csv
├── sales_by_channel.csv
└── sales_by_month.csv

## Logging
STEP 1: Loading data
STEP 2: First validation
STEP 3: Cleaning
STEP 4: Second validation
STEP 5: Generating outputs
STEP 6: Generating charts
STEP 7: Verifying outputs
PIPELINE COMPLETED

## How to Run

```bash
pip install pandas numpy matplotlib apscheduler
python main.py

```







