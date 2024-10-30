import socket

def get_local_ip():
    # Obtiene la dirección IP local
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))  # Conéctate a un servidor externo
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

def start_udp_server(host=None, port=2020):
    if host is None:
        host = get_local_ip()  # Obtiene la IP local si no se proporciona

    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    
    print(f'Servidor UDP escuchando en {host}:{port}')

    while True:
        # Recibir datos del cliente
        data, addr = sock.recvfrom(1024)  # Tamaño máximo de 1024 bytes
        print(f'Recibido {data} de {addr}')

if __name__ == '__main__':
    start_udp_server()
