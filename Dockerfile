# Use an official ROS 2 image as the base. 
# Desktop version includes development tools we will need.
FROM ros:humble-ros-base

# Set env variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set Cyclone DDS as the default middleware to ensure reliable local topic communication
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Update the container's package manager and install SLAM and sensor dependencies
# Added serial tools to accommodate the RPLIDAR A1 UART interface spec
# Added rplidar-ros, rviz2, and cyclonedds based on recent testing
RUN apt-get update && apt-get install -y \
    ros-humble-slam-toolbox \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-rplidar-ros \
    ros-humble-rviz2 \
    ros-humble-rmw-cyclonedds-cpp \
    python3-pip \
    python3-serial \
    minicom \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory inside the container
WORKDIR /workspace

# Set up the ROS 2 environment entrypoint so commands work automatically
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Default command when the container starts
CMD ["bash"]