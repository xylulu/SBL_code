#!/usr/bin/env python3
"""
Calibrate zero current measurements using electrode_8mA files as baseline.
Calculate baseline current for each rfd/tbs combination and adjust all traces in electrode_local.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
import json

# ===== CONFIGURATION =====
CALIBRATION_FOLDER = Path("/Users/xylu/Desktop/Data/electrode_8mA")
DATA_FOLDER = Path("/Users/xylu/Desktop/Data/electrode_local")
OUTPUT_FOLDER = Path("/Users/xylu/Desktop/Data/electrode_local_calibrated")
BASELINE_FILE = Path("/Users/xylu/Desktop/Data/baseline_currents.json")

# Smoothing parameters (same as in photocurrent processing)
smoothing_window_size = 300
baseline_time_min = -1200  # µs
baseline_time_max = -200   # µs

# Time shifts for file types
time_shifts = {
    'rfd4tbs2': 8.707,
    'rfd10tbs1': 10.320,
    'rfd11tbs1': -0.205,
    'rfd11tbs2': -0.205
}

# ===== HELPER FUNCTIONS =====

def extract_file_id(filename):
    """Extract rfd/tbs identifier from filename.
    E.g., '20260131_220406_rfd11tbs1.csv' -> 'rfd11tbs1'
    """
    stem = filename.stem
    parts = stem.split('_')
    if len(parts) >= 3:
        return parts[-1]  # rfd*tbs*
    return None


def read_and_process_calibration_file(file_path):
    """Read calibration file and extract baseline current.
    
    Returns:
        dict: Contains 'baseline_current', 'channels', 'raw_trace', 'smoothed_trace'
    """
    filename = file_path.name
    file_id = extract_file_id(file_path)
    is_rfd11 = 'rfd11' in filename
    
    # Detect header row
    skip_rows = 4
    ntrigger_val = None
    try:
        with open(file_path, 'r', errors='ignore') as f:
            for i in range(15):
                line = f.readline()
                if "Ntrigger" in line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        ntrigger_val = parts[1].strip()
                if line.startswith('CH1'):
                    skip_rows = i
                    break
    except Exception as e:
        print(f"Warning: Could not read header from {filename}: {e}")
        pass
    
    # Read channels
    try:
        if is_rfd11:
            df = pd.read_csv(file_path, skiprows=skip_rows, usecols=['CH1', 'CH2', 'CH3'])
            channels = ['CH1', 'CH2', 'CH3']
        else:
            df = pd.read_csv(file_path, skiprows=skip_rows, usecols=['CH1'])
            channels = ['CH1']
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None
    
    # Calculate time in microseconds
    time_us = np.arange(len(df)) * 75e-9 * 1e6 - 1400
    
    # Apply time shift
    if file_id in time_shifts:
        time_us = time_us + time_shifts[file_id]
    
    # Process each channel to calculate baseline
    baseline_currents = {}
    
    for ch_name in channels:
        try:
            ch_data = df[ch_name].values.copy()
            
            # Convert raw data to current in mA
            current_mA = ch_data / 10 / 50 * 1000  # 10x probe, 50Ω resistor, to mA
            
            # Apply smoothing filter
            smoothed_current = np.convolve(current_mA, np.ones(smoothing_window_size)/smoothing_window_size, mode='same')
            
            # Find baseline region (-1200 to -200 µs)
            baseline_mask = (time_us >= baseline_time_min) & (time_us <= baseline_time_max)
            baseline_region = smoothed_current[baseline_mask]
            
            if len(baseline_region) > 0:
                baseline_current = np.mean(baseline_region)
                baseline_currents[ch_name] = float(baseline_current)
            else:
                print(f"Warning: No data in baseline region for {filename} {ch_name}")
                baseline_currents[ch_name] = 0.0
                
        except Exception as e:
            print(f"Error processing {filename} {ch_name}: {e}")
            baseline_currents[ch_name] = 0.0
    
    return {
        'file_id': file_id,
        'filename': filename,
        'channels': channels,
        'baseline_currents': baseline_currents,
        'is_rfd11': is_rfd11
    }


def calculate_baseline_map():
    """Process all calibration files and create a baseline map.
    Groups by file_id (rfd*tbs*) and averages multiple files.
    
    Returns:
        dict: Map of file_id -> baseline currents for each channel
    """
    baseline_map = defaultdict(lambda: defaultdict(list))
    
    if not CALIBRATION_FOLDER.exists():
        print(f"Error: Calibration folder not found: {CALIBRATION_FOLDER}")
        return {}
    
    cal_files = sorted(CALIBRATION_FOLDER.glob("*.csv"))
    print(f"\nReading {len(cal_files)} calibration files from {CALIBRATION_FOLDER.name}...")
    
    for cal_file in cal_files:
        result = read_and_process_calibration_file(cal_file)
        if result:
            file_id = result['file_id']
            print(f"  ✓ {result['filename']:40} {file_id}: {result['baseline_currents']}")
            
            for ch_name, baseline_val in result['baseline_currents'].items():
                baseline_map[file_id][ch_name].append(baseline_val)
    
    # Average multiple files for same file_id
    averaged_baselines = {}
    for file_id, channels in baseline_map.items():
        averaged_baselines[file_id] = {}
        for ch_name, values in channels.items():
            avg_baseline = np.mean(values)
            averaged_baselines[file_id][ch_name] = float(avg_baseline)
            if len(values) > 1:
                print(f"  Averaged {len(values)} files for {file_id} {ch_name}: {avg_baseline:.6f} mA")
    
    return averaged_baselines





def save_baseline_reference(baseline_map):
    """Save baseline reference for documentation."""
    try:
        with open(BASELINE_FILE, 'w') as f:
            json.dump(baseline_map, f, indent=2)
        print(f"\nBaseline reference saved to: {BASELINE_FILE}")
    except Exception as e:
        print(f"Error saving baseline reference: {e}")


# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    print("="*70)
    print("ZERO CURRENT CALIBRATION")
    print("="*70)
    
    # Step 1: Calculate baseline from calibration files
    baseline_map = calculate_baseline_map()
    
    if not baseline_map:
        print("\nError: No baselines calculated. Exiting.")
        exit(1)
    
    print(f"\n{'='*70}")
    print(f"BASELINE SUMMARY")
    print(f"{'='*70}")
    for file_id in sorted(baseline_map.keys()):
        print(f"{file_id:20} {baseline_map[file_id]}")
    
    # Save baseline reference
    save_baseline_reference(baseline_map)
    
    print(f"\n{'='*70}")
    print("DONE")
    print(f"{'='*70}")
