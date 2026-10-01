# FSQRN Analytics

## Overview

**FSQRN Analytics** is a full-stack analytics platform designed to transform Food Safety, Quality, Regulatory and Nutrition (FSQRN) data into a centralized view of supplier and quality performance.

The platform combines a Python data pipeline, PostgreSQL database, FastAPI backend and React dashboard to support data validation, supplier risk analysis, inspection monitoring, quality incident tracking and corrective-action management.

The project demonstrates how operational FSQRN data can be transformed from structured datasets into an interactive analytics platform that helps users identify supplier risks, monitor quality performance and investigate operational issues.

The application uses synthetic data created specifically for this portfolio project.


## Problem

FSQRN teams can work with information across multiple operational areas, making it difficult to maintain a consistent view of supplier performance, inspections, quality incidents and corrective actions.

This project addresses that challenge by creating a centralized analytics platform that brings these data areas together and converts them into structured performance and risk information.

The goal is to demonstrate how data engineering, analytics, databases, APIs and interactive visualisation can be combined to support operational decision-making.

## Objectives

The platform was developed to:

- Centralize FSQRN-related operational data.
- Validate and structure data before analysis.
- Store operational data in a relational PostgreSQL database.
- Monitor food safety inspection performance.
- Analyse supplier inspection and failure rates.
- Identify suppliers with higher levels of operational risk.
- Track quality incidents and their seriousness.
- Monitor corrective actions and closure status.
- Provide interactive dashboards for exploring operational performance.
- Expose analytics through a REST API.
- Demonstrate an end-to-end data analytics workflow from data generation to business insight.


## Technology Stack

### Data Engineering & Analytics

- Python
- Pandas

### Database

- PostgreSQL
- SQL

### Backend

- FastAPI
- Uvicorn

### Frontend

- React
- JavaScript
- Vite

### Data Visualisation

- Recharts
- Interactive web dashboards

### Development & Version Control

- Git
- GitHub
- Visual Studio Code


## Project Architecture

```text
The platform follows an end-to-end data analytics architecture:

Synthetic FSQRN Data
        ↓
Python Data Generation & Validation
        ↓
PostgreSQL Database
        ↓
SQL Queries & Risk Calculations
        ↓
FastAPI REST API
        ↓
React Frontend
        ↓
Interactive FSQRN Analytics Dashboard
```

## Architecture Components

**Data Layer**

Synthetic operational datasets are generated and validated using Python and Pandas before being loaded into PostgreSQL.

**Database Layer**

PostgreSQL provides the central relational data store for suppliers, products, inspections, quality incidents and corrective actions.

**Analytics Layer**

SQL queries and Python-based calculations are used to analyse inspection performance, supplier failure rates, quality incidents and supplier risk.

**Backend Layer**

FastAPI exposes the underlying data and analytics through REST API endpoints consumed by the frontend.

**Frontend Layer**

The React application presents KPIs, charts, filters, tables and supplier-level drill-down information through an interactive dashboard.

**Visualisation Layer**

Recharts is used to transform analytical results into interactive charts for monitoring FSQRN performance and supplier risk.

# Dataset

The project uses synthetic data created specifically to simulate FSQRN operational data.

The current dataset contains:

| Data Area          | Records |
| ------------------ | ------: |
| Suppliers          |      50 |
| Products           |     150 |
| Inspections        |     500 |
| Quality Incidents  |     250 |
| Corrective Actions |     250 |

The dataset covers multiple countries and operational records across the period from January 2025 to September 2026.

Because the data is synthetic, the results are intended to demonstrate the analytics workflow rather than represent real company performance.

## Core Data Areas

The platform currently works with five core operational data areas:

- **Suppliers** — supplier information and performance data.
- **Products** — product information associated with the FSQRN dataset.
- **Inspections** — food safety inspection results and inspection history.
- **Quality Incidents** — reported quality incidents, including seriousness and status.
- **Corrective Actions** — actions taken in response to identified issues, including closure status and dates.

These datasets are stored in PostgreSQL and exposed through the FastAPI backend for use by the React dashboard.

## Analytics & Risk Assessment

A supplier risk model was developed to demonstrate how operational inspection and incident data can be combined into a supplier risk indicator.

The demonstration model considers three main components:

### Inspection Failure Score

Supplier inspection failure performance contributes to the overall risk score.

### Serious Incident Score

The number of serious quality incidents contributes to supplier risk.

### Incident Frequency Score

The overall frequency of quality incidents contributes additional risk points.

These three components are combined into a maximum total risk score of 12, which is converted into a percentage-based risk score.

### Risk Categories

Suppliers are classified into three categories:

- **High Risk**
- **Medium Risk**
- **Low Risk**

The resulting risk information is used throughout the dashboard to support supplier monitoring, comparison and prioritisation.

The risk model is a demonstration framework created specifically for this portfolio project and is **not an industry-standard FSQRN risk methodology**.

## Key Performance Indicators

The dashboard provides metrics and analytical views including:

- Total number of suppliers
- Supplier risk classification
- Supplier failure rate
- Inspection pass and fail performance
- Quality incident volume
- Serious quality incidents
- Corrective action status
- Corrective action closure information
- Average supplier risk score
- Supplier-level risk and performance information

