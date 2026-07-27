# UTARI Mobile Mapping Rover Workspace (`MavSentry`)

Welcome to the core software repository for our automated indoor mapping rover. This workspace handles everything from capturing 2D LiDAR data scans to translating controller inputs into physical wheel movements.

To keep our development environment identical across everyone's laptops (Windows/Linux) and our target hardware (NVIDIA Jetson), we use **Docker**. Think of Docker as a self-contained, pre-loaded virtual toolbox that comes with all our robotics libraries, drivers, and frameworks pre-installed.

---

## File Directory Layout

To keep things organized, our project is divided into strict folders. Avoid deeply nesting files; keep them exactly where they belong based on what they do:

```text
MavSentry/                  <- Root folder on your computer
├── Dockerfile               <- The blueprint recipe Docker uses to build our toolbox
├── README.md                <- This instruction document
│
├── high_level_ros2/         <- HIGH-LEVEL SOFTWARE WORKSPACE (ROS 2 Humble)
│
└── low_level_firmware/      <- HARDWARE FIRMWARE WORKSPACE (Microcontroller / Arduino)

```

### Where to add new files:

* **High-Level Code:** Put processing data, algorithm logic, SLAM mapping, and gamepad input nodes inside `high_level_ros2/`.
* **Microcontroller Code:** Put pin assignments, motor drivers, wheel encoder hardware interrupts, and serial output code inside `low_level_firmware/`.

---

## Docker Setup

Run the container using host networking and privilege flags so ROS 2 nodes can communicate properly and access USB devices (like the RPLIDAR A1):

```bash
sudo docker run -it --net=host --privileged -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd):/workspace my_rover_image:latest

```

---

## Running LiDAR, SLAM & RViz2

> **Important Environment Variable:** We use **Cyclone DDS** (`rmw_cyclonedds_cpp`) to avoid local inter-process communication issues inside the Jetson/Docker setup.

### 1. Launch the LiDAR Node

Open Terminal 1 inside the running container:

```bash
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
chmod 666 /dev/ttyUSB0
ros2 launch rplidar_ros rplidar_a1_launch.py serial_port:=/dev/ttyUSB0

```

### 2. Launch SLAM Toolbox (For Persistent 2D Mapping)

Open Terminal 2 (attach to container) to begin building an active occupancy grid:

```bash
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 0 --yaw 0 --pitch 0 --roll 0 --frame-id base_link --child-frame-id laser

```

### 3. Odometry to Robot Transform (Handheld Testing)

Provides "fake" zero-movement odometry to satisfy SLAM requirements before wheel encoders are integrated. Keep this running.

```bash
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 0 --yaw 0 --pitch 0 --roll 0 --frame-id odom --child-frame-id base_link
```

### 4. Launch SLAM Engine (Dynamic Mapping)

Generates the 2D occupancy grid. We run the node directly with lowered travel thresholds (0.1) so the map updates dynamically even with small handheld movements.

```bash
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ros2 run slam_toolbox async_slam_toolbox_node --ros-args -p odom_frame:=odom -p base_frame:=base_link -p map_frame:=map -p scan_topic:=/scan -p minimum_travel_distance:=0.1 -p minimum_travel_heading:=0.1

```

### 5. Launch RViz2 (Visualization)

Run this on a seperate Terminal (no container) before the container command

```bash
xhost +local:root

```
Opens the graphical interface to view the live scans and map.

```bash
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
rviz2

```

### 4. RViz2 Display Settings Configuration

Inside RViz2, make sure to configure the panel settings:

1. **Global Options $\rightarrow$ Fixed Frame:** Set to `map` (if running SLAM) or `laser` (for raw point cloud scan viewing).
2. **Add Display $\rightarrow$ LaserScan:**
* Topic: `/scan`
* **QoS Policy $\rightarrow$ Reliability:** Set to **Best Effort/Reliable** (matches the driver stream).


3. **Add Display $\rightarrow$ Map:**
* Topic: `/map` (rendered by `slam_toolbox`).