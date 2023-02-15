#!/usr/bin/env python


#This node drives the robot based on information from the other nodes.

import rospy
from state_definitions import *
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16, Float32

#Makes the state message global
def cb_state(msg):
    global state
    state = msg.data
    print ("recieved state from scan: " + str(state))

#Init node
rospy.init_node('driver')

#Make publisher for cmd_vel
pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

#make publisher for current_state
pub_state = rospy.Publisher('current_state', Int16, queue_size = 1)

#Make all subscribers
sub_state = rospy.Subscriber('state', Int16, cb_state)

#Rate object
rate = rospy.Rate(10)

# default state will be set to 0 (searching for wall)
state = 0

#Create two twist variable, one is modified here, one is copied from the PID messages
t_pub = Twist()

print("STARTING")

while not rospy.is_shutdown():
    pub_state.publish(state)
    print("STATE: ", state)

    # state 0 = searching for wall, slowly drive forward until wall is detected 1m away
    if (state == 0):
        t_pub.linear.x = 0.2
        t_pub.angular.z = 0
    # state 1 = wall is ~1m away, rotate the robot until its right side is parallel with wall
    elif (state == 1): 
        t_pub.linear.x = 0
        t_pub.angular.z = 0.2
    
    
    elif (state == 9): # halt
        t_pub.linear.x = 0
        t_pub.angular.z = 0
    else:
        print("STATE NOT FOUND")
    pub_vel.publish(t_pub)
    rate.sleep()
