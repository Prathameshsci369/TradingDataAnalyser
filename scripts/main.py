from pathlib import Path
import logging
import sys
import os

def setup_logging():
    """
    Set up logging configuration
    """
    try:
        log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'trading_analysis.log')
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging setup complete")
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        sys.exit(1)

def setup_project_structure():
    """
    Create necessary project directories
    """
    try:
        # Get the project root directory (parent of scripts directory)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # Define required directories
        directories = [
            os.path.join(project_root, 'logs'),
            os.path.join(project_root, 'output'),
            os.path.join(project_root, 'reports'),
            os.path.join(project_root, 'reports', 'plots'),
            os.path.join(project_root, 'scripts', 'logs')  # Added missing directory
        ]
        
        # Create directories
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logging.info(f"Created directory: {directory}")
            
        return project_root

    except Exception as e:
        logging.error(f"Error setting up project structure: {str(e)}")
        sys.exit(1)

def verify_data_file(project_root: str) -> str:
    """
    Verify that the data file exists and return its path
    """
    try:
        data_file = os.path.join(project_root, 'data', 'trade_history.csv')
        if not os.path.exists(data_file):
            logging.error(f"Trade history file not found at: {data_file}")
            print("Please ensure trade_history.csv exists in the data directory.")
            sys.exit(1)
        return data_file
    except Exception as e:
        logging.error(f"Error verifying data file: {str(e)}")
        sys.exit(1)

def main():
    # Setup logging
    setup_logging()
    
    # Setup project structure first
    project_root = setup_project_structure()
    
    try:
        # Verify data file exists
        data_file = verify_data_file(project_root)
        
        # Import TradingAnalyzer
        from trading_analyzer import TradingAnalyzer
        
        # Initialize analyzer with project root path
        analyzer = TradingAnalyzer(project_root)
        
        # Load and process data
        analyzer.load_data(data_file)
        logging.info("Data loaded successfully")
        
        analyzer.calculate_position_type()
        logging.info("Position types calculated")
        
        # Generate and save results
        output_path = os.path.join(project_root, 'output', 'top_portfolios.csv')
        analyzer.save_results(output_path)
        
        logging.info("Analysis completed successfully!")
        logging.info(f"Results saved to: {output_path}")
        
    except Exception as e:
        logging.error(f"Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()