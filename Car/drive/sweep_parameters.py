import Car.drive.param_enum.Parameters as Parameters
import numpy as np
import Competitions.competition.Competition as Competition


def select_param(param, value, car):
	param_dict = {
		Parameters.weight_dist: car.set_weight_dist(value),
		Parameters.cog_height: car.set_cog_height(value),
		Parameters.wheel_base: car.set_wheel_base(value),
		Parameters.frontal_area: car.set_frontal_area(value),
		Parameters.mass: car.set_mass(value),
		Parameters.lat_tire: car.set_lat_tire(value),
		Parameters.long_tire: car.set_long_tire(value),
		Parameters.wheel_radius: car.set_wheel_radius(value),
		Parameters.aero_balance: car.set_aero_balance(value),
		Parameters.brake_bias: car.set_brake_bias(value)
	}
	param_dict[param]


def sweep_1param(min_num, max_num, step_size, param, car):
	inc=(max_num-min_num+step_size)/step_size
	nums = np.arange(min_num,max_num,inc)

	points_endurance = np.zeros(len(nums))
	for i in range(len(nums)):
		select_param(param, nums[i], car)

		endurance_time = car.run_endurance()
		endurance_points = Competition.endurance_points_calc(endurance_time)

		points_endurance[i] = endurance_points

	return nums, points_endurance


def sweep_2param(min_num, max_num, step_size, param, min_2num, max_2num, step_size2, param2, car):
	inc1=(max_num-min_num+step_size)/step_size
	inc2=(max_2num-min_2num+step_size2)/step_size2
	nums = np.arange(min_num,max_num,inc1)
	nums2 = np.arange(min_2num,max_2num,inc2)
	select_param(param, car)
	select_param(param2, car)

	points_endurance = np.zeros(len(nums))
	for i in range(len(nums)):
		for j in range(len(nums2)):
			select_param(param, nums[i], car)
			select_param(param2, nums[j], car)

			endurance_time = car.run_endurance()
			endurance_points = Competition.endurance_points_calc(endurance_time)

			points_endurance[i] = endurance_points

	return nums, nums2, points_endurance
