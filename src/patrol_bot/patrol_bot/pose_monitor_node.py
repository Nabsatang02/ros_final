import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

class PoseMonitorNode(Node):
    def __init__(self):
        super().__init__('pose_monitor_node')
        
        # Subscribe รับค่าตำแหน่งจาก /odom
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
            
        # Publisher ส่งค่าตำแหน่งที่แปลงแล้วไปที่ /patrol_pose
        self.publisher = self.create_publisher(
            PoseStamped,
            '/patrol_pose',
            10)
            
        self.get_logger().info('Pose Monitor Node has been started.')

    def odom_callback(self, msg):
        # สร้าง Message ชนิด PoseStamped
        pose_msg = PoseStamped()
        
        # คัดลอกข้อมูล Header (รวมถึงเวลาและ frame_id) จาก /odom
        pose_msg.header = msg.header
        
        # คัดลอกข้อมูลตำแหน่ง (Position และ Orientation)
        pose_msg.pose = msg.pose.pose
        
        # ส่งข้อมูลออกไป
        self.publisher.publish(pose_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PoseMonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
