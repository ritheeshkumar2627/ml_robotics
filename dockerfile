FROM python:3.10-slim
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 libosmesa6 libglfw3 build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python libraries
RUN pip install --no-cache-dir torch torchvision ultralytics mujoco mujoco-python-viewer opencv-python

# 5. Copy BOTH files into your container workspace so they are both saved inside
COPY pytorch_core.py /workspace/pytorch_core.py
COPY simulate_robot.py /workspace/simulate_robot.py

# 6. Just choose ONE to run by default (Let's run the PyTorch one for today)
CMD ["python", "pytorch_core.py"]
