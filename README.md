Welcome to an innovative ROS 2 project that bridges the gap between an ESP32 embedded device and a dynamic mobile robotic system! This powerful node is designed to **seamlessly receive data via UDP** from the ESP32 and publish it as **JointState messages** within the ROS 2 framework. By facilitating efficient communication, we enable the capture of crucial encoder states and other important system parameters, empowering your robotic applications with real-time data.

But that's not all! Our node is also tuned to subscribe to the **cmd_vel topic**, allowing it to receive and interpret velocity commands for precise motor control. This means you can send commands to the ESP32 and achieve responsive, real-time control of your robot's movements—transforming your ideas into action!

## 🎯 Project Goals

- **Real-Time Data Reception**: Forge a robust communication link between the ESP32 and a ROS 2 node for continuous reception of encoder state data, ensuring your robot is always informed and ready to respond.
- **Efficient Publishing**: Transform the incoming data into standard **JointState messages**—the gold standard in ROS for articulating robot states—enabling their use in a variety of control and monitoring applications.
- **Dynamic Motor Control**: Tap into the **cmd_vel topic** to receive and interpret velocity commands, relaying them to the ESP32 to facilitate smooth and effective control of your robot's motors.
- **Leveraging UDP Protocol**: Harness the power of **UDP for data transmission**, providing low-latency communication that’s perfect for real-time applications—ensuring your robot reacts instantly to its environment.
"""

