import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial

class JoystickToSerialNode(Node):
    def __init__(self):
        super().__init__('joystick_to_serial_node')
        
        self.subscription = self.create_subscription(
            Joy, '/joy', self.joy_callback, 10)
         
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
            self.get_logger().info("Serial port opened successfully.")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            self.ser = None
          
        self.latest_throttle = 0.0
        self.latest_steering = 0.0

        **# Track the CURRENT physical speed of the motors to handle ramping**
        **self.current_left = 90**
        **self.current_right = 90**

        **# Safety Rate: Send data exactly once per second (1.0 second interval)**
        **self.timer = self.create_timer(.2, self.send_serial_packet)**

    def joy_callback(self, msg):
        self.latest_steering = msg.axes[0]
        self.latest_throttle = msg.axes[1]

    def send_serial_packet(self):
        throttle = self.latest_throttle
        steering = self.latest_steering
        
        # Calculate what the joystick WANTS the speed to be (Target Speed)
        target_left = 90 + (throttle * 90) + (steering * 45)
        target_right = 90 - (throttle * 90) - (steering * 45)
        
        target_left = int(max(1, min(180, target_left)))
        target_right = int(max(1, min(180, target_right)))
        
        **# ACCELERATION RAMP: Only allow the speed to change by a maximum step of 25 units per second**
        **MAX_STEP = 25**
        
        **# Ramp Left Motor**
        **if target_left > self.current_left:**
            **self.current_left = min(self.current_left + MAX_STEP, target_left)**
        **elif target_left < self.current_left:**
            **self.current_left = max(self.current_left - MAX_STEP, target_left)**
            
        **# Ramp Right Motor**
        **if target_right > self.current_right:**
            **self.current_right = min(self.current_right + MAX_STEP, target_right)**
        **elif target_right < self.current_right:**
            **self.current_right = max(self.current_right - MAX_STEP, target_right)**

        **# Encode the safely ramped current speeds into the packet**
        **packet = f"{self.current_left},{self.current_right}\n"**
        
        print(f"[PACKET TO BE SENT]: {packet.strip()}")
       
        if self.ser and self.ser.is_open:
            self.ser.write(packet.encode('utf-8'))
            self.get_logger().info(f"Sent Packet: {packet.strip()}")
        
def main(args=None):
    rclpy.init(args=args)
    node = JoystickToSerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()