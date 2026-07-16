import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32 # Pull standard 32-bit floating point messages

# Inherit from the formal ROS 2 Base Node Class layout container
class JointPublisherNode(Node):
    def __init__(self):
        # Initialize the base node structure with our package identifier string
        super().__init__('joint_state_publisher_node')
        
        # Instantiate a formal publisher topic tracking target
        # parameters: (MessageType, TopicName, QueueSizeBufferCeiling)
        self.publisher_ = self.create_publisher(Float32, '/joint_states', 10)
        
        # Configure an active, asynchronous high-frequency execution timer thread
        # 0.01 seconds = 100Hz loop execution rate boundary
        self.timer_ = self.create_timer(0.01, self.timer_callback)
        
        self.simulated_angle = 0.0
        self.get_logger().info("🚀 Asynchronous 100Hz Telemetry Publisher Node Active!")

    def timer_callback(self):
        # Create a blank instance tracking container of our message definition
        msg = Float32()
        
        # Simulate a moving joint position angle parameter using simple incremental steps
        self.simulated_angle += 0.01
        msg.data = self.simulated_angle
        
        # Broadcast the data binary layer over the network topic socket instantly
        self.publisher_.publish(msg)

def main(args=None):
    # Initialize the underlying execution context layers
    rclpy.init(args=args)
    
    # Spin the node container active in memory registers
    node = JointPublisherNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    # Shutdown context tracking boundaries cleanly on termination
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
