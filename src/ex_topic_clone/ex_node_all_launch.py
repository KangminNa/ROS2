import imp
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ex_topic',
            executable='ex_pub',
            name='pub0'
        ),
        Node(
            package='ex_topic',
            executable='ex_sub',
            name='sub0'
        ),
        Node(
            package='ex_topic_clone',
            executable='ex_pub',
            name='pub1'
        ),
        Node(
            package='ex_topic_clone',
            executable='ex_sub',
            name='sub1'
        ),
    ])