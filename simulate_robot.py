import mujoco
import mujoco_viewer
import time

# 1. Define a 3D world with custom underwater gravity and two objects
world_xml = """
<mujoco>
    <option gravity="0 5 -2"/> <!-- Custom Gravity: [X=0, Y=5 forward, Z=-2 slow fall] -->
    
    <worldbody>
        <light directional="true" diffuse=".8 .8 .8" specular=".2 .2 .2" pos="0 0 5" dir="0 0 -1"/>
        <geom type="plane" size="10 10 0.1" rgba=".9 .9 .9 1"/>
        
        <!-- Object 1: Massive Red Falling Sphere -->
        <body name="ball" pos="0 -3 5">
            <joint type="free"/>
            <geom type="sphere" size="0.5" rgba="1 0 0 1" mass="1"/>
        </body>

        <!-- Object 2: Heavy Static Blue Box Target -->
        <body name="box" pos="0 0 0.5">
            <joint type="free"/>
            <geom type="box" size="0.6 0.6 0.6" rgba="0 0 1 1" mass="5"/>
        </body>
    </worldbody>
</mujoco>
"""

# 2. Compile the XML script into the MuJoCo physics model
model = mujoco.MjModel.from_xml_string(world_xml)
data = mujoco.MjData(model)

# 3. Open the interactive visual window
viewer = mujoco_viewer.MujocoViewer(model, data)

print("🚀 Launching Upgraded MuJoCo Physics World... Close window to exit.")

# 4. Continuous simulation playback loop
while viewer.is_alive:
    mujoco.mj_step(model, data)  # Run 2 milliseconds of real physics equations
    viewer.render()
    time.sleep(0.002)            # Match real-world speed execution

print("👋 Simulation closed successfully.")
