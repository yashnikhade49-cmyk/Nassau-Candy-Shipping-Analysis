# Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

An exploratory data analytics project for analyzing shipping route performance, delay patterns, geographic bottlenecks, and shipping-mode characteristics using the Nassau Candy Distributor dataset.

## 📌 Project Overview

This project analyzes shipment data from Nassau Candy Distributor to understand how efficiently products move from factories to customers across different states and regions.

The analysis focuses on:

* Factory-to-customer route performance
* Shipping lead time
* Route efficiency
* Delay patterns
* Geographic performance
* Potential geographic bottlenecks
* Ship mode performance
* Interactive business intelligence through a Streamlit dashboard

The project follows a complete data analytics workflow, from raw dataset inspection and cleaning to exploratory analysis, route evaluation, dashboard development, and business recommendations.

## 🎯 Objectives

The main objectives of the project are to:

1. Inspect and validate the shipment dataset.
2. Clean and prepare the data for analysis.
3. Map products to their corresponding factories.
4. Calculate Shipping Lead Time.
5. Analyze factory-to-customer routes.
6. Develop a relative Route Efficiency Score.
7. Identify comparatively high lead-time shipments using a data-driven benchmark.
8. Identify potential geographic bottlenecks.
9. Compare shipping modes.
10. Develop an interactive Streamlit dashboard.
11. Generate business insights and recommendations.

## 📊 Dataset

The dataset contains:

* **10,194 shipment records**
* **18 original attributes**
* **15 products**
* **5 factories**
* **4 shipping modes**

### Original Attributes

The dataset includes information such as:

* Order ID
* Order Date
* Ship Date
* Ship Mode
* Customer ID
* City
* State/Province
* Region
* Product ID
* Product Name
* Sales
* Units
* Gross Profit
* Cost

The original dataset did not contain a factory field. A product-to-factory mapping was therefore applied to enable factory-to-customer route analysis.

## 🏭 Factory Mapping

The project uses five factories:

* Lot's O' Nuts
* Wicked Choccy's
* Sugar Shack
* Secret Factory
* The Other Factory

All 15 products were successfully mapped to a factory.

## 🔧 Data Processing and Feature Engineering

The following analytical features were created:

### Shipping Lead Time

Calculated as:

`Ship Date − Order Date`

### Route

Defined as:

`Factory → Customer State/Province`

### Region Route

Defined as:

`Factory → Customer Region`

### Delay Frequency

Calculated as the percentage of shipments exceeding the selected analytical delay benchmark.

### Route Efficiency Score

A relative 0–100 efficiency score was developed using reversed Min-Max normalization of average Shipping Lead Time.

Higher scores represent better relative route efficiency within the analyzed dataset.

## 📈 Analysis Performed

### Exploratory Data Analysis

The project examines:

* Shipping mode distribution
* Regional shipment distribution
* Factory distribution
* Shipping Lead Time distribution
* State-level shipment volume
* Product shipment volume
* Factory and regional performance

### Route Efficiency Analysis

Routes are evaluated using:

* Shipment volume
* Average lead time
* Minimum lead time
* Maximum lead time
* Delayed shipments
* Delay frequency
* Route Efficiency Score

For reliable route comparisons, routes with at least 10 shipments were considered.

### Delay Analysis

An initial 5-day threshold was found unsuitable because it classified all shipments as delayed.

A data-driven benchmark based on the **75th percentile of Shipping Lead Time (1,638 days)** was therefore used for relative delay analysis.

This benchmark is an analytical reference for this dataset and should not be interpreted as an operational Service Level Agreement (SLA).

### Geographic Analysis

States were evaluated using:

* Shipment volume
* Average Shipping Lead Time
* Delay frequency

States showing combinations of relatively high shipment activity and weaker performance indicators were classified as potential geographic performance concerns.

These classifications indicate analytical patterns and do not establish the actual cause of operational bottlenecks.

### Ship Mode Analysis

The following shipping modes were compared:

