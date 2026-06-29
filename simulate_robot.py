import mujoco
import mujoco.viewer
import time

# 1. Define our 3D world with a fixed post, a mechanical hinge joint, and a motor
robot_xml = """
<mujoco>
    <option gravity="0 0 -9.81"/> <!-- Standard Earth Gravity -->
    
    <worldbody>
        <light directional="true" diffuse=".8 .8 .8" specular=".2 .2 .2" pos="0 0 5" dir="0 0 -1"/>
        <geom type="plane" size="5 5 0.1" rgba=".9 .9 .9 1"/>
        
        <!-- Fixed Gray Pillar Base -->
        <body name="base" pos="0 0 2">
            <geom type="cylinder" size="0.1 1" rgba="0.5 0.5 0.5 1"/>
            
            <!-- Upgraded Robotic Hinge Link Arm -->
            <body name="arm" pos="0 0 0">
                <joint name="hinge_joint" type="hinge" axis="0 1 0" pos="0 0 0"/> 
                <geom type="capsule" fromto="0 0 0  0.5 0 -1" size="0.08" rgba="0 0 1 1" mass="2"/> 
            </body>
        </body>
    </worldbody>

    <!-- MOTOR ACTUATOR LAYER: Connects an automated motor to the hinge joint -->
    <actuator>
        <motor joint="hinge_joint" ctrlrange="-100 100" ctrllimited="true"/>
    </actuator>
</mujoco>
"""

# 2. Compile the robotic actuator layout into CPU memory
model = mujoco.MjModel.from_xml_string(robot_xml)
data = mujoco.MjData(model)

# TARGET SETTING: We want the arm to stand straight out horizontally (90 degrees = 1.57 radians)
target_angle = 1.57  
Kp = 40.0 # Proportional Gain (How aggressively the motor fights back to correct mistakes)

print("🤖 Launching Closed-Loop P-Controller Window... Close window to exit.")

# 3. Launch the official native passive viewer engine
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()
        
        # 4. CLOSED-LOOP FEEDBACK CONTROL STEP
        current_angle = data.qpos[0]      # Read the current position sensor value [1.1]
        error = target_angle - current_angle # Calculate the error distance
        
        # Proportional Formula: Torque = Kp * Error
        control_torque = Kp * error
        
        # Inject the corrective torque directly into our motor actuator variable [1.1]
        data.ctrl[0] = control_torque
        
        mujoco.mj_step(model, data) # Process physics equations with smart motor torque
        viewer.sync()               # Refresh graphical interface layer
        
        # Maintain physical execution rate limit synchronization (500 FPS)
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)

print("👋 Simulation closed successfully.")