The platform also provides filtering and drill-down capabilities, allowing users to move from high-level performance indicators to individual supplier records and inspection history.

## Key Results

The current synthetic dataset produced the following results:

- **50 suppliers** analysed.
- **7 suppliers** classified as high risk.
- **17 suppliers** classified as medium risk.
- **26 suppliers** classified as low risk.
- **500 inspections** analysed.
- **260 inspections passed.**
- **240 inspections failed.**
- Average supplier risk score: **42.33%**.
- Average supplier inspection failure rate: **48.12%**.

These results demonstrate how operational data can be transformed into supplier-level risk indicators and dashboard-based performance insights.

## Dashboard Features

The React dashboard provides several views for exploring the data.

## Dashboard

Provides a high-level overview of supplier risk and inspection performance through KPI cards and interactive charts.

## Suppliers

Provides supplier risk classification, failure rates, search and filtering functionality.

## Supplier Details

Allows users to investigate individual suppliers and review their associated performance and inspection history.

## Inspections

Provides inspection records and visualises inspection pass/fail performance.

## Quality Incidents

Provides visibility into reported quality incidents and their status and seriousness.

## Corrective Actions

Tracks corrective actions, their status and closure information.

## API

The FastAPI backend provides REST endpoints that connect the React dashboard to the underlying data and analytics.

Key endpoints include:

`GET /`
`GET /dashboard/summary`
`GET /suppliers/risk`
`GET /suppliers/{supplier_id}`
`GET /inspections`
`GET /incidents`
`GET /corrective-actions`

The API can also be explored through FastAPI's automatically generated interactive documentation:

http://127.0.0.1:8000/docs

## Project Structure

```text
FSQRN_Analytics/
├── analytics/
│   ├── generate_data.py
│   └── validate_data.py
├── backend/
│   └── main.py
├── database/
│   ├── schema.sql
│   └── load_data.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   └── ...
├── data/
│   ├── raw/
│   └── processed/
├── tests/
├── .gitignore
├── README.md
└── ...

### Folder Responsibilities

- **`analytics/`** — synthetic data generation and data validation.
- **`backend/`** — FastAPI application and REST API endpoints.
- **`database/`** — PostgreSQL schema and data-loading scripts.
- **`frontend/`** — React dashboard and data visualisations.
- **`data/`** — raw and processed datasets.
- **`tests/`** — project testing and validation.

## Data Validation

Data validation is performed before the datasets are used for analysis.

The validation process checks the generated datasets for issues such as:

- Missing values
- Invalid records
- Data consistency
- Required fields
- Unexpected data conditions

This helps ensure that the data entering the database and analytics workflow is structured and suitable for analysis.

## Development Workflow

The project follows a structured development workflow:

1. Generate synthetic FSQRN data.
2. Validate the datasets using Python.
3. Define the PostgreSQL database schema.
4. Load the datasets into PostgreSQL.
5. Query and analyse the data using SQL and Python.
6. Calculate supplier risk indicators.
7. Develop REST API endpoints using FastAPI.
8. Build the interactive dashboard using React.
9. Connect the frontend to the FastAPI backend.
10. Test the application and refine the dashboard.
11. Version the project using Git and GitHub.

## Project Status

**Status: Completed portfolio project**

The core FSQRN analytics platform has been implemented, including:

- Synthetic FSQRN dataset generation
- Data validation
- PostgreSQL database
- SQL-based data analysis
- Supplier risk scoring
- FastAPI REST API
- React frontend
- Interactive analytics dashboard
- Supplier risk analysis and filtering
- Supplier-level drill-down
- Inspection history
- Quality incident monitoring
- Corrective action monitoring
- Git version control
- GitHub repository

The project demonstrates an end-to-end analytics workflow from data generation and validation through database storage, API development, analysis and interactive visualisation.

## Future Improvements

Potential future improvements include:

- Deploying the application to the cloud.
- Adding authentication and role-based access.
- Adding automated data ingestion from external sources.
- Expanding the regulatory and nutrition data models.
- Adding automated scheduled reporting.
- Adding more advanced trend and anomaly detection.
- Adding automated alerts for high-risk suppliers.
- Expanding the testing suite.
- Adding production monitoring and logging.

## Limitations

This project has several intentional limitations:

- The dataset is synthetic and does not represent real operational data.
- The risk model is a demonstration framework rather than an industry-standard methodology.
- The application is currently designed as a portfolio demonstration rather than a production FSQRN management system.
- External data integrations have not been implemented.
- Authentication and user permissions have not been implemented.

These limitations provide opportunities for future development while keeping the current project focused on demonstrating full-stack analytics capabilities.

## Disclaimer

This is a portfolio and learning project using synthetic data created for demonstration purposes.

The data, supplier information, inspection results, quality incidents, corrective actions and risk scores do not represent real company data or real operational performance.

The risk-scoring methodology is a demonstration framework developed for this project and should not be interpreted as an industry-standard FSQRN risk methodology.

The project is not affiliated with or connected to Starbucks or any other company's internal systems, data or operations.
