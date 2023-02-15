#!/usr/bin/env python

#This processes all of the scan values


import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16, Float32
#from constants import *

#grab current state from driver.py
def cb_state(msg):
    global state
    state = msg.data
    print ("recieved state from driver: " + str(state))

#Process all the data from the LIDAR
def cb(msg):
    global state
    distance_front = (msg.ranges[-1] + msg.ranges[0] + msg.ranges[1]) / 3
    distance_left = (msg.ranges[88] + msg.ranges[89] + msg.ranges[90]) / 3
    distance_right = (msg.ranges[268] + msg.ranges[269] + msg.ranges[270]) / 3
    distance_rear = (msg.ranges[178] + msg.ranges[179] + msg.ranges[180]) / 3

    print(str(distance_front))
    print(str(distance_left))
    print(str(distance_right))
    print(str(distance_rear))

    if (state == 0 and distance_front <= 1): # if wall is <= 1m ahead, begin rotating robot until shortest distance is aligned to right side
        state = 1
    elif (state == 1 and distance_right > distance_front and distance_right > distance_back):
        state = 0
    else:
        state = 9

    pub_state.publish(state)
    #CALCULATE AND PUBLISH ANYTHING ELSE FOR THE PID



#Init node
rospy.init_node('scan_values_handler')

#Subscriber for LIDAR
sub = rospy.Subscriber('scan', LaserScan, cb)

#subscriber for current state
sub_state = rospy.Subscriber('current_state', Int16, cb_state)

#Publishers
pub_state = rospy.Publisher('state', Int16, queue_size = 1)
#THINK OF WHAT INFO TO PUBLISH TO THE PID

#Rate object
rate = rospy.Rate(10)

#Keep the node running
while not rospy.is_shutdown():
    print ("scan handler running... ")
    rate.sleep() 