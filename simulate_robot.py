import mujoco
import mujoco.viewer
import time

# 1. Define our 3D world with the torque limitation boundaries REMOVED
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
    
    <!-- ACTUATOR LAYER FIX: CTRLLIMITED REMOVED so motor can draw enough torque to lift the mass -->
    <actuator>
        <motor joint="hinge_joint"/>
    </actuator>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(robot_xml)
data = mujoco.MjData(model)

# TARGET: Absolute horizontal hold (90 degrees = 1.57 radians)
target_angle = 1.57  

# PID GAINS UPGRADE: Increased values to aggressively snap and lock the arm straight out
Kp = 150.0  # Heavy muscle power
Ki = 80.0   # Aggressive steady-state error correction
Kd = 15.0   # Stronger shock absorber dampening to stop shaking

error_integral = 0.0
last_time = time.time()

print("🚀 Launching Unlocked PID Controller... Watch it lift straight to 90 degrees!")

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()
        
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        # Read current physical state parameters
        current_angle = data.qpos[0] if hasattr(data.qpos, '__len__') else data.qpos
        current_velocity = data.qvel[0] if hasattr(data.qvel, '__len__') else data.qvel
        
        # Calculate tracking error distance values
        error = target_angle - current_angle
        
        # Accumulate error memory step to pull out of the gravity sag
        if dt > 0:
            error_integral += error * dt
            
        # Core PID Loop Architecture Form
        control_torque = (Kp * error) + (Ki * error_integral) - (Kd * current_velocity)
        
        # Feed torque directly to unconstrained hardware layer arrays
        data.ctrl[0] = control_torque
        
        mujoco.mj_step(model, data)
        viewer.sync()               
        
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)
