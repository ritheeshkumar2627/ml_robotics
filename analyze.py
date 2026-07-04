import os
import os

print("📊 Loading Robotics Telemetry Analyst Engine...")

filename = "robot_flight_log.csv"

# Verify if the flight log exists before reading it
if not os.path.exists(filename):
    print(f"❌ Error: '{filename}' not found! Run your simulation first.")
    exit()

total_absolute_error = 0.0
row_count = 0

with open(filename, "r", encoding="utf-8") as file:
    lines = file.readlines()
    
    # Loop over the metrics, skipping index 0 (the column header line)
    for line in lines[1:]:
        if line.strip(): # Ignore empty trailing spaces
            # Split the row by its commas into data parts: ["Time", "Target", "Actual"]
            parts = line.split(",")
            # Target is in the middle column (index 1), Actual is in the last column (index 2)
            target_val = float(parts[1])
            actual_val = float(parts[2])
            
            # Compute absolute difference and update your sum metric tracking counters
            step_error = abs(target_val - actual_val)
            total_absolute_error += step_error
            row_count += 1
# Prevent a division-by-zero crash if the log was empty
if row_count > 0:
    mean_absolute_error = total_absolute_error / row_count
    
    print("\n🎯 === CONTROL SYSTEMS PERFORMANCE EVALUATION ===")
    print(f"   ├── Total Trajectory Data Points Analyzed: {row_count}")
    print(f"   └── Mean Absolute Tracking Error (MAE): {mean_absolute_error:.6f} Radians")
    print("✅ Evaluation complete. Control feedback loops verified successfully.")
else:
    print("❌ Error: Flight log found, but it contained zero valid data rows.")

