#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('sasm_arm_control')
import rospy
from std_msgs.msg import Float64

class sasm_arm_repetition:
    def __init__(self):
        self.timer = rospy.Timer(rospy.Duration(2), self.callback)
        self.target_position_pub = rospy.Publisher("/joint_0_controller/command", Float64, queue_size=10)
        self.target_position = 0.5

    def callback(self, data):
        self.target_position = -self.target_position;
        self.target_position_pub.publish(self.target_position)

if __name__ == '__main__':
    rospy.init_node('sasm_arm_repetition', anonymous=True)
    tr = sasm_arm_repetition()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
