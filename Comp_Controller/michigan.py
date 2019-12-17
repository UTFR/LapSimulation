import constants as c
from Comp_Controller.competition import Competition

class Michigan(Competition):
	data_corner = c.DATA_CORNER
	data_straight = c.DATA_STRAIGHT
	car = None

	def __init__(input_car):
		super(input_car)

	def endurance_points_calc(time):
		worst_time = 1195.405
		return super.endurance_points_calc(time, worst_time)

	def skidpad_points_calc(time):
		worst_time = 4.865
		return super.skidpad_points_calc(time, worst_time)

	def accel_points_calc(time):
		worst_time = 4.109
		return super.accel_points_calc(time, worst_time)