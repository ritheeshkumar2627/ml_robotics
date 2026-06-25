import mujoco
import mujoco.viewer
import time

# 1. Define a 3D world with explicit coordinate endpoints for the capsule
robot_xml = """
<mujoco>
    <option gravity="0 0 -9.81"/> 
    
    <worldbody>
        <light directional="true" diffuse=".8 .8 .8" specular=".2 .2 .2" pos="0 0 5" dir="0 0 -1"/>
        <geom type="plane" size="5 5 0.1" rgba=".9 .9 .9 1"/>
        
        <!-- Fixed Base Gray Column -->
        <body name="base" pos="0 0 2">
            <geom type="cylinder" size="0.1 1" rgba="0.5 0.5 0.5 1"/>
            
            <!-- Upgraded Robotic Hinge Link Arm -->
            <body name="arm" pos="0 0 0">
                <joint type="hinge" axis="0 1 0" pos="0 0 0"/> 
                <!-- FIX: Using fromto explicitly draws the blue capsule pointing downwards -->
                <geom type="capsule" fromto="0 0 0  0.5 0 -1" size="0.08" rgba="0 0 1 1" mass="2"/> 
            </body>
        </body>
    </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(robot_xml)
data = mujoco.MjData(model)

print("🤖 Launching Passive MuJoCo Window... Rotate camera view with your left-mouse click.")

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()
        mujoco.mj_step(model, data) 
        viewer.sync()               
        
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)

print("👋 Simulation closed successfully.")
