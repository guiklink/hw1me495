#!/usr/bin/env python
#import math
import numpy
import rospy
import std_msgs
import rosbag 

from math import cos, sin, pi, sqrt
from geometry_msgs.msg import Twist, Vector3
from turtlesim.srv import TeleportAbsolute

#The below command will allow us to get user input when asking for the period
#or the length of time that it takes the turtle to traverse one
#figure 8

T = input('Enter the period of the function (T): ')
print("T=", T)

def send_values():
	#This is initializing the publisher node
	pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	rospy.init_node('send_values', anonymous=True)
	#Setting the rate at which the publisher is sending messages to the subscriber
	r = rospy.Rate(70)
	init_time = rospy.get_time()

	while not rospy.is_shutdown():
		useful_time = rospy.get_time()-init_time

		#The x and y positions are a function of time and we can take the derivative
		#of them to obtain the velocity and take the derivative again to get the accelerations

		x = 3.0*sin(4.0*pi*useful_time/T)
		y = 3.0*sin(2.0*pi*useful_time/T)

		vx = 12.0*pi*cos((4.0*pi*useful_time)/T)/T
		vy =  6.0*pi*cos((2.0*pi*useful_time)/T)/T

		ax = -48*pi*pi*sin((4.0*pi*useful_time)/T)/(T*T)
		ay = -12*pi*pi*sin((2.0*pi*useful_time)/T)/(T*T)

		v = (sqrt(vx*vx + vy*vy))

		#can get the omega by taking the derivative of theta = arctan(vy/vx)
		omega = ((vx*ay)-(vy*ax)) /((vx*vx) + (vy*vy))

		#The subscriber node takes two items as an input inthe form of twist: omega and v
		vel_cmd_out = Twist(Vector3(v,0,0),Vector3(0,0,omega))
		rospy.loginfo(vel_cmd_out)
		pub.publish(vel_cmd_out)

		r.sleep()

if __name__ == '__main__':
	try:
		rospy.wait_for_service('turtle1/teleport_absolute')
		turtle_sp = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
		turtle_sp = (8,3.54,100)
		send_values()
	except rospy.ROSInterruptException: pass