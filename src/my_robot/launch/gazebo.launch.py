from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    urdf_file = os.path.join(
        get_package_share_directory("my_robot"),
        "urdf",
        "my_robot.urdf"
    )

    robot_description = open(urdf_file).read()

    return LaunchDescription([

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[
                {"robot_description": robot_description}
            ],
            output="screen"
        ),
        ExecuteProcess(
            cmd=[
                "ign",
                "gazebo",
                "-r",
                "/usr/share/ignition/ignition-gazebo6/worlds/empty.sdf"
            ],
            output="screen"
        ),

        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=[
                "-name", "my_robot",
                "-topic", "robot_description",
                "-z", "1.0"
            ],
            output="screen"
        ),
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist"
            ],
            output="screen"
        )
    ])
