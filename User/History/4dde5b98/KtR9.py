#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

# Create a Publisher object. queue_size=1 means that messages that are
# published but not handled by received are lost beyond queue size.
example_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
# Initialize this program as a node
rospy.init_node('forwards_backwards')

change_direction_time = rospy.Time.now() + rospy.Duration(5)

# rate object gets a sleep() method which will sleep 1/10 seconds
rate = rospy.Rate(10)
while not rospy.is_shutdown():
    print(light_change_time, rospy.Time.now(), light_change_time < rospy.Time.now())
    if driving_forward:
        print("green", green_light_twist.linear.x)
        example_pub.publish(green_light_twist)
    else:
        print("red")
        example_pub.publish(red_light_twist)

    if light_change_time < rospy.Time.now():
        print("flip")
        driving_forward = not driving_forward
        light_change_time = rospy.Time.now() + rospy.Duration(5)
    rate.sleep()