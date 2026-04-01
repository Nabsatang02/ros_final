# ROS2 Workspace: ros_final

This repository contains our ROS2 packages and the TurtleBot3 simulation as a submodule.

## Clone the repository

To clone the repository along with the submodules:

```bash
git clone --recursive https://github.com/Nabsatang02/ros_final.git
```

---

### To Build

  ```bash
  colcon build
  ```

---

### Terminal 1 — Launch Gazebo Simulation

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
````

### Terminal 2 — Pose Monitor Node

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run patrol_bot pose_monitor_node
```

### Terminal 3 — Controller Node

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run patrol_bot controller_node
```

### Terminal 4 — Sensor Node

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run patrol_bot sensor_node
```