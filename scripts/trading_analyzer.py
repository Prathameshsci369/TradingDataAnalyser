import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from pathlib import Path
import os
import sys
import datetime as datetime
import ast
class TradingAnalyzer:
    def __init__(self, data_path: str):
        """
        Initialize TradingAnalyzer with path to trade history data
        """
        self.data_path = Path(data_path)
        self.trade_data = None
        self.project_root = self.setup_project_structure()
        self.metrics = {}
        self.logger = self.setup_logging()  # ✅ FIXED: Removed `_setup_logging()`
    
    def setup_project_structure(self):
        """
        Create necessary project directories
        """
        try:
            project_root = Path(__file__).parent.parent
            
            directories = [
                project_root / 'logs',
                project_root / 'output',
                project_root / 'reports',
                project_root / 'reports' / 'plots',
                project_root / 'scripts' / 'logs'
            ]
            
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {directory}")
                
            return project_root

        except Exception as e:
            print(f"Error setting up project structure: {str(e)}")
            sys.exit(1)

    def setup_logging(self):
        """
        Set up logging configuration
        """
        try:
            log_file = self.project_root / 'logs' / 'trading_analysis.log'
            logging.basicConfig(
                filename=log_file, 
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            logger = logging.getLogger(__name__)
            print(f"Logging setup complete. Log file: {log_file}")
            return logger  # ✅ FIXED: Logging correctly returned

        except Exception as e:
            print(f"Error setting up logging: {str(e)}")
            sys.exit(1)

    def analyze(self):
        """
        Perform trading analysis
        """
        try:
            self.logger.info("Starting trading analysis...")
            # Analysis logic goes here
            self.logger.info("Trading analysis completed successfully.")

        except Exception as e:
            self.logger.error(f"Error during analysis: {str(e)}")
            print(f"Error during analysis: {str(e)}")
            sys.exit(1)

    

    

    def load_data(self, data_path: Path) -> None:
        """
        Load and preprocess trade history data by flattening nested Trade_History.
        """
        try:
            self.logger.info(f"Loading data from {data_path}")

            # Read CSV file
            self.trade_data = pd.read_csv(data_path)

            # Log available columns
            self.logger.info(f"Columns found in CSV: {list(self.trade_data.columns)}")

            # Remove leading/trailing spaces in column names
            self.trade_data.columns = self.trade_data.columns.str.strip()

            # Rename 'Port_IDs' to 'Port_ID' for consistency
            if 'Port_IDs' in self.trade_data.columns:
                self.trade_data.rename(columns={"Port_IDs": "Port_ID"}, inplace=True)
            else:
                raise KeyError("Missing expected column 'Port_IDs' in CSV.")

            # Check if 'Trade_History' column exists
            if 'Trade_History' not in self.trade_data.columns:
                raise KeyError("Column 'Trade_History' not found in dataset.")

            # Flatten Trade_History (Convert JSON-like strings into dictionaries)
            flattened_data = []

            for _, row in self.trade_data.iterrows():
                try:
                    trade_list = ast.literal_eval(row["Trade_History"])  # Convert string to list of dicts
                    for trade in trade_list:
                        trade["Port_ID"] = row["Port_ID"]  # Now using correct 'Port_ID'
                        flattened_data.append(trade)
                except Exception as e:
                    self.logger.warning(f"Skipping malformed trade history: {e}")

            # Convert to DataFrame
            self.trade_data = pd.DataFrame(flattened_data)

            # Rename 'time' to 'timestamp' for consistency
            if 'time' in self.trade_data.columns:
                self.trade_data.rename(columns={"time": "timestamp"}, inplace=True)

            # Log new structure
            self.logger.info(f"Flattened data shape: {self.trade_data.shape}")
            self.logger.info(f"Columns after flattening: {list(self.trade_data.columns)}")

            # Convert timestamp to datetime format
            if 'timestamp' in self.trade_data.columns:
                self.trade_data['timestamp'] = pd.to_datetime(self.trade_data['timestamp'], unit='ms', errors='coerce')
            else:
                raise KeyError("Missing column 'timestamp' after processing.")

            # Ensure all required columns exist before proceeding
            required_columns = {"Port_ID", "timestamp", "side", "positionSide", "price", "quantity", "realizedProfit"}
            missing_columns = required_columns - set(self.trade_data.columns)

            if missing_columns:
                raise KeyError(f"Missing columns in data after flattening: {missing_columns}")

            self.logger.info("Trade data successfully loaded and flattened.")

        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise

    

    


       

    def calculate_position_type(self) -> None:
        """
        ट्रेड्सना पोझिशन प्रकारांमध्ये वर्गीकृत करा (long_open, long_close, short_open, short_close)
        """
        try:
            # ट्रेड्सना पोझिशन प्रकारांमध्ये वर्गीकृत करण्यासाठी अटी सेट करा
            conditions = [
                (self.trade_data['side'] == 'BUY') & (self.trade_data['positionSide'] == 'LONG'),  # खरेदी आणि लाँग पोझिशन
                (self.trade_data['side'] == 'SELL') & (self.trade_data['positionSide'] == 'LONG'),  # विक्री आणि लाँग पोझिशन
                (self.trade_data['side'] == 'SELL') & (self.trade_data['positionSide'] == 'SHORT'),  # विक्री आणि शॉर्ट पोझिशन
                (self.trade_data['side'] == 'BUY') & (self.trade_data['positionSide'] == 'SHORT')  # खरेदी आणि शॉर्ट पोझिशन
            ]
            # प्रत्येक अटीसाठी पोझिशन प्रकार निवडा
            choices = ['long_open', 'long_close', 'short_open', 'short_close']
            # अटींनुसार पोझिशन प्रकार सेट करा, जर कोणतीही अट जुळली नाही तर 'unknown' सेट करा
            self.trade_data['position_type'] = np.select(conditions, choices, default='unknown')
            
            # पोझिशन प्रकारांची पडताळणी करा
            unknown_positions = len(self.trade_data[self.trade_data['position_type'] == 'unknown'])
            if unknown_positions > 0:
                self.logger.warning(f"Found {unknown_positions} trades with unknown position type")  # अज्ञात पोझिशन प्रकार असलेल्या ट्रेड्सची संख्या लॉग करा
                
            self.logger.info("Position types calculated successfully")  # यशस्वीरित्या पोझिशन प्रकारांची गणना झाल्याचे लॉग करा
            
        except Exception as e:
            self.logger.error(f"Error calculating position types: {str(e)}")  # पोझिशन प्रकारांची गणना करताना त्रुटी असल्यास लॉग करा
            raise

    def calculate_metrics(self, port_id: str) -> Dict:
        """
        Calculate trading metrics for a specific portfolio
        """
        try:
            port_data = self.trade_data[self.trade_data['Port_ID'] == port_id].copy()
            
            if len(port_data) == 0:
                self.logger.warning(f"No data found for portfolio {port_id}")
                return None
            
            # Calculate basic metrics
            total_positions = len(port_data[port_data['position_type'].isin(['long_close', 'short_close'])])
            win_positions = len(port_data[port_data['realizedProfit'] > 0])
            
            # Calculate ROI
            total_investment = port_data[port_data['position_type'].isin(['long_open', 'short_open'])]['quantity'].sum()
            total_profit = port_data['realizedProfit'].sum()
            roi = (total_profit / total_investment * 100) if total_investment != 0 else 0
            
            # Calculate win rate
            win_rate = (win_positions / total_positions * 100) if total_positions != 0 else 0
            
            # Calculate daily returns for Sharpe Ratio
            daily_returns = port_data.groupby(port_data['timestamp'].dt.date)['realizedProfit'].sum()
            
            # Calculate Sharpe Ratio (assuming risk-free rate of 0 for simplicity)
            if len(daily_returns) > 1:  # Need at least 2 days of data
                sharpe_ratio = np.sqrt(252) * (daily_returns.mean() / daily_returns.std()) if daily_returns.std() != 0 else 0
            else:
                sharpe_ratio = 0
            
            # Calculate Maximum Drawdown
            if len(daily_returns) > 0:
                cumulative_returns = (1 + daily_returns).cumprod()
                rolling_max = cumulative_returns.expanding().max()
                drawdowns = cumulative_returns / rolling_max - 1
                max_drawdown = drawdowns.min() * 100
            else:
                max_drawdown = 0
            
            # Calculate additional metrics
            avg_profit_per_trade = total_profit / total_positions if total_positions > 0 else 0
            profit_factor = (
                abs(port_data[port_data['realizedProfit'] > 0]['realizedProfit'].sum()) /
                abs(port_data[port_data['realizedProfit'] < 0]['realizedProfit'].sum())
                if abs(port_data[port_data['realizedProfit'] < 0]['realizedProfit'].sum()) != 0
                else float('inf')
            )
            
            metrics = {
                'Port_ID': port_id,
                'ROI': round(roi, 2),
                'PnL': round(total_profit, 2),
                'Sharpe_Ratio': round(sharpe_ratio, 2),
                'MDD': round(max_drawdown, 2),
                'Win_Rate': round(win_rate, 2),
                'Win_Positions': win_positions,
                'Total_Positions': total_positions,
                'Avg_Profit_Per_Trade': round(avg_profit_per_trade, 2),
                'Profit_Factor': round(profit_factor, 2)
            }
            
            self.logger.info(f"Calculated metrics for portfolio {port_id}")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating metrics for portfolio {port_id}: {str(e)}")
            raise

    def analyze_all_portfolios(self) -> pd.DataFrame:
        """
        Analyze all portfolios and return results as DataFrame
        """
        try:
            self.logger.info("Starting analysis of all portfolios")
            results = []
            
            for port_id in self.trade_data['Port_ID'].unique():
                metrics = self.calculate_metrics(port_id)
                if metrics:
                    results.append(metrics)
                    
            results_df = pd.DataFrame(results)
            self.logger.info(f"Completed analysis of {len(results)} portfolios")
            return results_df
            
        except Exception as e:
            self.logger.error(f"Error analyzing portfolios: {str(e)}")
            raise

    def get_top_portfolios(self, n: int = 20) -> pd.DataFrame:
        """
        Get top N portfolios based on weighted scoring
        """
        try:
            results_df = self.analyze_all_portfolios()
            
            # Define weights for each metric
            weights = {
                'ROI': 0.3,
                'Sharpe_Ratio': 0.25,
                'Win_Rate': 0.2,
                'MDD': 0.15,  # Note: Higher MDD is worse
                'Profit_Factor': 0.1
            }
            
            # Normalize metrics
            for column in weights.keys():
                if column != 'MDD':
                    results_df[f'{column}_normalized'] = (results_df[column] - results_df[column].min()) / \
                                                       (results_df[column].max() - results_df[column].min())
                else:
                    # Inverse normalization for MDD (lower is better)
                    results_df[f'{column}_normalized'] = 1 - (results_df[column] - results_df[column].min()) / \
                                                       (results_df[column].max() - results_df[column].min())
            
            # Calculate weighted score
            results_df['total_score'] = sum(
                results_df[f'{metric}_normalized'] * weight 
                for metric, weight in weights.items()
            )
            
            # Sort and get top N
            top_portfolios = results_df.nlargest(n, 'total_score')
            
            # Select columns for output
            output_columns = ['Port_ID', 'ROI', 'PnL', 'Sharpe_Ratio', 'MDD', 
                            'Win_Rate', 'Win_Positions', 'Total_Positions', 
                            'Avg_Profit_Per_Trade', 'Profit_Factor', 'total_score']
            
            self.logger.info(f"Generated top {n} portfolios ranking")
            return top_portfolios[output_columns]
            
        except Exception as e:
            self.logger.error(f"Error generating top portfolios: {str(e)}")
            raise
    def save_results(self, output_path: Path) -> None:
        """
        Save analysis results to CSV
        """
        try:
            # Get top portfolios
            top_portfolios = self.get_top_portfolios()
            
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save results
            top_portfolios.to_csv(output_path, index=False)
            self.logger.info(f"Results saved to {output_path}")
            
            # Generate and save summary report
            self.generate_summary_report()
            
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            raise
    

    def generate_summary_report(self) -> str:
        """
        Generate a detailed summary report of the analysis
        """
        try:
            results_df = self.analyze_all_portfolios()
            
            report = f"""
    Trading Analysis Summary Report
    =============================
    Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    Dataset Overview:
    ---------------
    Total Trades Analyzed: {len(self.trade_data):,}
    Date Range: {self.trade_data['timestamp'].min().strftime('%Y-%m-%d')} to {self.trade_data['timestamp'].max().strftime('%Y-%m-%d')}
    Total Portfolios: {len(results_df):,}

    Overall Performance:
    -----------------
    Total Profitable Portfolios: {len(results_df[results_df['PnL'] > 0]):,} ({len(results_df[results_df['PnL'] > 0]) / len(results_df) * 100:.1f}%)
    Average ROI: {results_df['ROI'].mean():.2f}%
    Average Win Rate: {results_df['Win_Rate'].mean():.2f}%
    Average Sharpe Ratio: {results_df['Sharpe_Ratio'].mean():.2f}
    Average Maximum Drawdown: {results_df['MDD'].mean():.2f}%

    Top 5 Portfolios by ROI:
    ----------------------
    {results_df.nlargest(5, 'ROI')[['Port_ID', 'ROI', 'PnL', 'Win_Rate', 'Sharpe_Ratio']].to_string()}

    Top 5 Portfolios by Sharpe Ratio:
    ------------------------------
    {results_df.nlargest(5, 'Sharpe_Ratio')[['Port_ID', 'Sharpe_Ratio', 'ROI', 'MDD', 'Win_Rate']].to_string()}

    Portfolio Statistics:
    ------------------
    Best ROI: {results_df['ROI'].max():.2f}%
    Worst ROI: {results_df['ROI'].min():.2f}%
    Best Win Rate: {results_df['Win_Rate'].max():.2f}%
    Average Profit per Trade: ${results_df['Avg_Profit_Per_Trade'].mean():.2f}
    """
            
            # Save report
            report_path = Path(self.data_path).parent.parent / 'reports' / 'analysis_summary.txt'
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w') as f:
                f.write(report)
                
            self.logger.info(f"Summary report generated and saved to {report_path}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating summary report: {str(e)}")
            raise
        
        
if __name__ == "__main__":
    analyzer = TradingAnalyzer()
    analyzer.analyze()