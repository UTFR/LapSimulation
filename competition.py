import constants as c
from bisect import bisect_left
import numpy as np

class Competition:
	data_corner = c.DATA_CORNER
	data_straight = c.DATA_STRAIGHT
	car = None
	num_corners = 0
	num_straights = 0

	def __init__(self, input_car):
		self.car = input_car
		self.num_corners = len(self.data_corner[0])
		self.num_straights = len(self.data_straight[0])

	def run_endurance(self):
		corner_velos = np.zeros(self.num_corners)
		corner_times = np.zeros(self.num_corners)

		for i in range(self.num_corners):
			corner_times[i], corner_velos[i] = self.car.corner_calc(self.data_corner[0][i],self.data_corner[1][i])

		straight_times = np.zeros(self.num_straights)
		for i in range(self.num_straights):
			if (i == 0):
				straight_times[i] = self.car.straight_calc(self.data_straight[1][i],corner_velos[-1],corner_velos[i])
			else:
				straight_times[i] = self.car.straight_calc(self.data_straight[1][i],corner_velos[i-1],corner_velos[i])

		print("straight_times", straight_times)
		time = np.sum(straight_times) + np.sum(corner_times)
		print("time:" ,time/60)
		# print("corner_velos:", corner_velos)
		# print("corner_times:", corner_times)

		return time

	def run_accel(self):
		index = bisect_left(car.accel_dist, 75)
		time_car = car.accel_time[index]
		return time

	def run_skidpad(self):
		radius = 8.375
		length = 2*np.pi*radius
		time,unused = car.corner_calc(radius,length)
		return time

	def endurance_points_calc(self, time, worst_time):
		Tmin = worst_time
		Tmax= Tmin * 1.45

		endurance_score = 250*((Tmax/time) - 1)/((Tmax/Tmin) - 1) + 25
		return endurance_score

	def calc_skidpad_points(self, time, worst_time):
		Tmin = worst_time
		Tmax = Tmin * 1.25

		skidpad_score = 71.5((Tmax/time)**2 - 1)/((Tmax/Tmin)**2 - 1) + 3.5
		return skidpad_score

	def calc_accel_points(self, time, worst_time):
		Tmin = worst_time
		Tmax = Tmin * 1.5

		accel_score = 95.5*((Tmax/time) - 1)/((Tmax/Tmin) - 1) + 4.5
		return accel_score



