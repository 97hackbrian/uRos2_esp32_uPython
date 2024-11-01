import socket
import json
import time
from threading import Thread

# Definiciones de configuración
ESP32_IP = "192.168.0.12"  # Cambia a la IP de tu ESP32
ESP32_PORT_SEND = 2022      # Puerto donde la ESP32 envía datos
PC_PORT = 2021               # Puerto fijo para la PC

# Crear el socket UDP para enviar y recibir
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive.bind(("", PC_PORT))  # La PC escucha en el puerto fijo

# Función para obtener la IP local de la PC
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conectar a un servidor externo para determinar la IP de la interfaz activa
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"  # Fallback en caso de error
    finally:
        s.close()
    return local_ip

# Obtener IP local
pc_ip = get_local_ip()
print(f"PC escuchando en IP: {pc_ip}, Puerto: {PC_PORT}")

def send_cmd_vel(linear_x, linear_y, linear_z, angular_x, angular_y, angular_z):
    # Formato del mensaje Twist
    cmd_vel_msg = {
        "cmd_vel": {
            "linear": {"x": linear_x, "y": linear_y, "z": linear_z},
            "angular": {"x": angular_x, "y": angular_y, "z": angular_z}
        }
    }
    # Enviar mensaje a ESP32
    sock_send.sendto(json.dumps(cmd_vel_msg).encode(), (ESP32_IP, ESP32_PORT_SEND))
    print(f"Comando cmd_vel enviado: {cmd_vel_msg}")

def receive_joint_state():
    print("Escuchando mensajes de jointState desde el ESP32...")
    while True:
        try:
            data, addr = sock_receive.recvfrom(1024)  # Recibir datos desde el ESP32
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
        # Envía comandos de velocidad cada segundo (ajusta las velocidades según tus pruebas)
        send_cmd_vel(0.5, 0, 0, 0, 0, 0.1)  # Ejemplo de movimiento hacia adelante con rotación
        time.sleep(0.01)  # Intervalo entre envíos

if __name__ == "__main__":
    main()
