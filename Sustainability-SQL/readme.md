# 🌳 Sustainability Project (SQL)
## SQL Data Analysis Project: Global Sustainability Performance 🌍

This repository contains the complete SQL workflow for an in-depth **Sustainability Data Analysis Project**. This project covers the entire data pipeline, from data cleaning and transformation to building an optimized Star Schema (Data Warehouse) and extracting critical business insights.

The entire process was conducted using advanced SQL techniques to ensure data quality, integrity, and analytical performance.

---

## Project Overview 📊

The objective of this project was to analyze a dataset related to global product sustainability performance, focusing on key environmental metrics, brand behavior, and market trends. The analysis aims to uncover correlations, identify leading brands and countries, and assess the impact of factors like recycling and material choice on overall sustainability ratings.

| Project Stage | Focus | Key Deliverable | Icon |
| :--- | :--- | :--- | :--- |
| **Data Cleaning & Standardization** | Consistency & Integrity | Clean `raw_data` table. | 🧹 |
| **Outlier & Missing Value Handling** | Data Quality | Winsorized Numeric Data (IQR method). | 🔬 |
| **Data Modeling** | Performance & Scalability | Optimized Star Schema (Fact & Dimension Tables). | 🏗️ |
| **Statistical Analysis** | Relationships | Pearson Correlation Matrix. | 📈 |
| **Insight Generation** | Business Value | Key Performance Indicators (KPIs) & In-depth Queries. | 💡 |

---

## 1. Data Cleaning & Standardization 🧹

The initial stage focused on rigorous data preparation within the `raw_data` table to ensure uniformity and accuracy.

### Key Cleaning Techniques Used:
* **Text Standardization:** Used `TRIM()`, `CONCAT()`, `UPPER()`, and `LOWER()` functions to **Title Case** all qualitative columns (`brand_name`, `country_name`, etc.) for consistency.
* **Boolean Standardization:** Standardized various representations of Yes/No values (e.g., '1', 'y', 'true', 'yes') into a uniform **'Yes'** or **'No'** using detailed `CASE` statements.
* **Renewable Status Unification:** Grouped variations like 'fully renewable' and 'fully' into **'Fully Renewable'** and handled partial status with a `LIKE` condition.
* **Duplicate Check:** Verified the absence of duplicates based on the new `raw_id` primary key.

## 2. Data Quality Management 🔬

Addressing deviations in the numeric data was critical for reliable analysis.

### Outlier Handling (Winsorizing):
* **Methodology:** The **Interquartile Range (IQR) method** was applied to detect and cap outliers in five key numeric columns: `sustainability_rating`, `average_price`, `carbon_footprint`, `water_usage`, and `waste_production`.
* **Advanced SQL:** Complex SQL variables (`@Q1`, `@Q3`, `@lower`, `@upper`), `PREPARE` statements, and `FLOOR()`/`CEIL()` functions were used to dynamically calculate quartile positions and bounds.
* **Winsorizing:** The `LEAST()` and `GREATEST()` functions were used to cap values at the calculated upper and lower bounds, effectively minimizing the impact of extreme outliers.

### Missing Values:
* A dedicated query was used to identify the count of **`NULL` values** for every column, providing a clear map for subsequent imputation or filtering strategies.

---

## 3. Data Modeling (Star Schema) 🏗️

The cleaned data was transformed into an analytical **Star Schema** to optimize query performance and simplify complex reporting.

### Dimension Tables (The 'Who, Where, When'):
Seven dimension tables were created to house descriptive attributes, normalizing the data and minimizing redundancy:
1.  `brand_dim` (Brand Name, Category)
2.  `country_dim` (Country, Region)
3.  `year_dim` (Year)
4.  `material_dim` (Material Type, Renewable Status)
5.  `product_category_dim` (Product Category, Target Audience)
6.  `certification_dim` (Certification Type)
7.  `market_trend_dim` (Market Trend, Trend Score)

### Fact Table (The 'What Happened'):
* `sustainability_fact`: The central table containing all measurable metrics (`sustainability_rating`, `carbon_footprint`, `water_usage`, etc.) and the foreign keys linking to the seven dimension tables.

### Post-Modeling Preprocessing:
* **Renaming:** Columns were renamed for clarity (`renewable` $\rightarrow$ `material_status`, `product_line` $\rightarrow$ `product_category`).
* **Data Correction:** Specific value corrections were applied (e.g., 'Americas' $\rightarrow$ 'America', 'None' $\rightarrow$ 'Not Certified').

---

## 4. Key Performance Indicators (KPIs) & Analysis 💡

The final step involved extracting insights through a set of powerful analytical queries.

### Statistical Correlation:
* Used the **Pearson Correlation** formula in SQL to quantify the linear relationship between the `sustainability_rating` and the key environmental and financial metrics.

### Key Performance Indicators (KPIs):
* A **`KPIs` View** was created to provide a quick executive summary of the data, including:
    * Average environmental metrics (Price, Carbon Footprint, Water/Waste usage).
    * Min/Max Sustainability Ratings.
    * Counts of Yes/No for Eco-friendly Manufacturing and Recycling Programs.
    * Counts by **Sustainability Status** (Fully/Partially/Not Sustainable).

### Advanced Analysis Queries:
A variety of queries were used to drive deeper analysis, including:

* **Top/Bottom Performance:** Identifying the **Top 10 most sustainable brands** and **Top 5 product categories**.
* **Geographic Analysis:** Comparing sustainability across **countries** and **regions**.
* **Product Performance:** Analyzing average waste, water, and carbon metrics *per* **product category**.
* **Impact Analysis:** Assessing the effect of **Recycling Programs** and **Certifications** on the overall sustainability rating.
* **Time Series:** Tracking **sustainability improvements over time** by year.
* **Price Elasticity:** Categorizing products into **price ranges** to determine if higher cost correlates with higher sustainability.
