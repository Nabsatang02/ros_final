import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_patrol_bot = get_package_share_directory('custom_map')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')

    world_file = os.path.join(pkg_patrol_bot, 'worlds', 'custom_map.world')
    tb3_model_path = os.path.join(pkg_tb3_gazebo, 'models', 'turtlebot3_burger', 'model.sdf')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
            launch_arguments={'world': world_file}.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_tb3_gazebo, 'launch', 'robot_state_publisher.launch.py')),
            launch_arguments={'use_sim_time': 'true'}.items(),
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'burger', '-file', tb3_model_path, '-x', '0.0', '-y', '0.0', '-z', '0.05'],
            output='screen'
        )
    ])