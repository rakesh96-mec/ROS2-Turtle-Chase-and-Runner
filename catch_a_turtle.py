import rclpy
from rclpy.node import Node

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

import math


class CatchATurtle(Node):

    def __init__(self):
        super().__init__('catch_a_turtle')

        # publisher for turtle2
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle2/cmd_vel',
            10
        )

        # subscriber for turtle1 (target)
        self.turtle1_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.turtle1_callback,
            10
        )

        # subscriber for turtle2 (self)
        self.turtle2_sub = self.create_subscription(
            Pose,
            '/turtle2/pose',
            self.turtle2_callback,
            10
        )

        self.t1 = None
        self.t2 = None

        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info("Catch a Turtle Node Started")

    def turtle1_callback(self, msg):
        self.t1 = msg

    def turtle2_callback(self, msg):
        self.t2 = msg

    def control_loop(self):

        if self.t1 is None or self.t2 is None:
            return

        dx = self.t1.x - self.t2.x
        dy = self.t1.y - self.t2.y

        distance = math.sqrt(dx*dx + dy*dy)

        msg = Twist()

        # angle toward target
        target_angle = math.atan2(dy, dx)
        angle_error = target_angle - self.t2.theta

        # normalize angle
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        # stop condition (caught)
        if distance < 0.5:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)

            self.get_logger().info("🎯 Turtle1 caught!")
            return

        # proportional control
        msg.linear.x = 1.5 * distance
        msg.angular.z = 4.0 * angle_error

        self.publisher_.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = CatchATurtle()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()