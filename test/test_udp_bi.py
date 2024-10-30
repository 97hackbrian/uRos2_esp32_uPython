# pc_main.py

import socket
import json
import time
from threading import Thread

ESP32_IP = "192.168.0.12"  # Cambia a la IP de tu ESP32
ESP32_PORT = 59008
PC_PORT = 2020

# Crear el socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PC_PORT))  # La PC escucha en un puerto local

def send_cmd_vel(linear_x, linear_y, linear_z, angular_x, angular_y, angular_z):
    # Formato del mensaje Twist
    cmd_vel_msg = {
        "cmd_vel": {
            "linear": {"x": linear_x, "y": linear_y, "z": linear_z},
            "angular": {"x": angular_x, "y": angular_y, "z": angular_z}
        }
    }
    # Enviar mensaje a ESP32
    sock.sendto(json.dumps(cmd_vel_msg).encode(), (ESP32_IP, ESP32_PORT))
    print(f"Comando cmd_vel enviado: {cmd_vel_msg}")

def receive_joint_state():
    print("Escuchando mensajes de jointState desde el ESP32...")
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # Recibir datos desde el ESP32
            joint_state_msg = json.loads(data.decode())
            if "jointState" in joint_state_msg:
                print("Datos de encoders recibidos:")
                print("Posiciones:", joint_state_msg["jointState"]["position"])
                print("Velocidades:", joint_state_msg["jointState"]["velocity"])
                print("Esfuerzos:", joint_state_msg["jointState"]["effort"])
        except json.JSONDecodeError:
            print("Error al decodificar el mensaje")

def main():
    # Iniciar el hilo para escuchar los datos de jointState
    receiver_thread = Thread(target=receive_joint_state, daemon=True)
    receiver_thread.start()

    while True:
        # Envía comandos de velocidad cada segundo (puedes ajustar las velocidades según tus pruebas)
        send_cmd_vel(0.5, 0, 0, 0, 0, 0.1)  # Ejemplo de movimiento hacia adelante con rotación
        time.sleep(1)  # Intervalo entre envíos

if __name__ == "__main__":
    main()
