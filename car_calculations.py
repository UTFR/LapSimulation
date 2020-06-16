
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import constants as c
import math
import pdb
from bisect import bisect_left
from itertools import product


class Car_Calc:
	weight_dist = c.WEIGHT_DIST
	cog_height = c.COG_HEIGHT
	wheel_base = c.WHEEL_BASE
	frontal_area = c.FRONTAL_AREA
	mass = c.MASS
	lat_friction = c.LAT_TIRE
	long_friction = c.LONG_TIRE
	wheel_radius = c.WHEEL_RADIUS
	aero_balance = c.AERO_BALANCE
	brake_bias = c.BRAKE_BIAS
	shift_speeds = [0,0,0,0,math.inf]

	mass = 251
	g = 9.81
	final_ratios = [0,0,0,0,math.inf]

	def __init__(self):
		self.calc_final_ratios()
		self.shift_speed(10000)
		# _, _,di1, a = self.acceleration()
		# _, _,di2, d = self.deceleration()
		# #print("reeee: ",di1)
		# #print("reeee: ",di2)
		# di1 = np.cumsum(di1)
		# di2 = np.cumsum(di2)
		# fig, ax = plt.subplots()
		# ax.plot(di1, a)
		# ax.plot(di2, d)
		# plt.show()
		# pdb.set_trace()



	def rpm_to_rad_s(self, rpm):
		return rpm*(np.pi)/30

	def rad_s_to_rpm(self, rad_s):
		return rad_s*30/np.pi

	def shift_speed(self,shift_rpm):
		for i in range(len(self.shift_speeds)-1):
			shift = self.rpm_to_rad_s(shift_rpm)*self.wheel_radius/self.final_ratios[i]
			self.shift_speeds[i] = shift

	def calc_final_ratios(self):
		final_ratios = np.zeros(len(c.GEAR_RATIOS))
		for i in range(len(self.final_ratios)):
			self.final_ratios[i] = c.GEAR_RATIOS[i]*c.GEAR_RATIOS[-1]

	def linear_interpolation(self,torque_index,car_rpm):
			torque_low = c.TORQUE_CURVE[1][torque_index-1]
			torque_high = c.TORQUE_CURVE[1][torque_index]
			return ((torque_high-torque_low)/500)*(car_rpm-c.TORQUE_CURVE[0][torque_index-1]) + torque_low

	def calc_torque(self, velo):
		min_velocity = self.rpm_to_rad_s(3000)*self.wheel_radius/self.final_ratios[0]
		car_rpm = 0
		torque_index = 0

		if (velo < min_velocity):
			torque = c.TORQUE_CURVE[1][0]
			gear = self.final_ratios[0]
		else:
			wheel_rpm = self.rad_s_to_rpm(velo/self.wheel_radius)
			gear_index = bisect_left(self.shift_speeds, velo)
			gear = self.final_ratios[gear_index]
			car_rpm = wheel_rpm*gear
			torque_index = bisect_left(c.TORQUE_CURVE[0], car_rpm)

			if (car_rpm == c.TORQUE_CURVE[0][torque_index]):
				torque = c.TORQUE_CURVE[1][torque_index]
			else:
				torque = self.linear_interpolation(torque_index,car_rpm)
		print(car_rpm)

		return torque, gear

	def acceleration_single_iter(self, velo, delta_dis, accel, torque, gear):

		#F_d = 1/2*p*v^2*cd*A
		drag = 0.5*c.AIR_DENSITY*c.CD*self.frontal_area*velo**2
		#F_d = 1/2*W*H*F*p*v^2
		downforce = (1-self.weight_dist)*0.5*c.AIR_DENSITY*c.CL*self.frontal_area*velo**2
		#load_transfer = ahw/gb
		weight_transfer = accel*self.cog_height*self.mass/self.wheel_base

		#normal force at center of gravity of the car
		F_normal = self.mass*c.G + downforce
		#car is rear-wheel drive
		F_normal_rear = F_normal*(1-self.weight_dist) + weight_transfer
		#max force the car can apply to rear wheels
		F_friction = F_normal_rear*self.lat_friction
		#force applied by engine to wheel
		F_app = torque*gear/self.wheel_radius
		#make sure wheels don't spin
		if(F_app > F_friction):
			F_app = F_friction

		#include drag
		F_tot = F_app - drag

		#get acceleration, F=ma
		new_accel = F_app/self.mass
		#v_f^2 = v_i^2 + 2ax
		new_velo = np.sqrt(velo**2 + 2*new_accel*delta_dis)
		#v_f = v_i + at
		delta_time = abs(velo-new_velo)/new_accel
		#print(delta_time, new_velo, new_accel)

		return new_accel, new_velo, delta_time

	def acceleration(self):
		max_velo = self.rpm_to_rad_s(10500)*self.wheel_radius/self.final_ratios[4]

		velo = 0
		delta_dis = 0.1
		accel = 0
		distance_total = 0

		accel_arr = []
		velo_arr = []
		dist_arr = []
		time_arr = []
		torque, gear = self.calc_torque(max_velo)

		while(velo < max_velo):
			torque, gear = self.calc_torque(velo)
			new_accel, new_velo, delta_time = self.acceleration_single_iter(velo, delta_dis, accel, torque, gear)

			accel_arr.append(new_accel)
			velo_arr.append(new_velo)
			dist_arr.append(distance_total)
			time_arr.append(delta_time)

			velo = new_velo
			accel = new_accel
			distance_total += delta_dis


		# fig, ax = plt.subplots()
		# ax.plot(dist_arr, velo_arr)
		# plt.show()
		#pdb.set_trace()
		return velo_arr, dist_arr, time_arr

	def deceleration_single_iter(self, velo, delta_dis, accel):
		#F_d = 1/2*p*v^2*cd*A
		drag = 0.5*c.AIR_DENSITY*c.CD*self.frontal_area*velo**2
		#F_d = 1/2*W*H*F*p*v^2
		downforce = 0.5*c.AIR_DENSITY*c.CL*self.frontal_area*velo**2
		#load_transfer = ahw/gb
		weight_transfer = accel*self.cog_height*self.mass/self.wheel_base

		#normal force at center of gravity of the car
		F_normal = self.mass*c.G

		#brakes apply to all 4 wheels, weight shifts forward
		F_normal_rear = -F_normal*(1-self.weight_dist) - downforce*(1-self.aero_balance) + weight_transfer
		F_normal_front = -F_normal*self.weight_dist - downforce*(self.aero_balance) - weight_transfer

		#max force the car can apply to rear wheels
		F_friction_rear = F_normal_rear*self.lat_friction
		#max force the car can apply to front wheels
		F_friction_front = F_normal_front*self.lat_friction

		#make sure neither of the wheels skid
		F_braking = max(F_friction_front/self.brake_bias, F_friction_rear/(1-self.brake_bias))
		F_app = F_braking - drag

		#print("a", F_friction_front/self.brake_bias, F_friction_rear/(1-self.brake_bias))
		#pdb.set_trace()


		#calc accel, F=ma
		new_accel = F_braking/self.mass
		#v_f^2 = v_i^2 + 2ax
		if (velo**2 + 2*accel*delta_dis < 0):
			new_velo = 0
		else:
			new_velo = np.sqrt(velo**2 + 2*accel*delta_dis)
		#v_f = v_i + at
		delta_time = -abs(velo-new_velo)/new_accel
		#print("a", new_accel, new_velo, delta_time)
		print(delta_time, new_velo, new_accel, downforce*(1-self.aero_balance))

		return new_accel, new_velo, delta_time


	def deceleration(self):
		#max possible velocity
		velo = self.rpm_to_rad_s(10500)*self.wheel_radius/self.final_ratios[4]
		delta_dis = 0.1
		accel = 0
		distance_total = 0

		accel_arr = []
		velo_arr = []
		dist_arr = []
		time_arr = []

		while(velo > 0):
			new_accel, new_velo, delta_time = self.deceleration_single_iter(velo, delta_dis, accel)
			#pdb.set_trace()

			accel_arr.append(new_accel)
			velo_arr.append(new_velo)
			dist_arr.append(distance_total)
			time_arr.append(delta_time)

			velo = new_velo
			accel = new_accel
			distance_total += delta_dis


		# fig, ax = plt.subplots()
		# ax.plot(dist_arr, velo_arr)
		# plt.show()
		# pdb.set_trace()
		return velo_arr, dist_arr, time_arr

	def corner_calc(self, radius, corner_len):
		new_accel = 1
		error = 1;
		max_velo = self.rpm_to_rad_s(c.TORQUE_CURVE[0][-1])*self.wheel_radius/self.final_ratios[-2]

		while(error > 0.001):
			accel = new_accel
			velo = np.sqrt(accel*radius)
			if(velo > max_velo):
				velo = max_velo
				break
			else:
				downforce = 0.5*c.AIR_DENSITY*c.CL*self.frontal_area*velo**2
				lat_force = (self.mass*c.G + downforce)*self.lat_friction
				new_accel = lat_force/self.mass
				error = np.absolute(new_accel - accel)

		if (velo == max_velo):
			time = corner_len/velo
		else:
			velo = np.sqrt(new_accel*radius)
			time = corner_len/velo

		dist_arr = np.arange(0, corner_len/0.1, 0.1)
		velo_arr = np.full(len(dist_arr), velo)

		return time, velo#velo_arr, dist_arr

	def find_intersection(self, arr1, arr2):
		intersect = min(product(arr1, arr2), key=lambda t: abs(t[0]-t[1]))[0]
		intersect_index = bisect_left(arr1, intersect, lo=0, hi=min(len(arr1), len(arr2)))
		return intersect, intersect_index

	def find_intersection_val(self, arr, value):
		intersect = min(arr, key=lambda t : abs(t - value))
		intersect_index = (np.abs(arr - intersect)).argmin()
		return intersect, intersect_index

	def straight_calc(self, velo_in, velo_out):
		velo_arr_decel, dist_arr_decel, time_arr_decel = self.deceleration()
		velo_arr_accel, dist_arr_accel, time_arr_accel = self.acceleration()

		_, velo_in_index = self.find_intersection_val(velo_arr_accel, velo_in)
		_, velo_out_index = self.find_intersection_val(velo_arr_decel, velo_out)
		#print(velo_out_index)
		#print(velo_arr_decel)

		velo_arr_decel = velo_arr_decel[:velo_out_index]
		velo_arr_accel = velo_arr_accel[velo_in_index:]
		#print(velo_out_index, velo_in_index, velo_in, velo_out)
		#pdb.set_trace()

		# velo_arr_decel = velo_arr_decel[:-1]
		# velo_arr_accel = velo_arr_accel[0:]
		d1 = np.zeros(len(velo_arr_accel))
		d2 = np.zeros(len(velo_arr_decel))
		# for i in range(len(d1)):
		# 	d1[i]=0.1*i
		# for i in range(len(d2)):
		# 	d2[i]=0.1*i
		# fig, ax = plt.subplots()
		# ax.plot(d1, velo_arr_accel)
		# print(len(velo_arr_decel))
		# ax.plot(d2, velo_arr_decel)
		# plt.show()

		intersect, intersect_index = self.find_intersection(velo_arr_accel, velo_arr_decel)

		decel_cropped = time_arr_decel[intersect_index:velo_out_index]
		accel_cropped = time_arr_accel[velo_in_index:intersect_index]
		time = sum(decel_cropped) + sum(accel_cropped)

		print("ree",velo_arr_accel[intersect_index], velo_in)#, velo_arr_accel[velo_out_index], velo_arr_decel[velo_in_index])#, velo_arr_decel[intersect_index])
		return time, velo_arr_accel[velo_in_index:intersect_index], velo_arr_decel[intersect_index:velo_out_index]






















