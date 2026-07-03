# UTARI Mobile Mapping Rover Workspace

Welcome to the core software repository for our automated indoor mapping rover. This workspace handles everything from capturing 2D LiDAR data scans to translating controller inputs into physical wheel movements.

To keep our development environment identical across everyone's laptops (Windows/Linux) and our target hardware, we use **Docker**. Think of Docker as a self-contained, pre-loaded virtual toolbox that comes with all our robotics libraries, drivers, and frameworks pre-installed. You don't have to install any messy robotics software directly on your computer—Docker handles it for you.

# File Directory Layout
To keep things organized, our project is divided into strict folders. Try not deeply nest your files; keep them exactly where they belong based on what they do:
MavSentry/                  <- Root folder on your computer
├── Dockerfile               <- The blueprint recipe Docker uses to build our toolbox
├── README.md                <- This instruction document
│
├── high_level_ros2/         <- HIGH-LEVEL SOFTWARE WORKSPACE
│
└── low_level_firmware/      <- HARDWARE FIRMWARE WORKSPACE

## Where to add new files:

    If you are writing high-level code (processing data, algorithm logic, mapping, reading gamepad inputs), put it inside high_level_ros2/.

    If you are writing microcontroller code (reading hardware pins, spinning motors, talking to the motor driver hardware), put it inside low_level_firmware/.

# Docker Setup
Before running the container for the first time, you need to download our pre-built image from Docker Hub. Open your Linux/WSL terminal, navigate into your project folder, and run these two commands:

# 1. Download the shared environment image from Docker Hub
docker pull raaps25/rover_slam:v1

# 2. Spin up the container environment using that image
docker run -it --name active_slam --net=host --privileged -v $(pwd):/workspace raaps25/rover_slam:v1

    docker pull: Downloads the complete, pre-configured workspace environment so you don't have to spend time compiling ROS 2 or SLAM dependencies on your machine.

    docker run: Launches the container. It links the folder on your laptop directly to the environment sandbox (-v), connects your computer's network interface so we can view maps remotely (--net=host), and opens up access to attached hardware like USB controllers and serial cables (--privileged).

If this doesnt work you can also just use the dockerfile to install your own container