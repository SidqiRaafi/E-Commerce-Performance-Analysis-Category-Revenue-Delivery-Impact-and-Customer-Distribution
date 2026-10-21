# Brazilian E-Commerce Performance Analysis

[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-Data%20Analysis-3776AB?logo=python&logoColor=white)](#)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?logo=pandas&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end data analytics and business intelligence case study evaluating the operational performance of Olist, a Brazilian E-Commerce platform. This project covers extensive data wrangling, exploratory data analysis (EDA), advanced geospatial mapping, and an interactive dashboard deployment using Streamlit.

📊 **[Live Interactive Dashboard (Streamlit Cloud)](https://sidqi-brazilian-ecommerce-performance-analysis.streamlit.app/)**  
📊 **[Exploratory Data Analysis Notebook](notebook.ipynb)**

---

## 1. Executive Summary & Business Problem
Olist recorded **96,478 unique orders** generating **R$ 13.22M** in revenue between 2016 and 2018. The objective of this project is to analyze the platform's historical transaction data to optimize product catalogs, evaluate logistics performance, and map customer demographics.

**SMART Business Questions:**
1. **Revenue Contribution:** Which product categories generated the highest and lowest total gross revenue (BRL) over the 2016–2018 period, and how should we optimize the catalog based on this?
2. **Logistics & Reputation:** How severely does a missed delivery estimate impact the average customer review score (scale 1-5), and what is the current failure rate of our logistics network?
3. **Geospatial Demographics (Advanced Analysis):** What is the geographical distribution of unique customers across Brazilian states, and how should this dictate fulfillment center placements to optimize last-mile delivery?

---

## 2. Data Wrangling & Preprocessing (Python)
The raw data consisted of multiple relational tables (customers, orders, items, products, reviews, and geolocation) requiring extensive preprocessing before analysis.

### Data Quality & Processing Logic
* **Gathering & Merging:** Consolidated 5+ relational datasets using SQL-style `pd.merge()` operations to create a unified master dataframe.
* **Category Translation (`product_category_name_english`):** Standardized product category text from Portuguese to English using the provided `product_category_name_translation.csv` mapping.
* **Missing Value Handling:** 
  * Imputed or dropped missing logistical timestamps (`order_delivered_customer_date`) primarily associated with formally canceled or lost orders.
  * Handled missing product attributes (weight, dimensions) using median imputation to preserve row integrity.
* **Deduplication & Geospatial Cleaning:** Removed duplicate spatial coordinates and invalid zip code prefixes in the geolocation dataset to ensure accurate plotting.

---

## 3. Exploratory Data Analysis & Business Dashboard
![Dashboard](dashboard/images/kpi.png)
Designed an interactive Streamlit dashboard featuring Gestalt visual principles, executive scorecards, and advanced spatial plotting.

### A. Category Revenue Performance
![Top Categories](dashboard/images/category_revenue.png)
* **Top Revenue Drivers:** The `health_beauty` category leads the platform with **R$ 1.23M** in cumulative sales, followed closely by `watches_gifts` (R$ 1.17M) and `bed_bath_table` (R$ 1.02M).
* **Underperforming Segments:** Niche or service-oriented categories like `security_and_services` generated a negligible contribution of only **R$ 283** over the entire three-year period.

### B. The Cost of Logistical Delays
![Logistics Impact](dashboard/images/logistics_impact.png)
* **Baseline Satisfaction:** Orders completed on or before the estimated delivery date account for **91.9%** (96.5K orders) of total volume, maintaining a solid average review score of **4.29 / 5.00**.
* **Reputation Penalty:** The **7,826 orders (8.1%)** that missed their delivery estimates caused average review scores to plummet drastically to **2.57 / 5.00**.

### C. Advanced Analysis: Geospatial Demographics
![Geospatial Mapping](dashboard/images/geospatial_mapping.png)
* **Coastal Dominance:** Geospatial scatter plotting reveals massive market polarization. **São Paulo (SP)** controls absolute market share with **40,501 customers**, followed by Rio de Janeiro (RJ) and Minas Gerais (MG).
* **Topography Challenges:** The northern and western regions (Amazon basin) exhibit heavily dispersed, low-density customer distribution, representing high-cost, inefficient logistical zones.

---

## 4. Conclusion & Strategic Recommendations

### Conclusions
1. The platform's revenue is heavily concentrated in lifestyle, personal care, and home goods, while micro-categories (e.g., security services, CDs/DVDs) bloat the catalog without generating meaningful revenue.
2. Logistics directly dictate brand reputation. A delayed shipment essentially guarantees a negative customer review (sub-3.0 score).
3. The customer base is heavily centralized in the Southeastern coastal states (SP, RJ, MG), whereas inland and northern territories lack the density to support organic logistical efficiency.

### Business Recommendations (Action Items)
* **Catalog Optimization:** Reallocate digital marketing spend heavily toward the Top 5 categories (`health_beauty`, `watches_gifts`, etc.). Conduct an operational audit on bottom-tier categories to deprecate unprofitable segments and reduce database bloat.
* **Logistics SLA Re-evaluation:** Management must recalibrate the estimated delivery algorithm and penalize or replace underperforming third-party logistics (3PL) carriers responsible for the 7,826 delayed shipments.
* **Fulfillment Center Placement:** Establish localized warehouse hubs specifically within the SP-RJ-MG triangle. This will drastically reduce last-mile delivery costs for the core customer base while sustaining the 4.29 average satisfaction rating.

---

## 5. Technology Stack & Tooling

| Domain | Technology / Tool | Application |
| :--- | :--- | :--- |
| **Data Wrangling** | Python, Pandas, NumPy | Data cleaning, type coercion, relational merging |
| **Data Visualization** | Matplotlib, Seaborn | Exploratory static visualizations |
| **Advanced Analysis** | Python Geospatial Logic | Coordinate mapping (Latitude/Longitude density) |
| **Business Intelligence** | Streamlit | Interactive dashboard deployment and web hosting |

---

## 6. How to Run & Inspect

### Directory Structure
```text
brazilian-ecommerce-performance-analysis
├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
├── data
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

### Local Deployment Instructions
**1. Clone the repository:**
```bash
git clone [https://github.com/SidqiRaafi/brazilian-ecommerce-performance-analysis]
cd https://github.com/SidqiRaafi/brazilian-ecommerce-performance-analysis
```

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the streamlit app:**
```bash
streamlit run dashboard/dashboard.py
```
