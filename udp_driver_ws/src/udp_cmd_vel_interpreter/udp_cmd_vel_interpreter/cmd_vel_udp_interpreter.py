import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import json

class CmdVelUDPInterpreter(Node):
    def __init__(self):
        super().__init__('cmd_vel_udp_interpreter')
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.listener_callback, 10)

        # Configuraciones UDP
        self.ESP32_IP = "192.168.0.12"  # Cambia a la IP de tu ESP32
        self.ESP32_PORT_SEND = 2022      # Puerto donde la ESP32 recibe datos
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.get_logger().info("Suscrito al tópico cmd_vel y listo para enviar datos a la ESP32.")

    def listener_callback(self, msg):
        # Crear mensaje JSON a enviar por UDP
        cmd_vel_msg = {
            "cmd_vel": {
                "linear": {"x": msg.linear.x, "y": msg.linear.y, "z": msg.linear.z},
                "angular": {"x": msg.angular.x, "y": msg.angular.y, "z": msg.angular.z}
            }
        }
        # Enviar mensaje a ESP32
        self.sock_send.sendto(json.dumps(cmd_vel_msg).encode(), (self.ESP32_IP, self.ESP32_PORT_SEND))
        self.get_logger().info(f'Enviado a ESP32: {cmd_vel_msg}')

def main(args=None):
    rclpy.init(args=args)
    cmd_vel_udp_interpreter = CmdVelUDPInterpreter()
    rclpy.spin(cmd_vel_udp_interpreter)

    # Destruir el nodo
    cmd_vel_udp_interpreter.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

