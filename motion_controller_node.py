import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist  # Standard spatial velocity message schema [1.1]
import math

class MotionControllerNode(Node):
    def __init__(self):
        super().__init__('motion_controller_node')
        
        # Instantiate a formal publisher targeting the standardized movement topic
        # parameters: (MessageType, TopicName, QueueSizeBuffer)
        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Set up a high-frequency asynchronous control timer running at 50Hz (every 0.02s)
        self.control_timer = self.create_timer(0.02, self.generate_motion_commands)
        
        self.sim_time = 0.0
        self.get_logger().info("🤖 ROS 2 Motion Control Command Node Active! Broadcasting over /cmd_vel...")

    def generate_motion_commands(self):
        # Create a blank instance container of our standard spatial velocity message template
        twist_cmd = Twist()
        
        # Advance our simulated system runtime tracking variable
        self.sim_time += 0.02
        
        # Plan a continuous, safe movement trajectory profile using wave math
        twist_cmd.linear.x = 0.5 * abs(math.sin(self.sim_time))  # Forward speed: 0.0 to 0.5 m/s
        twist_cmd.angular.z = 0.8 * math.cos(self.sim_time)      # Turn rate: Sweeping left/right yaw
        
        # Explicitly zero out unused dimensions to keep hardware registers clean
        twist_cmd.linear.y = 0.0
        twist_cmd.linear.z = 0.0
        twist_cmd.angular.x = 0.0
        twist_cmd.angular.y = 0.0
        
        # Broadcast the spatial movement array over the network socket instantly
        self.cmd_publisher.publish(twist_cmd)
        
        # Print a diagnostic log entry update every 2 seconds
        if int(self.sim_time * 100) % 100 == 0:
            self.get_logger().info(f"📊 Transmitting -> Linear: {twist_cmd.linear.x:.2f} m/s | Angular Z: {twist_cmd.angular.z:.2f} rad/s")

def main(args=None):
    rclpy.init(args=args)
    node = MotionControllerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
