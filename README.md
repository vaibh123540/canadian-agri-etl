# Canadian Agriculture Data Pipeline & Dashboard

### Project Goal
To analyze the stability of Canadian food production (2020-2025) by building an ETL pipeline to process government data and visualizing the results for provincial stakeholders.

### [View the Interactive Tableau Dashboard Here](https://public.tableau.com/app/profile/vaibhav.jain4171/viz/CanadianAgricultureProductionAnalytics/Dashboard1?publish=yes)

### Dashboard Preview
![alt text](https://github.com/vaibh123540/canadian-agri-etl/blob/main/preview.png "Dashboard Preview")

---

### Technical Stack
* **Data Source:** Statistics Canada [Table 32-10-0359-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3210035901)
* **ETL (Python):** `etl_cleaner.py` cleans the raw semi-structured CSV, handling multi-level headers and filtering suppressed data points.
* **Visualization (Tableau):** Hosted on Tableau Public, featuring geospatial filtering and time-series forecasting.

### Key Insights
* **Recovery:** 2024 data shows a full yield recovery for Wheat and Canola following the 2021 drought.
* **Regional Trends:** Saskatchewan continues to lead in Canola production, while Quebec and Ontario dominate the Soybean market.

---

### Repository Structure
* `etl_cleaner.py`: The main Python script for data extraction, transformation, and loading.
* `3210035901-eng.csv`: Raw dataset sourced from the Open Government Portal.
* `cleaned_provincial_crops.csv`: The processed output file used for visualization.
   
