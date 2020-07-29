#!/usr/bin/env python
# Software License Agreement (BSD License)
#

import rospy
import numpy as np
import math
import T_computations as t
import J_computations as j

from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg

from std_msgs.msg import Float64MultiArray,MultiArrayDimension
from sensor_msgs.msg import JointState

# Obtained by building the file IK_JTA.srv
from math_pkg.srv import IK_JTA
from math_pkg.srv import IK_JTARequest
from math_pkg.srv import IK_JTAResponse

# Calculations to compute 6 dof Jacobian
def calculations_6(q_smartphone):

    p = np.pi
    n_joints = 6

    # Links length. [mm]
    L0 = 270.35
    L1 = 69.00
    L2 = 364.35
    L3 = 69.00
    Lh = math.sqrt(L2** 2 + L3** 2)
    L4 = 374.29
    L5 = 10.00
    L6 = 368.30

    # DH table of Baxter: alpha(i-1), a(i-1), d(i), theta(i).
    # Last row relates last joint to end-effector.
    DH = np.array([[0, 0, L0, 0],
                   [-p/2, L1, 0, p/2],
                   [0, Lh, 0, p/2],
                   [p/2, 0, L4, 0],
                   [-p/2, L5, 0, 0],
                   [p/2, 0, 0, 0],
                   [0, 0, L6, 0]])

    # Trasformation matrices given DH table. T0,1 T1,2 ... T7,e
    T_rel_ini = t.DH_to_T(DH)
    
    # type of joints, 1 = revolute, 0 = prismatic.
    info = np.array([1, 1, 1, 1, 1, 1])

    #print"Size info: %s\n"%(info.size)
    #print"Size q_smart: %s\n"%(q_smartphone.size)

    # initial q
    q = np.array([0, 0, 0, 0, 0, 0])
    
    #print"Size q: %s\n"%(q)

    ########
    # Entry point when receiving q from coppeliasim!!
    # Use q_smartphone

    #print"q_smartphone inside function:\n%s\n"%(q_smartphone.size)

    # transformations matrices given the configuration.
    T_trans = t.transformations(T_rel_ini,q_smartphone, info)

    # T0,1 T0,2 T0,3...T0,e
    T_abs = t.abs_trans(T_trans)

    # extract geometric vectors needed for computations.
    geom_v = j.geometric_vectors(T_abs)

    np.set_printoptions(precision = 4)
    np.set_printoptions(suppress = True)

    k = geom_v[0] # axis of rotation of the revolute joins projected on zero
    r = geom_v[1] # distances end_effector, joints projected on zero.

    Js = j.jacob(k, r, n_joints, info)
    #print(Js)
    return Js

# Callback Function for the Joints Positions
def jacobian_callback(data):
    global J_6
    q_smartphone = np.array(data.position)
    q_smartphone = np.delete(q_smartphone,2,0)
    rospy.loginfo("Joint positions: %s\n", str(q_smartphone))
    
    # Compute matrices
    J_6 = calculations_6(q_smartphone)
    rospy.loginfo("Jacobian:\n%s\n", J_6)

# Callback Function for the error on the position (error on Xee)
def error_callback(message):

    global error
    err_orient = np.array([message.data[:3]]).T
    err_pos = np.array([message.data[3:6]]).T
    error = np.concatenate((err_pos,err_orient), axis=0)
    rospy.loginfo("Received Position Error:\n%s\n", str(error))

# Callback Function for the error on the position (error on Xee)
def vel_callback(message):

    global vel
    vel = np.array([message.data[:6]]).T
    rospy.loginfo("Received Velocities End Effector:\n%s\n", str(vel))

# Handler for the Server
def handle_IK_JAnalytic(req):

    # q_dot initialization
    q_dot = JointState()
    
    # Gain for the Control Law
    K = 20

    print"Server Analytic accepted request\n"

    # q_dot definition, taking into account the error on the position
    q_dot_6 = np.linalg.pinv(J_6).dot(vel+K*error)

    # Since the third Joint is blocked, its velocity is 0
    q_dot.velocity = np.insert(q_dot_6,2,0)

    #q_dot.velocity = np.linalg.pinv(J_6).dot(vel+K*error)
    return IK_JTAResponse(q_dot)

def jac_mat():

    # Init node
    rospy.init_node('jac_mat', anonymous=True)

    rospy.loginfo("Server Analytic Initialized\n")

    # Subscribe for error positions
    rospy.Subscriber("errors", Float64MultiArray, error_callback)

    # Subscribe for error positions
    rospy.Subscriber("tracking", Float64MultiArray, vel_callback)

    # Subscribe for joint positions
    rospy.Subscriber("logtopic", JointState, jacobian_callback)

    # Service Definition
    s_vel = rospy.Service('IK_JAnalytic', IK_JTA, handle_IK_JAnalytic)

    rospy.spin()
    
if __name__ == '__main__':
    try:
        jac_mat()
    except rospy.ROSInterruptException:
        pass
