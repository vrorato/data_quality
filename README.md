# E-commerce Data Quality & Preparation Pipeline

## 📌 Business Context

Store 1 is an e-commerce company migrating historical customer and order data to a new
analytics and data warehouse environment. During migration, data quality issues emerged,
compromising trust in analytics and decision-making.

This project simulates a real-world data quality remediation scenario and delivers
clean, validated, and analytics-ready datasets.

---

## 🎯 Objectives

- Audit data quality across customer and order datasets
- Detect missing values, duplicates, invalid timestamps, and integrity issues
- Apply cleaning and standardization rules
- Implement reusable data validation schemas
- Deliver clean datasets for downstream analytics and ML

---

## 🗂️ Dataset

**Source:** Brazilian E-Commerce Public Dataset (Kaggle)

The original dataset is highly clean.  
To better reflect real-world production environments, controlled data quality issues were
intentionally introduced and fully documented.

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Pandera (Data Validation)
- Matplotlib / Seaborn

---

## 🔍 Data Quality Issues Simulated

- Missing ZIP codes
- Duplicate customer records
- Invalid future timestamps
- Broken referential integrity between orders and customers

---

## ⚙️ Pipeline Steps

1. Data ingestion
2. Controlled data corruption (simulation)
3. Data type standardization
4. Schema-based validation
5. Cleaning and integrity enforcement
6. Export of analytics-ready datasets

---

## 📈 Results

- Reduced duplicate customer records
- Enforced referential integrity across datasets
- Standardized timestamps and categorical fields
- Delivered clean datasets ready for analytics and machine learning
- Created reusable validation schemas for future pipelines

---

## 🚀 Next Steps

- Customer segmentation
- Churn prediction
- Customer Lifetime Value (LTV) modeling
- Integration with a cloud data warehouse

---

## 👤 Author

Data Science & Analytics Portfolio Project
