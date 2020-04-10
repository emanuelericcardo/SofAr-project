#!/usr/bin/env python
import rospy
import numpy as np
import tf
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3

class Kalman(object):
	"""docstring for Kalman"""
	def __init__(self, n_states, n_sensors):
		super(Kalman, self).__init__()
		self.n_states = n_states
		self.n_sensors = n_sensors

		self.x = np.matrix(np.zeros(shape=(n_states,1)))
		self.sigma = np.matrix(np.identity(n_states)) 
		self.F = np.matrix(np.identity(n_states))
		self.u = np.matrix(np.zeros(shape=(n_states,1)))
		self.G = np.matrix(np.zeros(shape=(n_sensors, n_states)))
		self.R = np.matrix(np.identity(n_sensors))
		self.I = np.matrix(np.identity(n_states))

		self.first = True

	def predict(self):
		self.x = self.F * self.x + self.u
		self.sigma = self.F * self.sigma * self.F.getT()

	def update(self, Y):
		'''Y: new sensor values as numpy matrix'''

		w = Y - self.G * self.x
		S = self.G * self.sigma * self.G.getT() + self.R
		H = self.sigma * self.G.getT() * S.getI()
		self.x = self.x + H * w
		self.sigma = (self.I - H * self.G) * self.sigma

# rotate vector v1 by quaternion q1 
def qv_mult(q1, v1):

	#v1 = tf.transformations.unit_vector(v1)
	q2 = list(v1)
	q2.append(0.0)

	return tf.transformations.quaternion_multiply(
		tf.transformations.quaternion_multiply(q1, q2), 
		tf.transformations.quaternion_conjugate(q1)
	)[:3]


def callback(data):

	linear_acceleration = Vector3()
	orientation = [data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]

	linear_acceleration.x = data.linear_acceleration.x
	linear_acceleration.y = data.linear_acceleration.y
	linear_acceleration.z = data.linear_acceleration.z

	rospy.loginfo("Imu result:      %lf %lf %lf", linear_acceleration.x,linear_acceleration.y,linear_acceleration.z)

	Z = np.matrix([linear_acceleration.x,linear_acceleration.y,linear_acceleration.z]).getT()

	if kalman.first:
		kalman.x = Z
		kalman.first = False

	
	kalman.predict()
	kalman.update(Z)

	vec = [kalman.x[0], kalman.x[1], kalman.x[2]]

	rospy.loginfo("Kalman result:   %lf %lf %lf", vec[0],vec[1],vec[2])

	vec = qv_mult(orientation,vec)

	rospy.loginfo("Rotation result: %lf %lf %lf", vec[0],vec[1],vec[2])

	for i in range(1,3):
		vec[i] = vec[i] + g_vector[i]

	rospy.loginfo("Final result:    %lf %lf %lf", vec[0],vec[1],vec[2])
	
	
def listener():

	# In ROS, nodes are uniquely named. If two nodes with the same
	# name are launched, the previous one is kicked off. The
	# anonymous=True flag means that rospy will choose a unique
	# name for our 'listener' node so that multiple listeners can
	# run simultaneously.
	rospy.init_node('listener', anonymous=True)

	rospy.Subscriber("android/imu", Imu, callback)

	
	kalman.H = np.matrix(np.identity(kalman.n_states))
	kalman.sigma *= 0.1
	kalman.R *= 0.01

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

if __name__ == '__main__':

	kalman = Kalman(n_states = 3, n_sensors = 3)

	g_vector = [0.0, 0.0, -9.81]

	listener()