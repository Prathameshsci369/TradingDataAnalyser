import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class PortfolioAnalysis:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "output")
        self.plot_dir = os.path.join(base_dir, "reports", "plots")
        self.file_path = os.path.join(self.data_dir, "top_portfolios.csv")
        self.df = None

    def load_data(self):
        if not os.path.exists(self.file_path):
            print(f"Error: {self.file_path} not found.")
            exit()
        self.df = pd.read_csv(self.file_path)

    def display_summary(self):
        print("\n🔍 Data Summary:")
        print(self.df.describe())

    def check_missing_values(self):
        print("\nMissing values per column:")
        print(self.df.isnull().sum())

    def create_plots(self):
        sns.set_theme(style="whitegrid")
        os.makedirs(self.plot_dir, exist_ok=True)

        # 1. Histogram of ROI
        plt.figure(figsize=(10, 5))
        sns.histplot(self.df["ROI"], bins=20, kde=True, color="blue")
        plt.xlabel("ROI (%)")
        plt.ylabel("Frequency")
        plt.title("Distribution of ROI Among Portfolios")
        plt.savefig(os.path.join(self.plot_dir, "roi_distribution.png"))
        plt.show()

        # 2. Scatter Plot: Sharpe Ratio vs ROI (Risk vs. Return)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.df, x="Sharpe_Ratio", y="ROI", hue="Profit_Factor", size="Total_Positions", palette="coolwarm", sizes=(20, 200))
        plt.xlabel("Sharpe Ratio (Risk-Adjusted Return)")
        plt.ylabel("ROI (%)")
        plt.title("Risk vs Return: Sharpe Ratio vs ROI")
        plt.legend(title="Profit Factor")
        plt.savefig(os.path.join(self.plot_dir, "risk_vs_return.png"))
        plt.show()

        # 3. Bar Chart: Win Positions vs Total Positions
        plt.figure(figsize=(12, 6))
        df_sorted = self.df.sort_values(by="Win_Rate", ascending=False).head(20)  # Top 20 accounts
        sns.barplot(x=df_sorted["Port_ID"].astype(str), y=df_sorted["Total_Positions"], color="gray", label="Total Positions")
        sns.barplot(x=df_sorted["Port_ID"].astype(str), y=df_sorted["Win_Positions"], color="green", label="Win Positions")

        plt.xticks(rotation=90)
        plt.xlabel("Port ID")
        plt.ylabel("Number of Positions")
        plt.title("Win Positions vs Total Positions for Top 20 Portfolios")
        plt.legend()
        plt.savefig(os.path.join(self.plot_dir, "win_vs_total_positions.png"))
        plt.show()

        # 4. Line Chart: Portfolio Growth Over Time (If Available)
        if "timestamp" in self.df.columns:
            self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
            df_sorted = self.df.sort_values("timestamp")

            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df_sorted, x="timestamp", y="PnL", hue="Port_ID")
            plt.xlabel("Time")
            plt.ylabel("Cumulative PnL")
            plt.title("Portfolio Growth Over Time")
            plt.savefig(os.path.join(self.plot_dir, "portfolio_growth.png"))
            plt.show()
        else:
            print("No timestamp data available for portfolio growth visualization.")

if __name__ == "__main__":
    base_dir = os.path.join(os.path.expanduser("~"), "Videos", "data science")
    analysis = PortfolioAnalysis(base_dir)
    analysis.load_data()
    analysis.display_summary()
    analysis.check_missing_values()
    analysis.create_plots()
