import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial

class JoystickToSerialNode(Node):
def init(self):
super().init('joystick_to_serial_node')

self.subscription = self.create_subscription(
Joy, '/joy', self.joy_callback, 10)

try:
self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
self.get_logger().info("Serial port opened successfully.")
except Exception as e:
self.get_logger().error(f"Failed to open serial port: {e}")
self.ser = None

# Initialize variables to store the latest joystick inputs
self.latest_throttle = 0.0
self.latest_steering = 0.0

# Create a timer that runs 5 times a second (every 0.2 seconds)
self.timer = self.create_timer(0.2, self.send_serial_packet)

def joy_callback(self, msg):
# Only save the raw joystick values when they arrive
self.latest_steering = msg.axes[0]
self.latest_throttle = msg.axes[1]

def send_serial_packet(self):
# Perform the math and send the packet at a controlled 5 Hz rate
throttle = self.latest_throttle
steering = self.latest_steering

# Fixed a minor typo from the original code where right_speed used left_speed
left_speed = 90 + (throttle * 90) + (steering * 45)
right_speed = 90 + (throttle * 90) - (steering * 45)

left_speed = int(max(0, min(180, left_speed)))
right_speed = int(max(0, min(180, right_speed)))

packet = f"{left_speed},{right_speed}\n"

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

if name == 'main':
main()