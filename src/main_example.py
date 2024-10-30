# main.py

from urclpy import Node
from ugeometry_msgs import Twist

def main():
    node = Node("esp32_node", "192.168.1.100", 8080)  # Cambia a la IP y puerto del servidor de ROS
    publisher = node.create_publisher(Twist, "cmd_vel")

    twist_msg = Twist()
    twist_msg.linear.x = 1.0
    twist_msg.angular.z = 0.5

    node.get_logger().info("Starting to publish Twist messages")
    while True:
        publisher.publish(twist_msg)


if __name__ == '__main__':
    main()