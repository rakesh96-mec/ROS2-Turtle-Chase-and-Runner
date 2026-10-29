import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class MoveTurtle(Node):

    def __init__(self):
        super().__init__('move_turtle')

        # publisher
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # subscriber
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # timer
        self.timer = self.create_timer(
            0.1,
            self.move_callback
        )

        # tracking variables
        self.start_x = None
        self.start_y = None

        self.near_start = False
        self.circle_count = 0

    def move_callback(self):

        msg = Twist()

        # move in circle
        msg.linear.x = 2.0
        msg.angular.z = 1.0

        self.publisher_.publish(msg)

    def pose_callback(self, msg):

        # save initial position once
        if self.start_x is None:
            self.start_x = msg.x
            self.start_y = msg.y
            return

        near = (
            abs(msg.x - self.start_x) < 0.2 and
            abs(msg.y - self.start_y) < 0.2
        )

        if near and not self.near_start:

            self.circle_count += 1

            self.get_logger().info(
                f'Circles completed: {self.circle_count}'
            )

            self.near_start = True

        elif not near:
            self.near_start = False


def main(args=None):

    rclpy.init(args=args)

    node = MoveTurtle()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()