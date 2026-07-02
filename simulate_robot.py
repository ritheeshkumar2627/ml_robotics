import mujoco
import mujoco.viewer
import time
import math
import csv
import os

robot_xml = """
<mujoco>
    <option gravity="0 0 -9.81"/> 
    <worldbody>
        <light directional="true" diffuse=".8 .8 .8" specular=".2 .2 .2" pos="0 0 5" dir="0 0 -1"/>
        <geom type="plane" size="5 5 0.1" rgba=".9 .9 .9 1"/>
        
        <body name="base" pos="0 0 2">
            <geom type="cylinder" size="0.1 1" rgba="0.5 0.5 0.5 1"/>
            <body name="arm" pos="0 0 0">
                <joint name="hinge_joint" type="hinge" axis="0 1 0" pos="0 0 0"/> 
                <geom type="capsule" fromto="0 0 0  0.5 0 -1" size="0.08" rgba="0 0 1 1" mass="2"/> 
            </body>
        </body>
    </worldbody>
    <actuator>
        <motor joint="hinge_joint"/>
    </actuator>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(robot_xml)
data = mujoco.MjData(model)

# HIGH-PERFORMANCE PID TUNING
Kp = 150.0  
Ki = 100.0  # Increased slightly to aggressively squash the tracking sag
Kd = 15.0   

error_integral = 0.0
# FIXED SCORING: Use MuJoCo's internal simulation clock tracker to initialize time
last_sim_time = data.time 

print("🚀 Launching Precision Trajectory PID Controller... Watch it wave flawlessly!")
# Create/Overwrite a clean text file with CSV headers BEFORE the loop fires up
filename = "robot_flight_log.csv"
with open(filename, "w", encoding="utf-8") as file:
    file.write("Time,Target_Angle,Actual_Angle\n")

print(f"📄 Telemetry stream initialized cleanly inside '{filename}'!")

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()
        
        # TIME FIX: Calculate precise delta intervals using MuJoCo's internal clock buffer
        current_sim_time = data.time
        dt = current_sim_time - last_sim_time
        last_sim_time = current_sim_time
        
        # 1. DYNAMIC TARGET TRACKING REFERENCE
        # Generates a smooth wavy trajectory over time centered at 90 degrees (1.57 rad)
        target_angle = 1.57 + 0.8 * math.cos(current_sim_time * 2.0)
        
        # 2. READ HARDWARE STATE ARRAYS
        current_angle = data.qpos if hasattr(data.qpos, '__len__') else data.qpos
        current_velocity = data.qvel if hasattr(data.qvel, '__len__') else data.qvel
        
        # 3. CORE CALCULATIONS
        error = target_angle - current_angle
        
        # Accumulate integral errors safely (dt is now guaranteed to match the physics steps!)
        if dt > 0:
            error_integral += error * dt
            
        # Complete PID Equation Formula
                
        control_torque = (Kp * error) + (Ki * error_integral) - (Kd * current_velocity)
        data.ctrl = control_torque
        
        # 🔍 NEW PRINT TRACKER: Prints the target vs actual angle in degrees
        # (Multiplying by 57.2958 converts raw radians into clean degrees)
        if int(current_sim_time * 100) % 20 == 0: # Limits prints so it doesn't flood your screen
            print(f"🎯 Target Angle: {target_angle * 57.2958:.1f}° | 🤖 Actual Angle: {current_angle[0] * 57.2958:.1f}° | ❌ Error: {error[0] * 57.2958:.1f}°")

        
        mujoco.mj_step(model, data)

        # TELEMETRY LOG STEP: Append the live sensor variables as text line entries
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{current_sim_time:.4f},{target_angle:.4f},{current_angle[0]:.4f}\n")

         



    

        viewer.sync()               
        
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)
