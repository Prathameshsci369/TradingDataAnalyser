

# **Trading Data Analyser 📊🚀**  
A **robust data analysis pipeline** for **Binance trade history**, designed to process, analyze, and visualize trading data. This project calculates **key financial metrics**, ranks portfolios, generates visual insights, and provides an **automated trading report in PDF format**.

---

## **📌 Features**  
✅ **Data Processing & Cleaning** – Parses trade history, validates data, and removes inconsistencies.  
✅ **Financial Metrics Calculation** – Computes **ROI, PnL, Sharpe Ratio, MDD, Win Rate**, and more.  
✅ **Portfolio Ranking** – Scores and ranks top-performing portfolios based on profitability.  
✅ **Exploratory Data Analysis (EDA)** – Generates key insights using **Seaborn & Matplotlib visualizations**.  
✅ **Automated PDF Reports** – Summarizes key findings, top traders, and recommendations.  
✅ **Modular & Scalable** – Supports future enhancements like **real-time data streaming**.

---

## **📁 Project Structure**  
```plaintext
TradingDataAnalyser/
│── data/                      # Raw & processed trade history files
│   ├── trade_history.csv       # Input trade history data
│   
│── logs/                       # Logs for debugging & tracking execution
│── output/                     # Stores final CSV results & analysis
│── reports/                    # Generated reports & visualizations
│   ├── plots/                  # Trading insights visualizations
│   ├── trading_report.pdf      # Automated PDF report
│── scripts/                    # Core Python scripts
│   ├── main.py                 # Main execution pipeline
│   ├── trading_analyzer.py      # Data processing & analysis module
│   ├── eda.py                  # Exploratory Data Analysis (EDA) script
│   ├── generate_report.py       # Automated PDF report generator
│── README.md                    # Project documentation
│── requirements.txt              # Required Python dependencies
│── .gitignore                    # Ignore unnecessary files in Git
```

---

## **🚀 Installation & Setup**  
### **🔹 Step 1: Clone the Repository**
```sh
git clone https://github.com/Prathameshsci369/TradingDataAnalyser.git
cd TradingDataAnalyser
```

### **🔹 Step 2: Create a Virtual Environment (Optional)**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **🔹 Step 3: Install Dependencies**
```sh
pip install -r requirements.txt
```

---

## **📌 How to Run the Project**
### **🔹 1. Run the Main Pipeline**
```sh
python scripts/main.py
```
This will **clean data, compute financial metrics, rank portfolios, and generate results.**  

### **🔹 2. Perform Exploratory Data Analysis (EDA)**
```sh
python scripts/eda.py
```
This will generate visual insights like:
- **ROI Distribution**
- **Risk vs Return Analysis**
- **Win Rate vs Total Positions**
- **Portfolio Growth Over Time**

### **🔹 3. Generate the Trading Report (PDF)**
```sh
python scripts/generate_report.py
```
The final report will be saved in:
```plaintext
reports/trading_report.pdf
```

---

## **📊 Key Financial Metrics Calculated**
| Metric | Description |
|--------|------------|
| **ROI (%)** | Return on Investment (Profit % based on initial capital) |
| **PnL ($)** | Total Profit/Loss generated |
| **Sharpe Ratio** | Risk-adjusted return metric |
| **MDD (Max Drawdown)** | Largest peak-to-trough portfolio loss |
| **Win Rate (%)** | Percentage of profitable trades |
| **Profit Factor** | Ratio of total profit to total loss |

---

## **📌 Example Output (`top_portfolios.csv`)**
| Port_ID | ROI (%) | PnL ($) | Sharpe Ratio | MDD | Win Rate (%) | Total Positions | Profit Factor |
|---------|--------|--------|--------------|------|--------------|----------------|--------------|
| 3826087012661391104 | 27.03 | 532.66 | 9.7 | -7.6e+21 | 91.3 | 69 | 16.08 |
| 4029506971304830209 | 6.04 | 2413.65 | 23.81 | 0.0 | 60.0 | 5 | 1899.27 |
| 4037282461943784704 | 0.5 | 4760.37 | 24.78 | 0.0 | 78.16 | 174 | 2.98 |

---

## **📌 Visual Insights Generated**
🔹 **Histogram of ROI (%)**  
🔹 **Risk vs Return: Sharpe Ratio vs ROI Scatter Plot**  
🔹 **Win Positions vs Total Positions (Bar Chart)**  
🔹 **Portfolio Growth Over Time (Line Chart)**  

All visualizations are saved in:  
```plaintext
reports/plots/
```

---

## **🛠 Future Improvements**
✅ **Automate real-time trading data fetching from Binance API**  
✅ **Integrate Streamlit for interactive visual dashboards**  
✅ **Expand to include multi-asset portfolio analysis**  
✅ **Machine Learning predictions for trade optimization**  

---

## **📌 Contributing**
We welcome contributions! If you'd like to **improve the analysis**, **add new features**, or **fix bugs**, follow these steps:
1. **Fork** the repository.
2. **Create a new branch** (`feature-new-analysis`).
3. **Commit your changes** (`git commit -m "Added new feature"`)
4. **Push to GitHub** (`git push origin feature-new-analysis`)
5. **Submit a Pull Request!** 🎉

---

## **📜 License**
This project is licensed under the **MIT License**. You are free to use, modify, and distribute this project with proper attribution.

---

## **📞 Contact**
🔹 **GitHub**: [Prathameshsci369](https://github.com/Prathameshsci369)  
🔹 **Email**: *prathameshsci963@gmail.com* 

---

### **🚀 Ready to analyze your trading data? Let's get started!**
🔥 **Star** the repo if you found this useful! 🌟  
🔄 **Fork & contribute** to make it even better! 🚀  

---

