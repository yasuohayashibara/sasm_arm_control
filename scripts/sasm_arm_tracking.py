#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('sasm_arm_control')
import rospy
from std_msgs.msg import Float64, Float32, Int8

class sasm_arm_tracking:
    def __init__(self):
        self.current_position_sub = rospy.Subscriber("/position", Float32, self.callback)
        self.target_position_pub = rospy.Publisher("/joint_0_controller/command", Float64, queue_size=10)
        self.current_position = 0
        self.target_position = 0

    def callback(self, data):
        self.current_position = data.data;
        self.target_position -= (self.current_position - 320) / 320 * 0.05;
        self.target_position_pub.publish(self.target_position)

if __name__ == '__main__':
    rospy.init_node('sasm_arm_tracking', anonymous=True)
    tr = sasm_arm_tracking()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
