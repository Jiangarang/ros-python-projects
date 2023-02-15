#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

# Create a Publisher object. queue_size=1 means that messages that are
# published but not handled by received are lost beyond queue size.
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
# Initialize this program as a node
rospy.init_node('forwards_backwards')

# Create 2 twist objects. Constructor sets all to zero firstr
# One that has 0 forward motion, called red_light_twist
# The other has forward motion, called green_light twist

red_light_twist = Twist()
green_light_twist = Twist()
red_light_twist.linear.x = -0.2
green_light_twist.linear.x = 0.2

# if driving_forward is true we use green_light_twist, otherwise red_light_twist
driving_forward = False

# light_change_time is future time when we want to change light
light_change_time = rospy.Time.now()
print (rospy.Time.now())

# rate object gets a sleep() method which will sleep 1/10 seconds
rate = rospy.Rate(10)

count = 0

if not rospy.is_shutdown():
    count += 1
    print(light_change_time, rospy.Time.now(), light_change_time < rospy.Time.now())
    if driving_forward:
        cmd_vel_pub.publish(green_light_twist)
    else:
        cmd_vel_pub.publish(red_light_twist)

    if light_change_time < rospy.Time.now():
        print("flip")
        driving_forward = not driving_forward
        light_change_time = rospy.Time.now() + rospy.Duration(5)
    rate.sleep()