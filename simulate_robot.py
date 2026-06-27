import mujoco
import mujoco.viewer
import time

# 1. Define a 3D world with a fixed column, a hinge arm, and an electronic motor
robot_xml = """
<mujoco>
    <option gravity="0 0 -9.81"/> <!-- Standard Earth Gravity -->
    
    <worldbody>
        <light directional="true" diffuse=".8 .8 .8" specular=".2 .2 .2" pos="0 0 5" dir="0 0 -1"/>
        <geom type="plane" size="5 5 0.1" rgba=".9 .9 .9 1"/>
        
        <!-- Fixed Base Gray Pillar -->
        <body name="base" pos="0 0 2">
            <geom type="cylinder" size="0.1 1" rgba="0.5 0.5 0.5 1"/>
            
            <!-- Upgraded Robotic Hinge Link Arm -->
            <body name="arm" pos="0 0 0">
                <joint name="hinge_joint" type="hinge" axis="0 1 0" pos="0 0 0"/> 
                <geom type="capsule" fromto="0 0 0  0.5 0 -1" size="0.08" rgba="0 0 1 1" mass="2"/> 
            </body>
        </body>
    </worldbody>

    <!-- MOTOR ACTUATOR LAYER: Adds an electronic motor to our hinge joint -->
    <actuator>
        <motor joint="hinge_joint" ctrlrange="-10 10" ctrllimited="true"/>
    </actuator>
</mujoco>
"""

# 2. Compile the robotic actuator layout into CPU memory
model = mujoco.MjModel.from_xml_string(robot_xml)
data = mujoco.MjData(model)

print("🤖 Launching Controlled MuJoCo Actuator Window... Close screen layout to exit.")

# 3. Launch the official native passive viewer engine
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()
        
        # 4. CONTROL STEP: Inject 3.5 Newton-meters of continuous torque into the motor
        # data.ctrl[0] targets the first actuator defined in your XML script
        data.ctrl[0] = 3.5
        
        mujoco.mj_step(model, data) # Run core physics formulas with active motor forces
        viewer.sync()               # Refresh graphical interface layer
        
        # Maintain physical execution rate limit synchronization (500 FPS)
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)

print("👋 Simulation closed successfully.")
