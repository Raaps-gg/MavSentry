# Use an official ROS 2 image as the base. 
# Desktop version includes development tools we will need.
FROM osrf/ros:humble-desktop

# Set env variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the container's package manager and install SLAM dependencies
# Added serial tools to accommodate the RPLIDAR A1 UART interface spec
RUN apt-get update && apt-get install -y \
    ros-humble-slam-toolbox \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
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
