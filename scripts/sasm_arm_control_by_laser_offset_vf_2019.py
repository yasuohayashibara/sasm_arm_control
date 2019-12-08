#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('sasm_arm_control')
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import Float32

class sasm_arm_repetition:
    def __init__(self):
        self.target_angles = [-0.001, 0.0, 0.0, 0.0, 0.1, 0.001, 0.0, 0.0, 0.0, -0.1]
        self.index = 0
        self.timer = rospy.Timer(rospy.Duration(2), self.callback)
        self.current_position_sub = rospy.Subscriber("/position", Float32, self.callback_position)
        self.target_position_pub = rospy.Publisher("/joint_0_controller/command", Float64, queue_size=10)
        self.current_position = 0
        self.target_position = - 1.732
        self.offset = 0
        self.lpf_offset = 0
        self.target = 600
        self.margin = 1

    def callback(self, data):
        self.index += 1
        if (self.index >= len(self.target_angles)):
            self.index = 0
        self.target_position = self.target_angles[self.index] - 1.732
        self.target_position_pub.publish(self.target_position + self.lpf_offset)
        self.offset = 0

    def callback_position(self, data):
        self.current_position = data.data;
        if self.target_angles[self.index] == 0:
            diff = self.target - self.current_position
            if (diff > self.margin):
                self.offset -= min([max([0.00005 * diff, -0.0005]), 0.0005])
                self.lpf_offset -= 0.0000005 * diff
            if (diff < - self.margin):
                self.offset -= min([max([0.00005 * diff, -0.0005]), 0.0005])
                self.lpf_offset -= 0.0000005 * diff
            print(str(self.lpf_offset))
            self.target_position_pub.publish(self.target_position + self.lpf_offset + self.offset)

if __name__ == '__main__':
    rospy.init_node('sasm_arm_repetition', anonymous=True)
    tr = sasm_arm_repetition()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
