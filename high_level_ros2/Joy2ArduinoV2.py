import rclpy                        # include <rclpy.h>
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial

class JoystickToSerialNode(Node):   # struct+Function(OOP)
    def __init__(self):             # init()
        super().__init__('joystick_to_serial_node')
        
        # 1. Subscribe to the standard ROS 2 joy topic  
        self.subscription = self.create_subscription(   # function ptr/ interrupt setup
            Joy, '/joy', self.joy_callback, 10)
        """    
        # 2. Open the physical USB Serial Port to Arduino
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
            self.get_logger().info("Serial port opened successfully.")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            self.ser = None
        """    
    def joy_callback(self, msg):
        # [0] is horizontal, [1] is vertical 
        throttle = msg.axes[1]
        steering = msg.axes[0]
        
        # Differential Drive Math for Independent Mode
        left_speed = 90 + (throttle * 90) + (steering * 45)
        right_speed = 90 + (throttle * 90) - (steering * 45)
        
        # Constrain values to RC Servo range(0,180)
        left_speed = int(max(0, min(180, left_speed)))
        right_speed = int(max(0, min(180, right_speed)))
        
        # 3. Encode data input a packet string: "L,R\n"
        packet = f"{left_speed},{right_speed}\n"
        
        # 4. Send the packet over USB Serial
        print(f"[PACKET TO BE SENT]: {packet.strip()}")
        """
        if self.ser and self.ser.is_open:
            self.ser.write(packet.encode('utf-8'))
            self.get_logger().info(f"Sent Packet: {packet.strip()}")
        """    
def main(args=None):
    rclpy.init(args=args)           # Init ROS2 middleware layer
    node = JoystickToSerialNode()   # Instantiate the struct/class obj
    rclpy.spin(node)                # while(1)
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
