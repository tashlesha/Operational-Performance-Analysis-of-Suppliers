📊 Operational Performance Analysis of Suppliers

🔍 Project Overview

This project analyzes supplier/vendor performance using real-world business data such as purchases, sales, inventory, and freight costs.
The goal is to evaluate supplier efficiency, profitability, and stock movement to support smarter procurement and business decisions.

🎯 Objectives

Measure vendor performance using KPIs
Identify profitable and low-performing suppliers
Analyze cost vs revenue trends
Support data-driven decision-making

🛠️ Tech Stack

Python (Pandas, SQLAlchemy)
SQL / SQLite
Power BI
Excel

📊 Key KPIs

Total Sales vs Purchases
Gross Profit
Profit Margin %
Stock Turnover Ratio
Freight Cost Analysis

Sales-to-Purchase Ratio

🚀 How to Run (Detailed)
1️⃣ Clone Repository
git clone https://github.com/tashlesha/vendor-performance-analysis.git
cd vendor-performance-analysis

2️⃣ Install Dependencies
pip install pandas sqlalchemy

3️⃣ Prepare Data Folder

Create a data folder and place CSV files inside:

project/
 ├── data/
 │    ├── purchases.csv
 │    ├── sales.csv
 │    ├── vendor_invoice.csv
 │    ├── purchase_prices.csv
 │    ├── begin_inventory.csv
 │    └── end_inventory.csv

4️⃣ Run Data Ingestion
python ingestion_db.py


✔ Loads CSVs into SQLite
✔ Creates inventory.db

5️⃣ Run Vendor Analysis
python vendor_summary.py


✔ Creates vendor_sales_summary
✔ Calculates KPIs automatically

6️⃣ View Dashboard

Open Power BI file (.pbix)

Connect to inventory.db

Click Refresh

📌 Key Insights

✅ Top vendors contributing highest profit
✅ Vendors with high freight cost impact
✅ Fast vs slow stock-moving products
✅ Clear supplier comparison metrics

💼 Business Value

This project demonstrates how data analytics can:
Optimize supplier selection
Reduce procurement costs
Improve profitability
Enable strategic decisions

👩‍💻 Author

Ashlesha Tayade
Computer Engineering Student (Data Analytics Enthusiast)
University of Mumbai

