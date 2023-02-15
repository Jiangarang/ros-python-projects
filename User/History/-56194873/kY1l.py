#!/usr/bin/env python

import rospy
import sys
import math
import tf
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

backward = Twist()
forward = Twist()
stop = Twist()
backward.linear.x = -0.2
forward.linear.x = 0.2

# if driving_forward is true we publish forward, otherwise backward
driving_forward = False

# change_direction_time is future time when we want to change cirection
change_direction_time = rospy.Time.now()
print (rospy.Time.now())

# rate object gets a sleep() method which will sleep 1/10 seconds
rate = rospy.Rate(10)

#stops the robot when it is finished going forward and then backward
count = 0

while not rospy.is_shutdown():
    if count == 3: 
        cmd_vel_pub.publish(stop)
        break
    if driving_forward:
        cmd_vel_pub.publish(forward)
    else:
        cmd_vel_pub.publish(backward)

    if change_direction_time < rospy.Time.now():
        print("changing direction")
        driving_forward = not driving_forward
        change_direction_time = rospy.Time.now() + rospy.Duration(5)
        # since velocity is 0.2 m/s, a period of 5 seconds will allow it to go 1 meter
        count += 1
    rate.sleep()