Breakdown of Terminals & Debugging Guide
Terminal 1: LiDAR Driver (rplidar_ros)

What it does:
Communicates directly with the physical sensor over USB serial (/dev/ttyUSB0), spins up the laser motor, reads raw distance measurements, and broadcasts them as ROS 2 sensor_msgs/msg/LaserScan messages on the /scan topic.

    What success looks like:
    You'll see log lines stating the device serial number, firmware version, and Succeed to start scan.

    How to Debug Terminal 1:

        Error: Failed to open serial port / Permission denied

            Fix: Run sudo chmod 666 /dev/ttyUSB0 or check if the LiDAR plugged into a different port using ls /dev/ttyUSB*.

        Error: RPLIDAR running on incorrect baudrate or device timeouts

            Fix: Unplug and replug the USB cable, or check if the Jetson's power supply is supplying enough current to power the LiDAR motor.

        Verify raw output: Open a new terminal tab and run:
        Bash

        ros2 topic echo /scan

        (If binary data streams across the screen, the LiDAR is working properly).

Terminal 2: SLAM Node (slam_toolbox)

What it does:
Acts as the mapping engine. It listens to the incoming /scan points from Terminal 1, performs scan-matching algorithms to build a 2D occupancy grid map over time, and publishes the resulting map onto the /map topic while constantly broadcasting the spatial transform (map → odom → laser).

    What success looks like:
    Log output showing Registering sensor: laser and periodic updates like Message Filter dropping message: frame 'laser' (normal during initialization) followed by active graph optimizations.

    How to Debug Terminal 2:

        Error: LaserPose transform not found / Map isn't building

            Fix: Check if slam_toolbox is listening to the right scan topic. Run:
            Bash

            ros2 topic info /scan

            Ensure there is 1 Publisher (rplidar) and 1 Subscription (slam_toolbox).

        Map jumps or becomes distorted:

            Fix: Because you don't have wheel odometry integrated yet, rapid movements will break scan-matching. Move the rover or handheld sensor very slowly.

        Verify map output: Run:
        Bash

        ros2 topic echo /map --once

        (If metadata like grid resolution and cell array data print out, SLAM is publishing correctly).

Terminal 3: Visualization (rviz2)

What it does:
Acts as the visual graphical interface (GUI). It does not generate or process map data itself—it simply subscribes to /scan and /map topics via DDS networking and renders them in 3D/2D space for human interaction.

    What success looks like:
    The RViz window opens without crash warnings, and subscribing to topics turns the display status indicators to OK (Green).

    How to Debug Terminal 3:

        Issue: "No transform from [laser] to [map]" or status warning in red

            Fix: slam_toolbox in Terminal 2 is either not running or hasn't received its first /scan message yet.

        Issue: /scan points aren't showing up, but topic exists

            Fix: Under LaserScan → QoS Policy, set Reliability to Best Effort instead of Reliable.

        Issue: Display won't launch or Could not connect to X server

            Fix: Ensure you launched Docker with -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix and ran xhost +local:root on your Linux host system before launching the container.

Quick Debugging Cheat Sheet
Command	Purpose
ros2 topic list	Lists all active topics (should see /scan, /map, /tf, /tf_static).
ros2 topic hz /scan	Checks the frequency of the LiDAR scan stream (~10 Hz is target).
ros2 run tf2_tools view_frames	Generates a PDF tree showing how map, odom, and laser frames link together.