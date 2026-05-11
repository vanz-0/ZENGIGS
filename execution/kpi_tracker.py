import csv
import os
import argparse
from datetime import datetime

def log_metric(metric_name, value, file_path=".tmp/kpi_tracking.csv"):
    """
    Logs a daily metric (e.g. Emails Sent, Proposals Sent) to a CSV file.
    """
    # Ensure .tmp directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    file_exists = os.path.exists(file_path)
    
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Metric", "Value"])
            
        today = datetime.now().strftime("%Y-%m-%d")
        writer.writerow([today, metric_name, value])
        
    print(f"Logged {metric_name} = {value} for {today} in {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track daily KPIs.")
    parser.add_argument("--metric", required=True, help="Name of the metric (e.g. 'Emails Sent')")
    parser.add_argument("--value", required=True, type=int, help="Numeric value of the metric")
    args = parser.parse_args()
    
    log_metric(args.metric, args.value)
