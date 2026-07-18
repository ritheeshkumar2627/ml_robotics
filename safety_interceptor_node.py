import sys
import os

# 🛠️ HARDWARE ENVIRONMENT OVERRIDE FENCE
# Force Python to read our isolated package registry directory directly before checking global system paths
venv_site_packages = os.path.expanduser("~/ml_robotics/venv/lib/python3.12/site-packages")
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge     
from ultralytics import YOLO
import time
from geometry_msgs.msg import Twist  # Standard spatial velocity message schema [1.1]

class SafetyInterceptorNode(Node):
    def __init__(self):
        super().__init__('safety_interceptor_node')

        # Initialize our serialization bridge layer [1.1]
        self.bridge = CvBridge()
        
        # Load our core lightweight object detection model architecture [1.1]
        model_path = os.path.expanduser("~/ml_robotics/models/yolov8n.pt")
        self.vision_model = YOLO(model_path)
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.process_and_evaluate,
            10
        )
        self.velocity_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        #define spatial parameters hazard
        self.CRITICAL_AREA_THRESHOLD=8000.0
        self.get_logger().info("closed loop interceptor node online and guarding")

    def process_and_evaluate(self,msg):
        try:
            cv_image=self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'serializationfailure :{str(e)}')
            return

        vision_results=self.vision_model(cv_image,verbose=False)
        hazard_detected=False

        for result in vision_results:
            for box in result.boxes:
                coords = box.xyxy[0].tolist()
                x1,y1,x2,y2=coords[0],coords[1],coords[2],coords[3]
                box_area=(x2-x1)*(y2-y1)
                if box_area>self.CRITICAL_AREA_THRESHOLD:
                    hazard_detection=True
                    break
        brake_cmd=Twist()
        if hazard_detected:
            brake_cmd.linear.x=0.0
            brake_cmd.angular.z=0.0
            self.velocity_publisher.publish(brake_cmd)
            self.get_logger().warn("collosion detected")
        else:
            brake_cmd.linear.x=0.2
            brake_cmd.angular.z=0.0
            self.velocity_publisher.publish(brake_cmd)
            self.get_logger().info("path is clear ")
def main(args=None):
    rclpy.init(args=args)
    node = SafetyInterceptorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

