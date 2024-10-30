#usensor_msgs.py

class JointState:
    """
    Representa el estado de las juntas de un robot, incluyendo posición, velocidad y esfuerzo.
    """
    def __init__(self):
        self.name = []        # Lista de nombres de las juntas
        self.position = []    # Lista de posiciones (por lo general en radianes)
        self.velocity = []    # Lista de velocidades (por lo general en rad/s)
        self.effort = []      # Lista de esfuerzos o torques aplicados

    def __str__(self):
        return f"JointState(name={self.name}, position={self.position}, velocity={self.velocity}, effort={self.effort})"


class Imu:
    """
    Representa datos de un sensor IMU, incluyendo orientación, velocidad angular y aceleración lineal.
    """
    def __init__(self):
        self.orientation = Quaternion()         # Orientación como un cuaternión
        self.angular_velocity = Vector3()       # Velocidad angular (rad/s)
        self.linear_acceleration = Vector3()    # Aceleración lineal (m/s^2)

    def __str__(self):
        return (f"Imu(orientation={self.orientation}, angular_velocity={self.angular_velocity}, /n linear_acceleration={self.linear_acceleration})")


class Quaternion:
    """
    Representa un cuaternión para describir orientación en el espacio 3D.
    """
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.w = 1.0  # Valor inicial para representar una orientación nula

    def __str__(self):
        return f"Quaternion(x={self.x}, y={self.y}, z={self.z}, w={self.w})"


class Vector3:
    """
    Representa un vector 3D, utilizado para velocidad y aceleración.
    """
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def __str__(self):
        return f"Vector3(x={self.x}, y={self.y}, z={self.z})"
