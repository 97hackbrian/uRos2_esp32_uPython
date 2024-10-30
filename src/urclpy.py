# urclpy.py

import usocket

class Node:
    def __init__(self, node_name, ip, port):
        self.node_name = node_name
        self.udp_ip = ip
        self.udp_port = port
        self.sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)

    def create_publisher(self, msg_type, topic):
        return Publisher(self.sock, self.udp_ip, self.udp_port, topic)

    def get_logger(self):
        return Logger(self.node_name)

class Publisher:
    def __init__(self, sock, udp_ip, udp_port, topic):
        self.sock = sock
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.topic = topic

    def publish(self, msg):
        # Convierte el mensaje en un formato JSON o cadena
        msg_str = f"{self.topic}:{msg.data}"
        self.sock.sendto(msg_str.encode(), (self.udp_ip, self.udp_port))

class Logger:
    def __init__(self, node_name):
        self.node_name = node_name

    def info(self, message):
        print(f"[INFO] [{self.node_name}] {message}")
