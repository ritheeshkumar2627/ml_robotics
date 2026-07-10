import mujoco
import mujoco.viewer
import time
import math
import os
import configparser

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

# INITIAL WORKBENCH SETUP: Give the robot solid operational baseline values
Kp = 150.0  
Ki = 50.0  
Kd = 15.0   # Normal smooth fluid dampening

error_integral = 0.0
last_sim_time = data.time 

print("🚀 Launching Reactive Control State Interceptor... Waiting for perception logs...")

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()
        
        current_sim_time = data.time
        dt = current_sim_time - last_sim_time
        last_sim_time = current_sim_time
        
        # 1. READ PERCEPTION INTERPROCESS BRIDGE DATA
        autopilot_status = "CLEAR" # Default safety baseline
        
        if os.path.exists("autopilot_signal.cfg"):
            try:
                with open("autopilot_signal.cfg", "r", encoding="utf-8") as f:
                    line = f.read().strip()
                    if "=" in line:
                        autopilot_status = line.split("=")[1]
            except Exception:
                pass # Prevent minor file read/write collision locks from crashing the loop

        # 2. STATE MACHINE INTERCEPTOR GATES
        if autopilot_status == "critical brake":
            target_angle = 0.0  # Force arm to safe neutral bracing point instantly
            Kd_active = 80.0    # Inject heavy hydraulic dampening brakes to freeze movement
            current_state = "🚨 EMERGENCY OVERRIDE INTERCEPT"
        else:
            # Execute normal, smooth wavy trajectory reference tracking operations
            target_angle = 1.57 + 0.8 * math.cos(current_sim_time * 2.0)
            Kd_active = 15.0    # Return back to smooth fluid shock absorption dampening
            current_state = "🟢 NORMAL AUTOPILOT TRACKING"

        # 3. CORE COUPLING CALCULATIONS
        current_angle = data.qpos[0] if hasattr(data.qpos, '__len__') else data.qpos
        current_velocity = data.qvel[0] if hasattr(data.qvel, '__len__') else data.qvel
        
        error = target_angle - current_angle
        if dt > 0:
            error_integral += error * dt
            
        # Run PID loop pulling the dynamic reactive brakes
        control_torque = (Kp * error) + (Ki * error_integral) - (Kd_active * current_velocity)
        data.ctrl = control_torque
        
        # MONITOR PERFORMANCE CHANNELS LIVE
        if int(current_sim_time * 100) % 20 == 0:
            print(f"🚦 Mode: {current_state} | Target: {target_angle:.2f} | Kd: {Kd_active:.1f}")
            
        mujoco.mj_step(model, data)
        viewer.sync()               
        
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)
