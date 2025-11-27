# 🌳  Sustainability Project (PowerBI)

## 1. Project Title:  Sustainability Dashboard Analysis  🌍

***

## 2. Overview 💡

This project features a comprehensive **Sustainability Performance Dashboard** built on **Microsoft Power BI**. It is designed to track, analyze, and optimize the organization's environmental footprint, product ratings, and efficiency metrics across the supply chain. The solution is crucial for ESG reporting, operational teams, and management seeking immediate, data-driven insights to meet strategic sustainability targets, enhance brand reputation, and manage resource efficiency.

***

## 3. Key Objectives 🎯

The dashboard is structured to address the following critical business dimensions:

* **Environmental Footprint:** 💨 Monitor core resource consumption metrics like **AVG Waste Production, AVE Water Usage,** and **AVG Carbon FootPrint**.
* **Product & Brand Ratings:** ⭐ Analyze **Min/Max Sust Ratings**, compare **Sustainability Rating by Brand Name,** and track **Distribution of Material Renewability** to inform R&D and marketing strategies.
* **Logistics & Financial Impact:** 💰 Connect **Sales** and **Logistics Cost** with the environmental impact metrics, such as **Carbon Footprint for Logistics** and **AVG Carbon Footprint by country\_name**.
* **Operational Efficiency:** ⚙️ Track **Water\_Efficiency** and **Carbon\_Efficiency** across different product lines, and analyze the correlation between **AVG Price and AVG Sustainability** to optimize sourcing.
* **Geographic Analysis:** 🗺️ Pinpoint high-impact **Countries** for carbon and water usage to focus abatement efforts.

***

## 4. Dashboard Breakdown & Key Insights 📊

The solution comprises four functional screens: **Executive KPIs, Environmental Snapshot (D1), Product & Rating Analysis (D2), Financial & Logistics (D3),** and **Brand & Efficiency (D4)**.

### **Executive KPIs: The Summary 📈**

This screen pulls high-level, aggregate metrics from the entire report for quick executive status checks.

| Icon | Key Metric | Description |
| :---: | :--- | :--- |
| **🗑️** | **AVG Waste Production** | The average waste generated (e.g., $6.23$ units). |
| **🌊** | **AVE Water Usage** | The average water consumed across operations (e.g., $654$ units). |
| **☁️** | **AVG Carbon FootPrint** | The overall average carbon footprint (e.g., $30$ units). |
| **💵** | **Total Sales** | The total realized revenue monitored in the system (e.g., $2.5\text{B}$). |
| **🏅** | **Min/Max Sust Rating** | The range of sustainability ratings across products (1 to 5). |
| **🚚** | **Carbon Footprint for Logistics** | The specific carbon output associated with supply chain logistics (e.g., $15$ units). |

---

### **Dashboard 1: Environmental Snapshot (D1) & Product Ratings (D2)** 💨

This section combines the high-level environmental outputs with initial product and pricing analysis.

| Icon | Visualization | Core Metrics & Insights |
| :---: | :--- | :--- |
| **🗺️** | **AVE Carbon Footprint for each country** | Bar chart showing geographic distribution of carbon output (e.g., Italy, Brazil, Turkey). |
| **📊** | **Environmental impact for top 5 countries** | Bi-metric chart comparing carbon footprint and water usage by country sustainability rating. |
| **🌱** | **Sustainability rate for eco/non-eco** | Donut chart showing the proportional split of products by eco-friendly criteria. |
| **📦** | **Product line by sustainability rating** | Bar chart comparing sustainability scores across product categories (e.g., Clothing, Garden, Kitchenware). |
| **⏳** | **Average of sustainability\_rating over year** | Line chart tracking the performance of the overall sustainability rating over time. |
| **♻️** | **Distribution of material renewability** | Pie chart showing the proportional split of materials (Fully Renew., Partially Renew., Not Renew.). |
| **💲** | **Avg price for every brand category** | Pie chart showing average price distribution across brand categories (Local, Startup, Multinational). |

---

### **Dashboard 2: Financial & Logistics Impact (D3) & Brand Efficiency (D4)** 💰

This section focuses on the operational, financial, and brand-specific details of sustainability performance.

| Icon | Visualization | Core Metrics & Insights |
| :---: | :--- | :--- |
| **📈** | **Sales by Product Line** | Bar chart and Donut chart showing revenue breakdown across different product categories. |
| **🧭** | **Logistics cost by country\_name** | Table detailing the cost of logistics per country for operational planning. |
| **📉** | **AVG Price and AVG Carbon Footprint** | Scatter Plot showing the relationship between price and carbon output by product line. |
| **✨** | **sustainability\_rating by brand\_name** | Bar chart ranking brands based on their sustainability scores. |
| **✅** | **Water\_Efficiency and Carbon\_Efficiency** | Detailed table comparing the efficiency of water and carbon usage across product lines. |
| **🧱** | **sustainability\_rating by material\_type** | Treemap showing the sustainability rating influence of specific materials (Hemp, Glass, Recycled plastic). |
| **🎯** | **Correlation between AVG price and AVG Sustainability** | Scatter Plot analyzing if higher prices correlate with higher sustainability scores. |

***

## 5. Interactivity and Usage 🖱️

This dashboard is highly interactive, utilizing **Slicers and Cross-Filtering** for granular, multi-dimensional analysis.

* **Slicers (Filtering):** 🔍 Use the **country\_name, product\_line, brand\_name,** and **year** slicers to dynamically focus all charts and KPIs on a specific market segment or time period.
* **Cross-Filtering (Deep Dive):** 🔗 Clicking on any element (e.g., a specific "product\_line" in one chart or "Recycled plastic" in the material treemap) will instantly filter every other visual on the report to show the associated sales, carbon footprint, and efficiency metrics.

### **How to Use:** ▶️

1.  Open the sustainability Project file in your data visualization software (**Power BI Desktop**).
2.  Navigate sequentially between the report tabs for a comprehensive review.
3.  Use the **Slicers** to select specific *Countries, Product Lines,* or *Brands* for focused analysis.
4.  Interact directly with the charts to analyze trends and gain strategic insights into operational and brand sustainability performance.

***

## 6. Others 📁

### **Technology** 💻

The entirety of this reporting suite is developed and maintained within the **Microsoft Power BI** environment. Accessing the full functionality requires Power BI Desktop or the Power BI Service.

### **Repository Structure** 💾

| Icon | Area | Description |
| :---: | :--- | :--- |
| **📂** | **Core Asset** | The primary analytical file is the Power BI report (`Sustainability Project.pbix`). All data connections, data models, calculations, and visualizations are encapsulated within this single file. |
| **📄** | **Documentation** | This README provides the necessary technical and content context. 

