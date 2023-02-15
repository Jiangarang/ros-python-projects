#!/usr/bin/env python

import rospy
import time
import sys
import math
import tf
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# fill in scan callback
def scan_cb(msg):
   return

# it is not necessary to add more code here but it could be useful
def key_cb(msg):
   global state; global last_key_press_time
   state = msg.data.lower()
   last_key_press_time = rospy.Time.now()

# odom is also not necessary but very useful
def odom_cb(msg):
   return


# print the state of the robot
def print_state():
   print("---")
   print("STATE: " + state)

   # calculate time since last key stroke
   time_since = rospy.Time.now() - last_key_press_time
   print("SECS SINCE LAST KEY PRESS: " + str(time_since.secs))

# init node
rospy.init_node('dance')

# subscribers/publishers
scan_sub = rospy.Subscriber('scan', LaserScan, scan_cb)

# RUN rosrun prrexamples key_publisher.py to get /keys
key_sub = rospy.Subscriber('keys', String, key_cb)
odom_sub = rospy.Subscriber('odom', Odometry, odom_cb)
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

# start in state halted and grab the current time
state = "h"
last_key_press_time = rospy.Time.now()

# set rate
rate = rospy.Rate(10)

""" l: rotate left
r: rotate right
f: move forward
b: move backward
h: halt all motion
s: spiraling motion (like a curl or a spring)
z: zigzag motion """

# Wait for published topics, exit on ^c
while not rospy.is_shutdown():
   # print out the current state and time since last key press
   print_state()

   # publish cmd_vel from here 
   
   t = Twist()
   if state == "l":
        t.angular.z = 0.2
        t.linear.x = 0
   elif state == "r":
        t.angular.z = -0.2
        t.linear.x = 0
   elif state == "f":
        t.angular.z = 0
        t.linear.x = 0.2
   elif state == "b":
        t.angular.z = 0
        t.linear.x = -0.2
   elif state == "s":
        t.angular.z = 2
        t.linear.x = 0.2
   elif state == "z":
        t.angular.z = -2
        t.linear.x = 0.2

   cmd_vel_pub.publish(t)

   # run at 10hz
   rate.sleep()