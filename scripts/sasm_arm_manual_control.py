#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('sasm_arm_control')
import rospy
from std_msgs.msg import Float64
import sys
import readchar

class sasm_arm_manual_control:
    def __init__(self):
        self.target_position_pub = rospy.Publisher("/joint_0_controller/command", Float64, queue_size=10)
        self.target_position = 0.0

    def loop(self):
    	c = readchar.readchar()
        if c == 'z':
            self.target_position += 0.001
        elif c == 'x':
            self.target_position -= 0.001
        elif c == 'a':
            self.target_position += 0.01
        elif c == 's':
            self.target_position -= 0.01
        elif c == 'q':
            self.target_position += 0.1
        elif c == 'w':
            self.target_position -= 0.1
        self.target_position_pub.publish(self.target_position)
        print(self.target_position)

if __name__ == '__main__':
    rospy.init_node('sasm_arm_manual_control', anonymous=True)
    mc = sasm_arm_manual_control()
    r = rospy.Rate(10)
    try:
        while not rospy.is_shutdown():
            mc.loop();
            r.sleep()
    except KeyboardInterrupt:
        print("Shutting Down")
