import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from patrol_interfaces.msg import PatrolStatus

class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        
        # Subscriber รับค่าเลเซอร์จาก Gazebo
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
            
        # Publisher ส่งสถานะไปให้ Controller
        self.publisher = self.create_publisher(
            PatrolStatus,
            '/patrol_status',
            10)

    def scan_callback(self, msg):
        # ดึงค่าระยะทางเฉพาะมุมด้านหน้า (เฉียงซ้าย 30 องศา และ เฉียงขวา 30 องศา)
        front_ranges = msg.ranges[0:30] + msg.ranges[330:359]
        
        # กรองค่าที่เป็น 0.0 หรือ inf (ค่า error/ระยะอนันต์ของเซนเซอร์) ออก
        valid_ranges = [r for r in front_ranges if r > 0.0 and r < float('inf')]
        
        # หาระยะที่ใกล้ที่สุดด้านหน้า
        if len(valid_ranges) > 0:
            min_dist = min(valid_ranges)
        else:
            min_dist = 999.0 # ถ้ามองไม่เห็นอะไรเลย ให้ถือว่าโล่งมาก
            
        # เตรียมส่ง Message
        status_msg = PatrolStatus()
        status_msg.min_dist = float(min_dist)
        
        # เช็คระยะปลอดภัย ถ้าน้อยกว่า 0.4 เมตร คือใกล้ชนแล้ว
        if min_dist < 0.4:
            status_msg.mode = "OBSTACLE_NEAR"
        else:
            status_msg.mode = "OK"
            
        # ส่ง (Publish) ข้อมูลออกไป
        self.publisher.publish(status_msg)
        
        # ปริ้นต์บอกใน Terminal
        self.get_logger().info(f'Status: {status_msg.mode}, Front Distance: {min_dist:.2f} m')


def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
