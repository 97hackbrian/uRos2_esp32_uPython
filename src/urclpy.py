# urclpy.py

import usocket
import json
from usensor_msgs import JointState, Imu
from ugeometry_msgs import Twist

class Node:
    def __init__(self, node_name, ip, port):
        self.node_name = node_name
        self.udp_ip = ip
        self.udp_port = port
        self.sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    
    def create_publisher(self, msg_type, topic):
        return Publisher(self.sock, self.udp_ip, self.udp_port, topic)
    
    def create_subscriber(self, msg_type, topic, callback):
        return Subscriber(self.sock, topic, msg_type, callback)
    
    def get_logger(self):
        return Logger(self.node_name)


class Publisher:
    def __init__(self, sock, udp_ip, udp_port, topic):
        self.sock = sock
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.topic = topic

    def publish(self, msg):
        msg_str = self.format_msg(msg)
        self.sock.sendto(msg_str.encode(), (self.udp_ip, self.udp_port))

    def format_msg(self, msg):
        if isinstance(msg, Twist):
            msg_dict = {
                "linear": {
                    "x": msg.linear.x,
                    "y": msg.linear.y,
                    "z": msg.linear.z
                },
                "angular": {
                    "x": msg.angular.x,
                    "y": msg.angular.y,
                    "z": msg.angular.z
                }
            }
            return json.dumps({self.topic: msg_dict})
        elif isinstance(msg, JointState):
            msg_dict = {
                "name": msg.name,
                "position": msg.position,
                "velocity": msg.velocity,
                "effort": msg.effort
            }
            return json.dumps({self.topic: msg_dict})
        elif isinstance(msg, Imu):
            msg_dict = {
                "orientation": {
                    "x": msg.orientation.x,
                    "y": msg.orientation.y,
                    "z": msg.orientation.z,
                    "w": msg.orientation.w
                },
                "angular_velocity": {
                    "x": msg.angular_velocity.x,
                    "y": msg.angular_velocity.y,
                    "z": msg.angular_velocity.z
                },
                "linear_acceleration": {
                    "x": msg.linear_acceleration.x,
                    "y": msg.linear_acceleration.y,
                    "z": msg.linear_acceleration.z
                }
            }
            return json.dumps({self.topic: msg_dict})


class Subscriber:
    def __init__(self, sock, topic, msg_type, callback):
        self.sock = sock
        self.topic = topic
        self.msg_type = msg_type
        self.callback = callback

    def listen(self):
        while True:
            data, _ = self.sock.recvfrom(1024)
            try:
                msg = json.loads(data.decode())
                if self.topic in msg:
                    parsed_msg = self.parse_msg(msg[self.topic])
                    self.callback(parsed_msg)
            except json.JSONDecodeError:
                print("Error decoding message")

    def parse_msg(self, msg_dict):
        if self.msg_type == Twist:
            msg = Twist()
            msg.linear.x = msg_dict["linear"]["x"]
            msg.linear.y = msg_dict["linear"]["y"]
            msg.linear.z = msg_dict["linear"]["z"]
            msg.angular.x = msg_dict["angular"]["x"]
            msg.angular.y = msg_dict["angular"]["y"]
            msg.angular.z = msg_dict["angular"]["z"]
        elif self.msg_type == JointState:
            msg = JointState()
            msg.name = msg_dict["name"]
            msg.position = msg_dict["position"]
            msg.velocity = msg_dict["velocity"]
            msg.effort = msg_dict["effort"]
        elif self.msg_type == Imu:
            msg = Imu()
            msg.orientation.x = msg_dict["orientation"]["x"]
            msg.orientation.y = msg_dict["orientation"]["y"]
            msg.orientation.z = msg_dict["orientation"]["z"]
            msg.orientation.w = msg_dict["orientation"]["w"]
            msg.angular_velocity.x = msg_dict["angular_velocity"]["x"]
            msg.angular_velocity.y = msg_dict["angular_velocity"]["y"]
            msg.angular_velocity.z = msg_dict["angular_velocity"]["z"]
            msg.linear_acceleration.x = msg_dict["linear_acceleration"]["x"]
            msg.linear_acceleration.y = msg_dict["linear_acceleration"]["y"]
            msg.linear_acceleration.z = msg_dict["linear_acceleration"]["z"]
        return msg


class Logger:
    def __init__(self, node_name):
        self.node_name = node_name

    def info(self, message):
        print(f"[INFO] [{self.node_name}] {message}")
