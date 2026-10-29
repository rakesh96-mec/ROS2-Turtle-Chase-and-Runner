# ROS 2 Turtle Chase and Runner

A university ROS 2 `turtlesim` project with two Python nodes: one moves a turtle in a circular path while another pursues it using pose feedback.

## What this project demonstrates

- ROS 2 Python nodes using `rclpy`
- Publishers and subscribers with `geometry_msgs/Twist` and `turtlesim/Pose`
- Timer-driven motion control
- Distance, target-angle, and heading-error calculations for a basic pursuit controller
- Counting completed loops by detecting when a turtle returns near its starting position

## Files

| File | Purpose |
|---|---|
| `turtle_runner.py` | Publishes constant linear and angular velocity commands to `/turtle1/cmd_vel` and counts returns near the initial position. |
| `catch_a_turtle.py` | Reads both turtle poses and commands `turtle2` to pursue `turtle1`, stopping when their distance is below 0.5 turtlesim units. |

## Requirements

- A working ROS 2 installation
- The `turtlesim` package for your ROS 2 distribution
- Python 3 in a terminal where the ROS 2 environment has been sourced

## How to run

Replace `<ros_distro>` with your installed ROS 2 distribution, such as `humble` or `jazzy`.

**Terminal 1 — start turtlesim:**

```bash
source /opt/ros/<ros_distro>/setup.bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 — spawn the second turtle:**

```bash
source /opt/ros/<ros_distro>/setup.bash
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'turtle2'}"
```

**Terminal 3 — run the circular runner:**

```bash
source /opt/ros/<ros_distro>/setup.bash
python3 turtle_runner.py
```

**Terminal 4 — run the chase controller:**

```bash
source /opt/ros/<ros_distro>/setup.bash
python3 catch_a_turtle.py
```

Run the Python commands from the directory containing the scripts. The two scripts are standalone ROS 2 nodes; this repository does not include a `colcon` package wrapper or installed console entry points.

## Control approach

The runner publishes fixed forward and angular velocities to produce circular motion in `turtlesim`. It counts completed loops by detecting when the turtle returns near its starting position.

The chaser calculates the relative position of the target, then computes the target heading and heading error. A simple proportional controller converts distance and heading error into linear and angular velocity commands. The chaser stops when the turtles are within 0.5 units.

## Scope

This is a learning exercise using the `turtlesim` simulator. The simple proportional controller is not validated for use on a physical robot.
