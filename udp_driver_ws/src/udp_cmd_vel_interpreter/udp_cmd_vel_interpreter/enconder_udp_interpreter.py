import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import socket
import json

class JointStateUDPReceiver(Node):
    def __init__(self):
        super().__init__('joint_state_udp_receiver')
        
        # Publicador para el tópico joint_states
        self.publisher = self.create_publisher(JointState, 'joint_states', 10)
        
        # Configuraciones UDP
        self.PC_PORT = 2021
        self.sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_receive.bind(("", self.PC_PORT))
        
        self.get_logger().info(f"Escuchando en puerto {self.PC_PORT} para joint states")

        # Iniciar hilo para recibir datos de joint state
        self.create_timer(0.01, self.receive_joint_state)

    def receive_joint_state(self):
        try:
            data, addr = self.sock_receive.recvfrom(1024)  # Recibir datos desde el ESP32
            joint_state_msg = json.loads(data.decode())
            if "jointState" in joint_state_msg:
                # Log de datos recibidos
                self.get_logger().info("Datos de encoders recibidos:")
                self.get_logger().info(f"Posiciones: {joint_state_msg['jointState']['position']}")
                self.get_logger().info(f"Velocidades: {joint_state_msg['jointState']['velocity']}")
                self.get_logger().info(f"Esfuerzos: {joint_state_msg['jointState']['effort']}")
                
                # Crear y publicar el mensaje JointState
                joint_state = JointState()
                joint_state.header.stamp = self.get_clock().now().to_msg()  # Agregar timestamp
                joint_state.name = ["joint1", "joint2", "joint3"]  # Cambia esto según tus joints
                
                # Convertir las posiciones, velocidades y esfuerzos a float
                joint_state.position = [float(pos) for pos in joint_state_msg['jointState']['position']]
                joint_state.velocity = [float(vel) for vel in joint_state_msg['jointState']['velocity']]
                joint_state.effort = [float(eff) for eff in joint_state_msg['jointState']['effort']]
                
                self.publisher.publish(joint_state)
                self.get_logger().info("Publicado joint state en el tópico 'joint_states'.")

        except json.JSONDecodeError:
            self.get_logger().error("Error al decodificar el mensaje")

def main(args=None):
    rclpy.init(args=args)
    joint_state_receiver = JointStateUDPReceiver()
    rclpy.spin(joint_state_receiver)

    # Destruir el nodo
    joint_state_receiver.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

