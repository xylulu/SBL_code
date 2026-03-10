#!/usr/bin/env python3
import os
import glob
import pandas as pd
from datetime import datetime

base_path = "/Users/xylu/Desktop/Data/acoustic_vpp/"
date_str = "20260127"
start_time_str = "000000"
end_time_str = "002000"

# Setup dates
start_time_obj = datetime.strptime(date_str + start_time_str, "%Y%m%d%H%M%S")
end_time_obj = datetime.strptime(date_str + end_time_str, "%Y%m%d%H%M%S")

print(f"Time range: {start_time_obj} to {end_time_obj}")

# Direct path
date_folder = os.path.join(base_path, date_str)
print(f"Folder: {date_folder}")
print(f"Exists: {os.path.exists(date_folder)}")

if os.path.exists(date_folder):
    csv_files = sorted(glob.glob(os.path.join(date_folder, f"{date_str}*.csv")))
    print(f"Found {len(csv_files)} CSV files")
    
    if csv_files:
        # Try loading first 3 files
        for i, csv_file in enumerate(csv_files[:3]):
            print(f"\n--- File {i+1}: {os.path.basename(csv_file)} ---")
            df = pd.read_csv(csv_file)
            print(f"Shape: {df.shape}")
            
            # Convert datetime
            df['time_datetime'] = pd.to_datetime(df['time_datetime'])
            print(f"Date range: {df['time_datetime'].min()} to {df['time_datetime'].max()}")
            
            # Check if there's data in our time range
            mask = (df['time_datetime'] >= start_time_obj) & (df['time_datetime'] <= end_time_obj)
            filtered = df[mask]
            print(f"Rows in time range [{start_time_str}-{end_time_str}]: {len(filtered)}")
