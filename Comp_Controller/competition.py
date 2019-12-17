import constants as c
from bisect import bisect_left

class Competition:
	data_corner = c.DATA_CORNER
	data_straight = c.DATA_STRAIGHT
	car = None

	def __init__(input_car):
		self.car = input_car

	def run_endurance():
		corner_velos = np.zeros(len(data_corner[1]))
		corner_times = np.zeros(len(data_corner[1]))

		for i in range(len(data_corner[1]):
			corner_times[i], corner_velos[i] = car.corner_calc(data_corner[1][i],data_corner[2,i]))

		straight_times = np.zeros(len(data_straight[1]))
		for i in range(len(data_straight[1])):
			if (i == 1):
				straight_times[i] = car.straight_calc(data_straight[1][i],corner_velos[-1],corner_velos[i])
			else:
				straight_times[i] = car.straight_calc(data_straight[1][i],corner_velos[i-1],corner_velos[i])
		time = np.sum(straight_times) + np.sum(corner_times)

		return time

	def run_accel():
		index = bisect_left(car.accel_dist, 75)
		time_car = car.accel_time[index]
		return time

	def run_skidpad():
		radius = 8.375
		length = 2*np.pi*radius
		time,unused = car.corner_calc(radius,length)
		return time

	def endurance_points_calc(time, worst_time):
		Tmin = worst_time
		Tmax= Tmin * 1.45

		endurance_score = 250*((Tmax/time) - 1)/((Tmax/Tmin) - 1) + 25
		return endurance_score

	def calc_skidpad_points(time, worst_time):
		Tmin = worst_time
		Tmax = Tmin * 1.25

		skidpad_score = 71.5((Tmax/time)**2 - 1)/((Tmax/Tmin)**2 - 1) + 3.5
		return skidpad_score

	def calc_accel_points(time, worst_time):
		Tmin = worst_time
		Tmax = Tmin * 1.5

		accel_score = 95.5*((Tmax/time) - 1)/((Tmax/Tmin) - 1) + 4.5
		return accel_score



