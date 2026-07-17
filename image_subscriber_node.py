import sys
import os

# 🛠️ HARDWARE ENVIRONMENT OVERRIDE FENCE
# Force Python to read our isolated package registry directory directly before checking global system paths
venv_site_packages = os.path.expanduser("~/ml_robotics/venv/lib/python3.12/site-packages")
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

# Your normal imports follow below cleanly
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge     
from ultralytics import YOLO
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image # Standard ROS 2 image sensor matrix schema layout [1.1]
from cv_bridge import CvBridge     # Specialized serialization bridge tracking module [1.1]
from ultralytics import YOLO
import time
import os

class ImageSubscriberNode(Node):
    def __init__(self):
        super().__init__('image_subscriber_node')
        
        # Initialize our serialization bridge layer [1.1]
        self.bridge = CvBridge()
        
        # Load our core lightweight object detection model architecture [1.1]
        model_path = os.path.expanduser("~/ml_robotics/models/yolov8n.pt")
        self.vision_model = YOLO(model_path)
        
        # Instantiate a formal subscriber tracking target topic channel
        # parameters: (MessageType, TopicName, CallbackFunction, QueueSizeBuffer)
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        
        self.get_logger().info("👁️ YOLOv8 ROS 2 Image Subscriber Perception Node Activated!")

    def image_callback(self, msg):
        start_time = time.perf_counter()
        
        try:
            # 🛠️ DESERIALIZATION BRIDGE: Unpack network message buffer straight into OpenCV pixel array [1.1]
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"❌ Serialization Failure: {str(e)}")
            return

        # Run our foundation object detection model live on the unpacked frame array matrix [1.1]
        vision_results = self.vision_model(cv_image, verbose=False)
        
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        
        # Parse tracking arrays for active targets inside the loop bounds
        object_count = 0
        for result in vision_results:
            object_count += len(result.boxes)
            
        self.get_logger().info(
            f"📥 Processed Frame Array | Latency: {latency_ms:.1f} ms | Detected Targets: {object_count}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = ImageSubscriberNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
