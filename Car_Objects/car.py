from Car_Objects import constants as c
import numpy as np
from bisect import bisect_left
import math

class Car:
	weight_dist = c.WEIGHT_DIST
	cog_height = c.COG_HEIGHT
	wheel_base = c.WHEEL_BASE
	frontal_area = c.FRONTAL_AREA
	mass = c.MASS
	lat_tire = c.LAT_TIRE
	long_tire = c.LONG_TIRE
	wheel_radius = c.WHEEL_RADIUS
	aero_balance = c.AERO_BALANCE
	brake_bias = c.BRAKE_BIAS

	step_size = 0.01
	shift_speeds = [0,0,0,0,0,0,math.inf] #figure out what these should be, math.inf is for bisect_left
	accel_vel = [] #figure out what to do with this?
	deccel_vel = [] #figure out what to do with this?
	accel_dist = [] #figure out what to do with this?
	accel_time = [] #figure out what to do with this?
	deccel_time = [] #figure out what to do with this?

	def __init__(self):
		print("hi")

	def set_weight_dist(weight_dist):
		self.weight_dist = weight_dist

	def get_weight_dist(weight_dist):
		return self.weight_dist

	def set_cog_height(cog_height):
		self.cog_height = cog_height

	def get_cog_height(cog_height):
		return self.cog_height

	def set_wheel_base(wheel_base):
		self.wheel_base = wheel_base

	def get_wheel_base():
		return self.wheel_base

	def set_frontal_area(frontal_area):
		self.frontal_area = frontal_area

	def get_frontal_area():
		return self.frontal_area

	def set_mass(mass):
		self.mass = mass

	def get_mass():
		return self.mass

	def set_lat_tire(lat_tire):
		self.lat_tire = lat_tire

	def get_lat_tire():
		return self.lat_tire

	def set_long_tire(long_tire):
		self.long_tire = long_tire

	def get_long_tire():
		return self.long_tire

	def set_wheel_radius(wheel_radius):
		self.wheel_radius = wheel_radius

	def get_wheel_radius():
		return wheel_radius

	def set_aero_balance(aero_balance):
		self.aero_balance = aero_balance

	def get_aero_balance():
		return aero_balance

	def set_brake_bias(brake_bias):
		self.brake_bias = brake_bias

	def get_brake_bias():
		return brake_bias

	def shift_gears(rpm):
		index = TORQUE_CURVE[0].index(rpm)
		TORQUE_CURVE[1].index

	def rpm_to_rad_s(rpm):
		return rpm*(np.pi)/30

	def rad_s_to_rpm(rad_s):
		return rad_s*30/np.pi

	def accelerate():
		min_velocity = rpm_to_rad_s(3000)*self.wheel_radius/self.GEAR_RATIOS[1]
		max_gear_velocity = rpm_to_rad_s(10500)*self.wheel_radius/self.GEAR_RATIOS[5]
		velo = 0
		accel = 0
		index = 1
		torque = 0
		gear = 0
		weight_transfer = 0
		force_applied = 0
		distance = []

		velo_out = []
		time_out = []
		force_e_out = []
		accel_out = []

		while (accel >= 0 and (velo < max_gear_velocity)):
			if (velo < min_velocity):
				torque = self.TORQUE_CURVE[1][2]
				gear = self.GEAR_RATIOS[1]
			else:
				wheel_rpm = rad_s_to_rpm(velo/self.wheel_radius)
				gear_index = bisect_left(self.shift_speeds, velo)
				#exact = score == self.shift_speeds[gear_index] <-- might need for later use?
				gear = self.shift_speeds[gear_index] #check if fancy schmancy bisect_left func works
				car_rpm = wheel_rpm*gear
				
				torque_index = bisect_left(self.TORQUE_CURVE[1], car_rpm)
				if (car_rpm == self.TORQUE_CURVE[2][torque_index]):
					torque = self.TORQUE_CURVE[2][torque_index]
				else:
					torque_low = self.TORQUE_CURVE[2][torque_index-1]
					torque_high = self.TORQUE_CURVE[2][torque_index+1]
					#wtf is going on here --> make it shorter?
					torque = ((torque_high-torque_low)/500)*(car_rpm-self.TORQUE_CURVE[1][torque_index-1]) + torque_low

			if (velo == 0):
				weight_transfer = 0
			else:
				weight_transfer = accel*self.mass*self.GRAVITY*self.cog_height/self.wheel_base

			downforce = self.LIFT_COEF*velo**2 #check this
			drag = self.CD*velo**2
			force_e = torque*gear/self.wheel_radius
			force_n = (self.mass/2)*self.GRAVITY + weight_transfer + downforce/2 #tf is this?
			force_tire_max = force_n*self.long_tire

			if (force_e > force_tire_max):
				force_applied = force_tire_max
				print(spinning)
			else:
				force_applied = force_e

			new_accel = (force_applied-drag)/self.mass
			distance[index] = step_size*index #what?

			if (index == 1):
				velo_out[index] = 0
				time_out[index] = 0
			else:
				vel_final = np.sqrt(velo**2 + 2*new_accel*step_size)
				time_out[index] = (vel_final - velo)/new_accel + time_out[index-1]
				velo_out[index] = vel_final*3.6 #where does 3.6 come from?
				velo = vel_final

			force_e_out[index] = force_e
			accel_out[index] = new_accel/self.GRAVITY
			accel = new_accel

			index += 1

		return time_out, velo_out, accel_out, force_e_out


	def decelerate():
		velo = rpm_to_rad_s(10500)*self.wheel_radius/self.GEAR_RATIOS[5]
		index = 1

		static_mass_fr = self.mass*self.weight_transfer
		static_mass_r = self.mass-static_mass_fr
		accel = 2*self.GRAVITY

		downforce = 0
		drag = 0

		accel_out = []
		velo_out = []
		time_out = []
		weight_transfer_out = []
		force_rear_out = []
		force_front_out = []
		brake_bias_ideal = []

		while (velo > 0):
			downforce = self.LIFT_COEF*velo**2
			drag = self.CD*velo**2

			mass_transfer = (accel*self.mass*self.COG_HEIGHT)
			weight_transfer = mass_transfer*self.GRAVITY

			#tf is going on here
			f_norm_front_max = self.GRAVITY*static_mass_fr + weight_transfer + downforce*self.WEIGHT_DIST #check this
			f_norm_rear_max = self.GRAVITY*static_mass_r - weight_transfer + downforce*(1-self.WEIGHT_DIST) #check this

			f_front = f_norm_front_max*self.LONG_TIRE
			f_rear = f_norm_rear_max*self.LONG_TIRE

			f_app_brakes = self.mass*accel
			f_app_front = f_app_brakes*self.brake_bias
			f_app_rear = f_app_brakes*(1-self.brake_bias)

			while(f_app_front > f_front or f_app_rear > f_rear):
				accel -= 0.01
				mass_transfer = accel*self.mass*self.COG_HEIGHT/self.wheel_base
				weight_transfer = mass_transfer*self.GRAVITY
				f_norm_front = self.GRAVITY*static_mass_fr + weight_transfer + downforce*self.WEIGHT_DIST
				f_norm_rear = self.GRAVITY*static_mass_r - weight_transfer + downforce*(1-self.WEIGHT_DIST)

				f_front = f_norm_front*self.long_tire
				f_rear = f_norm_rear*self.long_tire
				f_app_brakes = self.mass*accel
				f_app_front = f_app_brakes*self.brake_bias
				f_app_rear = f_app_brakes*(1-self.brake_bias)
				print("wheels locking")

			accel = f_app_brakes/self.mass
			accel_true = accel+(drag/self.mass)
			vel_new = np.sqrt(velo**2 - 2*accel_true*step_size)
			time = np.abs(vel_new-velo)/accel_true
			distance_out[index] = step_size*index

			if(index == 1):
				velo_out[index] = max_velo
				time_out[index] = 0
			else:
				time_out[index] = time_out[index-1] + time
				velo_out[index] = 3.6*np.abs(vel_new)

			accel_out[index] = accel_true/self.GRAVITY
			weight_transfer_out[index] = mass_transfer
			force_rear_out[index] = f_app_rear
			force_front_out[index] = f_app_front
			brake_bias_ideal[index] = f_front/(f_front+f_rear)
			velo = vel_new
			index += 1

		return distance, time_out, velo_out, accel_out, weight_transfer_out, force_rear_out, force_front_out, brake_bias_ideal

	def corner_calc(radius, corner_len):
		new_accel = 1
		error = 1;
		max_velo = rpm_to_rad_s(c.TORQUE_CURVE[-1])*wheel_radius/self.GEAR_RATIOS[-2]

		while(error > 0.001):
			accel = new_accel
			velo = np.sqrt(accel*self.wheel_radius)
			if(velo > max_velo):
				velo = max_velo
				break
			else:
				downforce = c.LIFT_COEF*velo**2 #double check this
				lat_force = (self.mass*self.F_G + downforce)*self.LAT_TIRE
				new_accel = lat_force/self.mass
				error = np.absolute(new_accel - accel)

		if (velo == max_velo):
			time = corner_len/velo
		else:
			velo = np.sqrt(new_accel*self.radius)
			time = corner_len/velo

		return time, velo

	def straight_calc(length, velo_in, velo_out):
		a = 1
		b = 1

		while (self.accel_vel[a] < velo_in):
			a += 1
		while (self.deccel_vel[b] < velo_out):
			b += 1

		c = a
		d = b

		while (self.accel_dist[c]-self.accel_dist[a]+self.deccel_dist[b]-self.deccel_dist[d] < length):
			if (self.accel_vel[c] < self.deccel_vel[d]):
				c += 1
			else:
				d -= 1

		if (np.abs(self.accel_vel[c]-self.deccel_vel[d]) > 1):
			print("%d m straight is too short!",length)

		time = (self.accel_time[c]-self.accel_time[a]) + (car.deccel_time[b]-self.deccel_time[d])
		
		return time



















		
