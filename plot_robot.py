import os
import matplotlib.pyplot as plt

print("📊 Loading Telemetry Data Parser...")

filename = "robot_flight_log.csv"

# 1. Error check: Make sure the file exists before reading it
if not os.path.exists(filename):
    print(f"❌ Error: '{filename}' not found! Run your 'simulate_robot.py' first.")
    exit()

# 2. Initialize empty lists to store your numerical data tracks
time_stamps = []
targets = []
actuals = []

# 3. Open and read the file line-by-line
with open(filename, "r", encoding="utf-8") as file:
    lines = file.readlines()
    
    # LOOP STEP: Skip line 0 (the headers: "Time,Target_Angle...") and parse the rest
    for line in lines[1:]:
        if line.strip(): # Skip any blank rows if they exist
            # Split the line by commas into a list of strings: ["Time", "Target", "Actual"]
            parts = line.split(",") 
            
            # CRUCIAL STEP: Convert the strings to floats and append them to your tracking lists
            time_stamps.append(float(parts[0]))
            targets.append(float(parts[1]))
            actuals.append(float(parts[2]))

print(f"📥 Successfully parsed {len(time_stamps)} rows of physical telemetry logs!")

# --- YOUR MATPLOTLIB PLOTTING CODE GOES RIGHT HERE ---
plt.figure(figsize=(10, 6)) # Creates a wide canvas sheet (10 inches wide, 6 inches high)
# Line 1: Draw the dynamic Target path as a blue dashed line
plt.plot(time_stamps, targets, label="Target Reference Path", color="blue", linestyle="--")

# Line 2: Draw the Actual physical arm path as a solid red line
plt.plot(time_stamps, actuals, label="Actual Robotic Joint Angle", color="red", linewidth=2)
plt.title("Robotic Trajectory PID Tracking Profile", fontsize=14, fontweight="bold")
plt.xlabel("Simulation Clock Timestamp (Seconds)", fontsize=11)
plt.ylabel("Joint Angle Position (Radians)", fontsize=11)
plt.grid(True, linestyle=":", alpha=0.6) # Adds a clean dotted grid background
plt.legend()                             # Displays the box explaining your color labels

plt.savefig("robot_performance.png", dpi=300) # Compiles and saves the plot as a crisp image
plt.close()                                   # Frees up your laptop's memory
