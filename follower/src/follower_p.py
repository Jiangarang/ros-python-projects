#!/usr/bin/env python

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import math


def ang_vel_control(x):
    return -1/(1+math.e**x) + 0.5



class Follower:
    def __init__(self):
        #cv_bridge gets initialized, publishers and subscribers get set up
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback)
        self.centroid_pub = rospy.Publisher('centroid', Image, queue_size=1)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.twist = Twist()
        self.logcount = 0
        self.lostcount = 0

    def image_callback(self, msg):

        # get image from camera
        image = self.bridge.imgmsg_to_cv2(msg)

        # filter out everything that's not yellow
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_yellow = numpy.array([ 40, 0, 0])
        upper_yellow = numpy.array([ 120, 255, 255])
        mask = cv2.inRange(hsv,  lower_yellow, upper_yellow)
        masked = cv2.bitwise_and(image, image, mask=mask)

    # clear all but a 20 pixel band near the top of the image
    # These lines convert the image to the HSV color space and apply a color mask to filter 
    # out everything that is not in the yellow color range.
    # This is done by setting all pixel values outside this band to zero
        h, w, d = image.shape
        search_top = int(3 * h /4)
        search_bot = search_top + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        
    # This helps to reduce noise and focus on the most relevant part of the image
        cv2.imshow("band", mask) # The resulting mask is then displayed in a window called "band"

    # Compute the "centroid" and display a red circle to denote it
        M = cv2.moments(mask) # computes the "centroid" of the yellow pixels in the image
        self.logcount += 1
        print("M00 %d %d" % (M['m00'], self.logcount))

        if M['m00'] > 0:
            cx = int(M['m10']/M['m00']) + 100
            cy = int(M['m01']/M['m00'])
            cv2.circle(image, (cx, cy), 20, (0,0,255), -1)

            # Move at 0.2 M/sec
            # add a turn if the centroid is not in the center
            # Hope for the best. Lots of failure modes.
            err = cx - w/2   # computes the error between the centroid location and the center of the image, in terms of pixels
            self.twist.linear.x = 0.2
            ang_vel  = ang_vel_control(-float(err) / 100) # returns a value between -0.5 and 0.5, which is then multiplied by a constant linear velocity of 0.2 m/s to produce the final twist
            self.twist.angular.z = ang_vel
            self.cmd_vel_pub.publish(self.twist)
            self.centroid_pub.publish(self.bridge.cv2_to_imgmsg(image))
        cv2.imshow("image", image)
        cv2.waitKey(3)

rospy.init_node('follower')
follower = Follower()
rospy.spin()