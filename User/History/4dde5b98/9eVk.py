#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

# Create a Publisher object. queue_size=1 means that messages that are
# published but not handled by received are lost beyond queue size.
example_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
# Initialize this program as a node
rospy.init_node('forwards_backwards')

now = rospy.Time.now()
change_direction_time = rospy.Time.now() + rospy.Duration(5)

if not rospy.is_shutdown():
    twist = Twist()
    twist.linear.x = 0.2
    example_pub.publish(twist)
    twist.linear.x = 0.0
    example_pub.publish(twist)
    twist.linear.x = -0.2
    example_pub.publish(twist)