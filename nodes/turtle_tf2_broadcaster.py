#!/usr/bin/env python

import math

import rospy
import tf2_ros
from std_msgs.msg import Time
from webots_ros.srv import set_float, get_float, set_int
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import Range, LaserScan

# Global Variables
foo = '/foo'
tfbr = None
pub_found = None
publisher = None
range = 0

sensor_name = "prox_horizontal_0"
target_name = "target"

def callback(value):
    global range
    range = value.range
    rospy.logwarn(f'{value.header.frame_id}: {range}')
    
    
    scan = LaserScan()
    scan.header.stamp = rospy.Time.now
    scan.header.frame_id = value.header.frame_id
    scan.angle_min = -1.57
    scan.angle_max = 1.57
    scan.angle_increment = 3.14
    scan.time_increment = (1 / 40) / (100)
    scan.range_min = 0.0
    scan.range_max = 100.0

    publisher.publish(scan)


def send_tf_target():
    rospy.wait_for_service(foo + "/prox_horizontal_0/enable")
    rospy.wait_for_service(foo + "/prox_horizontal_1/enable")
    rospy.wait_for_service(foo + "/prox_horizontal_2/enable")
    rospy.wait_for_service(foo + "/prox_horizontal_3/enable")
    rospy.wait_for_service(foo + "/prox_horizontal_4/enable")
    rospy.wait_for_service(foo + "/prox_horizontal_5/enable")
    rospy.wait_for_service(foo + "/prox_horizontal_6/enable")

    service_enable_horizontal_0 = rospy.ServiceProxy(foo + "/prox_horizontal_0/enable", set_int)
    service_enable_horizontal_1 = rospy.ServiceProxy(foo + "/prox_horizontal_1/enable", set_int)
    service_enable_horizontal_2 = rospy.ServiceProxy(foo + "/prox_horizontal_2/enable", set_int)
    service_enable_horizontal_3 = rospy.ServiceProxy(foo + "/prox_horizontal_3/enable", set_int)
    service_enable_horizontal_4 = rospy.ServiceProxy(foo + "/prox_horizontal_4/enable", set_int)
    service_enable_horizontal_5 = rospy.ServiceProxy(foo + "/prox_horizontal_5/enable", set_int)
    service_enable_horizontal_6 = rospy.ServiceProxy(foo + "/prox_horizontal_6/enable", set_int)

    service_enable_horizontal_0.call(10)
    service_enable_horizontal_1.call(10)
    service_enable_horizontal_2.call(10)
    service_enable_horizontal_3.call(10)
    service_enable_horizontal_4.call(10)
    service_enable_horizontal_5.call(10)
    service_enable_horizontal_6.call(10)

    rospy.Subscriber(foo + '/prox_horizontal_0/value', Range, callback)
    rospy.Subscriber(foo + '/prox_horizontal_1/value', Range, callback)
    rospy.Subscriber(foo + '/prox_horizontal_2/value', Range, callback)
    rospy.Subscriber(foo + '/prox_horizontal_3/value', Range, callback)
    rospy.Subscriber(foo + '/prox_horizontal_4/value', Range, callback)
    rospy.Subscriber(foo + '/prox_horizontal_5/value', Range, callback)
    rospy.Subscriber(foo + '/prox_horizontal_6/value', Range, callback)

    # Generate our "found" timestamp
    time_found = rospy.Time.now()

    # Create a transform arbitrarily in the
    # camera frame
    t = TransformStamped()
    t.header.stamp = time_found
    t.header.frame_id = sensor_name
    t.child_frame_id = target_name

    t.transform.translation.x = -0.4
    t.transform.translation.y = 0.2
    t.transform.translation.z = 1.5
    t.transform.rotation.x = 0.0
    t.transform.rotation.y = 0.0
    t.transform.rotation.z = 0.0
    t.transform.rotation.w = 1.0

    # Send the transformation to TF
    # and "found" timestamp to localiser
    tfbr.sendTransform(t)
    pub_found.publish(time_found)

if __name__ == '__main__':
    rospy.init_node('tf2_broadcaster_target')
    rospy.loginfo("tf2_broadcaster_target sending target found...")

    # Setup tf2 broadcaster and timestamp publisher
    tfbr = tf2_ros.TransformBroadcaster()
    pub_found = rospy.Publisher('/emulated_uav/target_found', Time, queue_size=10)
    publisher = rospy.Publisher(foo + '/scan', LaserScan, queue_size=50)

    # Give the nodes a few seconds to configure
    rospy.sleep(rospy.Duration(2))

    # Send out our target messages
    send_tf_target()

    # Give the nodes a few seconds to transmit data
    # then we can exit
    rospy.sleep(rospy.Duration(2))
    rospy.loginfo("tf2_broadcaster_target sent TF and timestamp")