* Standard Class
* Second Class
* First Class
* Same Day

Performance was examined using shipment volume, lead time, delay frequency, cost, and sales.

## 🚨 Key Findings

Some important findings from the analysis include:

* Shipping performance varies considerably across factory-to-customer routes.
* All 15 products were successfully mapped to 5 factories.
* The 5-day delay threshold was unsuitable for this dataset.
* The 75th-percentile Shipping Lead Time was **1,638 days**.
* **Wicked Choccy's → New Mexico** recorded 11 delayed shipments out of 17, giving a delay frequency of **64.71%**.
* **Lot's O' Nuts → New Mexico** recorded 10 delayed shipments out of 18, giving a delay frequency of **55.56%**.
* Geographic analysis identified states requiring further investigation based on shipment volume, lead time, and delay frequency.
* Route Efficiency Scores provide a standardized relative comparison between routes.

## 📊 Streamlit Dashboard

An interactive Streamlit dashboard was developed to make the analysis accessible without directly working with the underlying datasets.

The dashboard provides:

* Region filter
* State filter
* Ship Mode filter
* Order Date filter
* Maximum Shipping Lead Time filter
* KPI cards
* Route Efficiency Overview
* Geographic Shipping Map
* Ship Mode Performance Comparison
* Route Drill-Down
* Geographic Bottleneck Analysis

### Dashboard KPIs

The dashboard displays:

* Total Shipments
* Total Routes
* Average Lead Time
* Delay Frequency
* Average Cost
* Average Sales

## 📁 Project Structure

```text
Nassau-Candy-Shipping-Analysis/
│
├── data/
│   ├── raw/
│   │   └── nassau_candy.csv
│   └── processed/
│       ├── cleaned_data.csv
│       ├── factory_mapped_data.csv
│       ├── feature_engineered_data.csv
│       ├── route_efficiency_analysis.csv
│       ├── final_route_efficiency_analysis.csv
│       ├── geographic_bottleneck_analysis.csv
│       ├── ship_mode_performance_analysis.csv
│       ├── business_insights_summary.csv
│       └── dashboard_validation_results.csv
│
├── notebooks/
│   ├── 01_dataset_inspection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_factory_mapping.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_eda.ipynb
│   ├── 06_route_analysis.ipynb
│   ├── 07_efficiency_score.ipynb
│   ├── 08_geographic_analysis.ipynb
│   ├── 09_ship_mode_analysis.ipynb
│   ├── 10_final_insights.ipynb
│   └── 11_dashboard_validation.ipynb
│
├── app/
│   ├── app.py
│   └── components/
│       ├── charts.py
│       ├── maps.py
│       └── metrics.py
│
├── reports/
│   ├── research_paper/
│   └── executive_summary/
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## ▶️ How to Run the Dashboard

### 1. Clone the repository

```bash
git clone <repository-url>
cd Nassau-Candy-Shipping-Analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit application

```bash
streamlit run app/app.py
```

The dashboard will then open in the browser.

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* Streamlit
* Jupyter Notebook

## 📌 Limitations

The dataset does not contain several operational factors such as:

* Carrier information
* Transportation distance
* Vehicle information
* Warehouse capacity
* Traffic conditions
* Weather conditions
* Real-time shipment status

Therefore, the analysis is primarily descriptive and exploratory and does not establish causal relationships.

The unusual Shipping Lead Time values in the dataset also affect the interpretation of delay-related results.

## 🔮 Future Scope

Future development could include:

* Predictive delay modeling
* Real-time shipment monitoring
* Route optimization
* Carrier performance analysis
* Transportation-distance analysis
* Time-series forecasting
* Automated alerts
* Cost optimization
* Integration with business systems

## 👤 Author

**Yash Nikhade**

Bachelor of Engineering
Computer Science and Engineering
Academic Session: 2026–2027

## 📄 Project Type

Data Analytics / Supply Chain Analytics / Business Intelligence

## 📜 License

This project is intended for educational and portfolio purposes.
