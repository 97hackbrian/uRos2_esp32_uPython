import network
from urclpy import Node
from ugeometry_msgs import Twist
from usensor_msgs import JointState
import gc
import time
from machine import Pin, PWM

# Variables globales de los encoders
encoder_left_count = 0
encoder_right_count = 0

# Pines de los encoders
encA1 = Pin(2, Pin.IN)
encB1 = Pin(15, Pin.IN)
encA2 = Pin(4, Pin.IN)
encB2 = Pin(16, Pin.IN)

# Funciones para actualizar contadores de encoders
def update_left_encoder(pin):
    global encoder_left_count
    if encA1.value() == encB1.value():
        encoder_left_count += 1
    else:
        encoder_left_count -= 1

def update_right_encoder(pin):
    global encoder_right_count
    if encA2.value() == encB2.value():
        encoder_right_count += 1
    else:
        encoder_right_count -= 1

# Configuración de interrupciones
encA1.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=update_left_encoder)
encA2.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=update_right_encoder)

# Funciones de WiFi
def connect_to_wifi(ssid, password):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print("Conectando a la red WiFi...")
        wifi.connect(ssid, password)
        while not wifi.isconnected():
            time.sleep(1)
            print("Intentando conectar...")
    print("Conexion WiFi establecida:", wifi.ifconfig())
    return wifi.ifconfig()  # Devuelve la configuración IP

def check_wifi_connection(ssid, password):
    wifi = network.WLAN(network.STA_IF)
    if not wifi.isconnected():
        print("Conexion WiFi perdida. Reintentando...")
        connect_to_wifi(ssid, password)

# Función de callback para cmd_vel
def cmd_vel_callback(msg):
    print("Mensaje recibido en cmd_vel:")
    print(f"Linear - x: {msg.linear.x}, y: {msg.linear.y}, z: {msg.linear.z}")
    print(f"Angular - x: {msg.angular.x}, y: {msg.angular.y}, z: {msg.angular.z}")

# Función principal
def main():
    ssid = "ROSNET1"  # SSID de la red
    password = "ROSNET2024"  # Contraseña de la red
    ip_info = connect_to_wifi(ssid, password)  # Conectar y obtener IP
    esp32_ip = ip_info[0]  # Obtener la IP del ESP32
    esp32_port = 2022  # Puerto que usará el ESP32

    # Imprimir la IP y el puerto del ESP32
    print(f"ESP32 escuchando en IP: {esp32_ip}, Puerto: {esp32_port}")

    # Aquí deberías usar la IP y puerto de la PC
    pc_ip = "192.168.0.17"  # Cambia a la IP de tu PC
    pc_port = 2021  # Puerto que usará la PC

    # Nodo, publicador y suscriptor
    node = Node("esp32_node", pc_ip, pc_port)  # Usar la IP de la PC
    publisher = node.create_publisher(JointState, "jointState")
    subscriber = node.create_subscriber(Twist, "cmd_vel", cmd_vel_callback,esp32_port,esp32_ip)

    encoder = JointState()
    encoder.name = ["base_link"]

    node.get_logger().info("Iniciando la publicación de mensajes de Encoder")

    # Dentro del bucle principal
    while True:
        try:
            check_wifi_connection(ssid, password)

            # Actualiza el estado del encoder
            encoder.position = [encoder_left_count, encoder_right_count, 0]
            encoder.velocity = [0, 0, 0]  # Puedes calcular la velocidad si es necesario
            encoder.effort = [0, 0, 0]

            # Imprimir los datos antes de publicar
            print("Datos del mensaje del encoder a enviar:")
            print("Posiciones:", encoder.position)
            print("Velocidades:", encoder.velocity)
            print("Esfuerzos:", encoder.effort)

            # Publica el mensaje de encoder
            publisher.publish(encoder)

            # Recolecta basura y espera antes de la siguiente iteración
            gc.collect()
            #time.sleep(0.01)

            # Escucha mensajes entrantes en el suscriptor
            subscriber.listen()
        except OSError as e:
            node.get_logger().info(f"Error al enviar: {e}")
            time.sleep(0.5)


if __name__ == '__main__':
    main()
