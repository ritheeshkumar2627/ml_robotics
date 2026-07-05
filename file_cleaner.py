import os
junk_files=["vision_profile.txt","robot_flight_log.csv","vision_summary.txt","robot_performance.png"]

for filename in junk_files:
    if os.path.exists(filename):
        os.remove(filename)
        print(f'{filename} is deleted')