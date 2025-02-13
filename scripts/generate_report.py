from fpdf import FPDF
import pandas as pd
import os

class TradingReportGenerator:
    def __init__(self, data_path, report_path):
        self.data_path = data_path
        self.report_path = report_path
        self.df = None
        self.pdf = None

    def load_data(self):
        if not os.path.exists(self.data_path):
            print(f"Error: {self.data_path} not found.")
            exit()
        self.df = pd.read_csv(self.data_path)

    def create_pdf(self):
        self.pdf = PDFReport()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()

    def add_title(self):
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(200, 10, "Portfolio Performance Summary", ln=True, align="L")
        self.pdf.ln(5)

    def add_summary_statistics(self):
        self.pdf.set_font("Arial", "", 12)
        summary_text = f"""
        Total Portfolios Analyzed: {len(self.df)}
        Average ROI: {self.df["ROI"].mean():.2f}%
        Highest ROI: {self.df["ROI"].max():.2f}%
        Lowest ROI: {self.df["ROI"].min():.2f}%
        Average Profit & Loss (PnL): ${self.df["PnL"].mean():,.2f}
        """
        self.pdf.multi_cell(0, 10, summary_text)
        self.pdf.ln(5)

    def add_top_performers(self):
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(200, 10, "Top 5 Performing Portfolios", ln=True, align="L")
        self.pdf.ln(5)

        self.pdf.set_font("Arial", "", 11)
        top_performers = self.df.sort_values(by="ROI", ascending=False).head(5)

        for index, row in top_performers.iterrows():
            self.pdf.cell(200, 10, f"Port ID: {int(row['Port_ID'])}, ROI: {row['ROI']:.2f}%, PnL: ${row['PnL']:,.2f}", ln=True)
        self.pdf.ln(10)

    def add_insights(self):
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(200, 10, "Insights & Recommendations", ln=True, align="L")
        self.pdf.ln(5)

        self.pdf.set_font("Arial", "", 11)
        insights = """
        - Traders with high ROI generally have a higher Sharpe Ratio, indicating better risk management.
        - Portfolios with high Profit Factors tend to have higher Win Rates.
        - Some portfolios show extremely high drawdowns (MDD), meaning they took high risks.
        - Diversifying across multiple assets can reduce risk exposure and increase profitability.
        """
        self.pdf.multi_cell(0, 10, insights)

    def save_pdf(self):
        self.pdf.output(self.report_path)
        print(f"✅ Report generated successfully: {self.report_path}")

    def generate_report(self):
        self.load_data()
        self.create_pdf()
        self.add_title()
        self.add_summary_statistics()
        self.add_top_performers()
        self.add_insights()
        self.save_pdf()

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(200, 10, "Trading Analysis Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

if __name__ == "__main__":
    data_path = "/home/anand/Videos/data science/output/top_portfolios.csv"
    report_path = "/home/anand/Videos/data science/reports/trading_report.pdf"
    report_generator = TradingReportGenerator(data_path, report_path)
    report_generator.generate_report()
