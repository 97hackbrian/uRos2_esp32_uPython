# main.py

import network
from urclpy import Node
from ugeometry_msgs import Twist
from usensor_msgs import JointState
import gc
import time
from machine import Pin, PWM

# Variables globales para los contadores de los encoders
encoder_left_count = 0
encoder_right_count = 0

# Pines de los encoders
encA1 = Pin(2, Pin.IN)
encB1 = Pin(15, Pin.IN)
encA2 = Pin(4, Pin.IN)
encB2 = Pin(16, Pin.IN)

# Función de interrupción para actualizar el contador del encoder izquierdo
def update_left_encoder(pin):
    global encoder_left_count
    if encA1.value() == encB1.value():
        encoder_left_count += 1
    else:
        encoder_left_count -= 1

# Función de interrupción para actualizar el contador del encoder derecho
def update_right_encoder(pin):
    global encoder_right_count
    if encA2.value() == encB2.value():
        encoder_right_count += 1
    else:
        encoder_right_count -= 1

# Configuración de interrupciones para los encoders
encA1.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=update_left_encoder)
encA2.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=update_right_encoder)

# Función para conectarse a WiFi
def connect_to_wifi(ssid, password):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print("Conectando a la red WiFi...")
        wifi.connect(ssid, password)
        while not wifi.isconnected():
            time.sleep(1)
            print("Intentando conectar...")
    print("Conexión WiFi establecida:", wifi.ifconfig())

# Función para verificar y reconectar WiFi en caso de desconexión
def check_wifi_connection(ssid, password):
    wifi = network.WLAN(network.STA_IF)
    if not wifi.isconnected():
        print("Conexión WiFi perdida. Reintentando...")
        connect_to_wifi(ssid, password)

# Callback para procesar los mensajes recibidos en cmd_vel
def cmd_vel_callback(msg):
    print("Mensaje recibido en cmd_vel:")
    print(f"Linear - x: {msg.linear.x}, y: {msg.linear.y}, z: {msg.linear.z}")
    print(f"Angular - x: {msg.angular.x}, y: {msg.angular.y}, z: {msg.angular.z}")
    # Aquí podrías agregar la lógica para ajustar el movimiento del robot

def main():
    # Configuración WiFi
    ssid = "ROSNET1"  # Cambia a tu SSID
    password = "ROSNET2024"  # Cambia a tu contraseña
    connect_to_wifi(ssid, password)

    # Nodo, publicación y suscripción
    node = Node("esp32_node", "192.168.0.17", 2020)  # Cambia a la IP y puerto del servidor de ROS
    publisher = node.create_publisher(JointState, "jointState")
    subscriber = node.create_subscriber(Twist, "cmd_vel", cmd_vel_callback)

    encoder = JointState()
    encoder.name = ["base_link"]
    
    node.get_logger().info("Starting to publish Encoder messages")
    
    while True:
        try:
            # Revisa y reconecta WiFi si es necesario
            check_wifi_connection(ssid, password)
            
            # Actualiza los valores de posición en el mensaje de encoder
            encoder.position = [encoder_left_count, encoder_right_count, 0]
            encoder.velocity = [0, 0, 0]
            encoder.effort = [0, 0, 0]
            
            publisher.publish(encoder)
            gc.collect()
            time.sleep(0.01)
            
            # Escuchar mensajes de cmd_vel en el suscriptor
            subscriber.listen()  # Verifica y procesa los mensajes entrantes
        except OSError as e:
            node.get_logger().info(f"Error al enviar: {e}")
            time.sleep(1)  # Espera antes de volver a intentar

if __name__ == '__main__':
    main()
