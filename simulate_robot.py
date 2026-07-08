import mujoco
import mujoco.viewer
import time
import math

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

# INITIAL DIAGNOSTIC SETUP: Start Kp at absolute zero muscle strength
Kp = 0.0  
Ki = 50.0  
Kd = 5.0   

error_integral = 0.0
last_sim_time = data.time 

print("🚀 Launching Automated Diagnostic Gain Sweeper Loop...")

# Notice: key_callback parameter is completely removed here!
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()
        
        current_sim_time = data.time
        dt = current_sim_time - last_sim_time
        last_sim_time = current_sim_time
        
        # 1. AUTOMATED RAMP STEP: Automatically add 0.1 muscle power on every pass up to 200
        Kp = min(200.0, Kp + 0.1)
        
        target_angle = 1.57 + 0.8 * math.cos(current_sim_time * 2.0)
        
        current_angle = data.qpos[0] if hasattr(data.qpos, '__len__') else data.qpos
        current_velocity = data.qvel[0] if hasattr(data.qvel, '__len__') else data.qvel
        
        error = target_angle - current_angle
        if dt > 0:
            error_integral += error * dt
            
        # Core PID Loop pulling the smoothly sweeping Kp parameter
        control_torque = (Kp * error) + (Ki * error_integral) - (Kd * current_velocity)
        data.ctrl = control_torque
        
        # LIVE DIAGNOSTIC MONITOR
        if int(current_sim_time * 100) % 20 == 0:
            print(f"📈 Sweeping Gains -> Kp: {Kp:.1f} | 🤖 Actual Angle: {current_angle * 57.3:.1f}°")
            
        mujoco.mj_step(model, data)
        viewer.sync()               
        
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)
