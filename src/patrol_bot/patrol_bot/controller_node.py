import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from patrol_interfaces.msg import PatrolStatus

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')
        self.subscription = self.create_subscription(PatrolStatus, '/patrol_status', self.status_callback, 10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def status_callback(self, msg):
        cmd = Twist()
        if msg.mode == "OK":
            # ทางสะดวก เดินหน้า
            cmd.linear.x = 0.2
            cmd.angular.z = 0.0
        elif msg.mode == "OBSTACLE_NEAR":
            # เจอสิ่งกีดขวาง หยุดแล้วเลี้ยว
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
            
        self.publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
