#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
import xacro

def generate_launch_description():
    pkg_name = 'custom_map'

    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true', description='Use simulation (Gazebo) clock if true'
    )
    declare_x_pose = DeclareLaunchArgument(
        'x_pose', default_value='0.0', description='Initial X position of the robot'
    )
    declare_y_pose = DeclareLaunchArgument(
        'y_pose', default_value='0.0', description='Initial Y position of the robot'
    )

    # Paths
    world_path = os.path.join(
        get_package_share_directory(pkg_name),
        'worlds',
        'custom_map.world'
    )

    urdf_path = os.path.join(
        get_package_share_directory(pkg_name),
        'urdf',
        'turtlebot3_burger.urdf'
    )

    # Process URDF (xacro-safe)
    robot_desc = xacro.process_file(urdf_path).toxml()

    # Nodes
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': use_sim_time
        }]
    )

    spawn_robot_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'turtlebot3',
            '-file', urdf_path,
            '-x', x_pose,
            '-y', y_pose
        ],
        output='screen'
    )

    gzserver_node = ExecuteProcess(
        cmd=['gzserver', '--verbose', world_path, '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    gzclient_node = ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_x_pose,
        declare_y_pose,
        gzserver_node,
        gzclient_node,
        robot_state_publisher_node,
        spawn_robot_node
    ])