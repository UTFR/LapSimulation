import constants as c
from Competitions.competition import Competition


class Michigan(Competition):
	data_corner = c.DATA_CORNER
	data_straight = c.DATA_STRAIGHT
	car = None

	def __init__(self, input_car):
		super().__init__(input_car)

	# for each of these, they should not return values to the super class 'competition', but should store them in here,
	# since each competition will have its own individual values but the super class is just there to facilitate
	# the calculation of the points
	def endurance_points_calc(self, time):
		worst_time = 1195.405  # best time
		return super.endurance_points_calc(time, worst_time)

	def skidpad_points_calc(self, time):
		worst_time = 4.865
		return super.skidpad_points_calc(time, worst_time)

	def accel_points_calc(self, time):
		worst_time = 4.109
		return super.accel_points_calc(time, worst_time)
