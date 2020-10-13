#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Empty
from turtlesim.msg import Pose
import tf
from tf.transformations import euler_from_quaternion
from math import degrees
import time
import math

x = 0
y = 0
theta = 0

def poseCallBack(pose_message):
    global x, y, theta
    pose_jackal = pose_message.pose.pose
    x = pose_jackal.position.x
    y = pose_jackal.position.y
    q1 = pose_jackal.orientation.x
    q2 = pose_jackal.orientation.y
    q3 = pose_jackal.orientation.z
    q4 = pose_jackal.orientation.w
    q = (q1, q2, q3, q4)
    e = euler_from_quaternion(q)
    print "robot's pose: [%f,%f,%f]"%(x,y,e[2])
    theta = e[2]

def to_positive_angle(th):
    while True:
        if th < 0:
            th += 360
        if th > 0:
            ans = th % 360
            return ans
            break

def move(speed, distance, isForward):
    velocity_message = Twist()

    if (isForward):
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0

    velocity_message.angular.x = 0
    velocity_message.angular.y = 0
    velocity_message.angular.z = 0

    time_t0 = rospy.Time.now().to_sec()
    current_distance = 0
    loop_rate = rospy.Rate(10)
    test = True
    while test:
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        time_t1 = rospy.Time.now().to_sec()
        current_distance = speed * (time_t1 - time_t0)
        

        if not (current_distance < distance):
            test = False
    
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)

def degrees2radians(angular_speed):
    return angular_speed * 3.1415/180.0

def radians2degrees(rad):
    return rad * 180.0/3.1415

def rotate(angular_speed, relative_angle, isClockwise):
    velocity_message = Twist()

    velocity_message.linear.x = 0
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0

    velocity_message.angular.x = 0
    velocity_message.angular.y = 0
    if (isClockwise):
        velocity_message.angular.z = -abs(angular_speed)
    else:
        velocity_message.angular.z = abs(angular_speed)

    time_t0 = rospy.Time.now().to_sec()
    current_angle = 0
    loop_rate = rospy.Rate(10)    
    test = True
    while test:
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        time_t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (time_t1 - time_t0)
        if not (current_angle < relative_angle):
            test = False
    
    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)

def setDesideredOrientation(desired_angle):
    difference_angle = desired_angle - theta
    isClockwise_h = False
    if (difference_angle < 0):
        isClockwise_h = True
    rotate(abs(difference_angle), abs(difference_angle), isClockwise_h)

def moveGoal(goal_x, goal_y, goal_theta, distance_tolerance):
    global x, y, theta
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0

    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    test = True
    while (test):
        K_linear = .2
        diff_x = goal_x - x
        diff_y = goal_y - y
        print "diff_x: [%f = %f - %f]"%(diff_x,goal_x,x)
        print "diff_y: [%f = %f - %f]"%(diff_y,goal_y,y)
        distance = abs(math.sqrt((diff_x**2) + (diff_y**2)))
        print "distance: [%f]"%(distance)
        linear_speed = distance * K_linear
        print "linear_speed: [%f]"%(linear_speed)

        K_angular = 2.0
        desired_angle_goal = math.atan2(diff_y, diff_x)
        print "desired_angle_goal: [%f]"%(desired_angle_goal)
        print "desired_angle_goal: %f | theta: %f"%(radians2degrees(desired_angle_goal),radians2degrees(theta))
        angular_speed = (desired_angle_goal-theta)*K_angular
        print "angular_speed: [%f]"%(angular_speed)

        vel_msg.linear.x = linear_speed
        vel_msg.angular.z = angular_speed
        print "robot's pose: [%f,%f,%f]"%(x,y,theta)
        print "movement: [%f,%f]"%(vel_msg.linear.x,vel_msg.angular.z)
        print " "
        velocity_publisher.publish(vel_msg)

        if (distance < distance_tolerance):
            #setDesideredOrientation(goal_theta)
            test = False

def  keyboardTeleop():
	mv = input('Move the robot:\n1 - Forward\n2 - Backward\n3 - Left\n4 - Right\n0 - Stop\n5 - Quit\n')
	vel_msg = Twist()
	vel_msg.linear.x = 0
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0

	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	while(mv != 5):
		if(mv == 1):
			vel_msg.angular.z = 0
			if(vel_msg.linear.x < 0):
				vel_msg.linear.x = 0
			vel_msg.linear.x = vel_msg.linear.x + 1 
			print "Forward: %f"%(vel_msg.linear.x)
		if(mv == 2):
			vel_msg.angular.z = 0
			if(vel_msg.linear.x > 0):
				vel_msg.linear.x = 0
			vel_msg.linear.x = vel_msg.linear.x - 1 
			print "Backward: %f"%(vel_msg.linear.x)
		if(mv == 3):
			vel_msg.linear.x = 0
			if(vel_msg.angular.z < 0):
				vel_msg.angular.z = 0
			vel_msg.angular.z = vel_msg.angular.z + 1 
			print "Lef: %f"%(vel_msg.angular.z)
		if(mv == 4):
			vel_msg.linear.x = 0
			if(vel_msg.angular.z > 0):
				vel_msg.angular.z = 0
			vel_msg.angular.z = vel_msg.angular.z - 1 
			print "Right: %f"%(vel_msg.angular.z)
		if(mv == 0):
			vel_msg.linear.x = 0
			vel_msg.angular.z = 0
			print "Right: %f, %f"%(vel_msg.linear.x,vel_msg.angular.z)
		velocity_publisher.publish(vel_msg)
		mv = input('Move the robot:\n1 - Forward\n2 - Backward\n3 - Left\n4 - Right\n0 - Stop\n5 - Quit\n')


if __name__ == '__main__':
    try:
        rospy.init_node('move_jackal', anonymous=True)
        velocity_publisher = rospy.Publisher("/jackal_velocity_controller/cmd_vel", Twist, queue_size = 10) 
        #pose_subscriber = rospy.Subscriber("/odometry/filtered", Odometry, poseCallBack) 
        time.sleep(.2)
        #move(1, 4, 1)
        
        #rotate(degrees2radians(30), degrees2radians(90), 1)
        
        #setDesideredOrientation(degrees2radians(120))
        
        
        goal_x = 0.0
        goal_y = 0.0
        goal_theta = degrees2radians(90)
        #moveGoal(goal_x, goal_y, goal_theta, 0.01);
	keyboardTeleop()

        #gridClean()

        #spiralClean()
        #rospy.spin()

    except rospy.ROSInternalException:
        rospy.loginfo("Node terminated.")
