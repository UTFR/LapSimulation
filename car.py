import constants as c
import numpy as np
from bisect import bisect_left
import math
from car_helpers import *
import pdb;

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
	final_ratios = []

	step_size = 0.01
	shift_speeds = [0,0,0,0,math.inf] #math.inf is for bisect_left
	accel_vel = [] #figure out what to do with this?
	deccel_vel = [] #figure out what to do with this?
	accel_dist = [] #figure out what to do with this?
	accel_time = [] #figure out what to do with this?
	deccel_time = [] #figure out what to do with this?
	deccel_dist = []

	def __init__(self):
		print("hi")
		self.final_ratios()
		self.shift_speed(10000)
		print("shift_speeds", self.shift_speeds)
		# pdb.set_trace()

		accel_dist, time_out_accel, velo_out_accel, accel_out, _ = self.accelerate()
		decel_dist, time_out_decel, velo_out_decel, accel_out, _, _, _, _ = self.decelerate()

		self.accel_vel = velo_out_accel
		self.deccel_vel = velo_out_decel
		self.accel_dist = accel_dist
		self.accel_time = time_out_accel
		self.deccel_time = time_out_decel
		self.deccel_dist = decel_dist

	def set_weight_dist(self, weight_dist):
		self.weight_dist = weight_dist

	def get_weight_dist(self, weight_dist):
		return self.weight_dist

	def set_cog_height(self, cog_height):
		self.cog_height = cog_height

	def get_cog_height(self, cog_height):
		return self.cog_height

	def set_wheel_base(self, wheel_base):
		self.wheel_base = wheel_base

	def get_wheel_base(self):
		return self.wheel_base

	def set_frontal_area(self, frontal_area):
		self.frontal_area = frontal_area

	def get_frontal_area(self):
		return self.frontal_area

	def set_mass(self, mass):
		self.mass = mass

	def get_mass(self):
		return self.mass

	def set_lat_tire(self, lat_tire):
		self.lat_tire = lat_tire

	def get_lat_tire(self):
		return self.lat_tire

	def set_long_tire(self, long_tire):
		self.long_tire = long_tire

	def get_long_tire(self):
		return self.long_tire

	def set_wheel_radius(self, wheel_radius):
		self.wheel_radius = wheel_radius

	def get_wheel_radius(self):
		return wheel_radius

	def set_aero_balance(self, aero_balance):
		self.aero_balance = aero_balance

	def get_aero_balance(self):
		return aero_balance

	def set_brake_bias(self, brake_bias):
		self.brake_bias = brake_bias

	def get_brake_bias(self):
		return brake_bias

	def shift_gears(self, rpm):
		index = TORQUE_CURVE[0].index(rpm)
		TORQUE_CURVE[1].index

	def final_ratios(self):
		self.final_ratios = np.zeros(len(c.GEAR_RATIOS))
		for i in range(len(self.final_ratios)):
			self.final_ratios[i] = c.GEAR_RATIOS[i]*c.GEAR_RATIOS[-1]

	def rpm_to_rad_s(self, rpm):
		return rpm*(np.pi)/30

	def rad_s_to_rpm(self, rad_s):
		return rad_s*30/np.pi

	def shift_speed(self,shift_rpm):
		for i in range(len(self.shift_speeds)-1):
			#print(self.wheel_radius,self.final_ratios[i])
			shift = self.rpm_to_rad_s(shift_rpm)*self.wheel_radius/self.final_ratios[i]
			self.shift_speeds[i] = shift

	def linear_interpolation(self,torque_index,car_rpm):
		torque_low = c.TORQUE_CURVE[1][torque_index-1]
		torque_high = c.TORQUE_CURVE[1][torque_index+1]
		return ((torque_high-torque_low)/500)*(car_rpm-c.TORQUE_CURVE[1][torque_index-1]) + torque_low

	def calc_cl(self, downforce):
		print("============================", 0.5*c.AIR_DENSITY*downforce*self.frontal_area)
		print(downforce)
		return 0.5*c.AIR_DENSITY*downforce*self.frontal_area

	def calc_cd(self, drag):
		return 0.5*c.AIR_DENSITY*drag*self.frontal_area

	def accelerate(self):
		#init variables
		velo = 0
		accel = 0
		index = 0
		torque = 0
		gear = 0
		weight_transfer = 0
		force_applied = 0
		distance = []

		velo_out = []
		time_out = []
		force_e_out = []
		accel_out = []

		#calculate the min/max velocity car can reach
		min_velocity = self.rpm_to_rad_s(3000)*self.wheel_radius/self.final_ratios[0]
		max_gear_velocity = self.rpm_to_rad_s(10500)*self.wheel_radius/self.final_ratios[4]

		#is car stil accelerating/can still accelerate?
		while (accel >= 0 and (velo < max_gear_velocity)):
			#get the torque and gear number depending on rpm
			if (velo < min_velocity):
				#first gear
				torque = c.TORQUE_CURVE[1][0]
				gear = self.final_ratios[0]
			else:
				wheel_rpm = self.rad_s_to_rpm(velo/self.wheel_radius)
				#pick gear based on which range wheel_rpm is in
				gear_index = bisect_left(self.shift_speeds, velo)
				gear = self.shift_speeds[gear_index] #check if fancy schmancy bisect_left func works
				#car_rpm is rpm after shifting gears
				car_rpm = wheel_rpm*gear
				#print(car_rpm)
				#print("hi")
				#print(c.TORQUE_CURVE[0])
				#get torque
				torque_index = bisect_left(c.TORQUE_CURVE[0], car_rpm) #this line is questionable at best
				#print(torque_index)
				if (car_rpm == c.TORQUE_CURVE[0][torque_index]):
					torque = c.TORQUE_CURVE[1][torque_index]
				else:
					torque = self.linear_interpolation(torque_index,car_rpm)
			#get weight transfer
			if (velo == 0):
				weight_transfer = 0
			else:
				weight_transfer = accel*self.mass*c.GRAVITY*self.cog_height/self.wheel_base

			downforce = c.LIFT_COEF*velo**2 #check this
			drag = c.CD*velo**2
			force_e = torque*gear/self.wheel_radius
			force_n = (self.mass/2)*c.GRAVITY + weight_transfer + downforce/2 #tf is this?
			force_tire_max = force_n*self.long_tire

			#determine if wheel is gripping road
			if (force_e > force_tire_max):
				force_applied = force_tire_max
				print("spinning")
			else:
				force_applied = force_e

			#save + update values
			new_accel = (force_applied-drag)/self.mass
			distance.append(self.step_size*index) #what?
			if (index == 0):
				velo_out.append(0)
				time_out.append(0)
			else:
				vel_final = np.sqrt(velo**2 + 2*new_accel*self.step_size)
				time_out.append((vel_final - velo)/new_accel + time_out[index-1])
				velo_out.append(vel_final*3.6) #<-- 3.6 is converting from m/s to km/h
				velo = vel_final

			force_e_out.append(force_e)
			accel_out.append(new_accel/c.GRAVITY)
			accel = new_accel

			index += 1

		return distance, time_out, velo_out, accel_out, force_e_out


	def decelerate(self):
		velo = self.rpm_to_rad_s(10500)*self.wheel_radius/self.final_ratios[4]
		print("velo", velo)
		index = 0

		static_mass_fr = self.mass*self.weight_dist
		static_mass_r = self.mass-static_mass_fr
		accel = 2*c.GRAVITY
		#print("static_mass_r", static_mass_r)

		cl = self.calc_cl(c.LIFT_COEF)
		cd = self.calc_cd(c.CD)

		accel_out = []
		velo_out = []
		time_out = []
		weight_transfer_out = []
		force_rear_out = []
		force_front_out = []
		brake_bias_ideal = []
		distance = []

		while (velo > 0):
			downforce = cl*velo**2
			drag = cd*velo**2
			print("downforce", downforce, velo, cl)
			#print("downorce, drag", downforce, drag, velo)
			#pdb.set_trace()

			mass_transfer = (accel*self.mass*self.cog_height)/self.wheel_base
			weight_transfer = mass_transfer*c.GRAVITY
			# print("statss")
			# print(mass_transfer, weight_transfer)
			# pdb.set_trace()

			print("vars", static_mass_fr, weight_transfer, downforce, self.weight_dist)
			#tf is going on here
			f_norm_front_max = c.GRAVITY*static_mass_fr + weight_transfer + downforce*self.weight_dist
			f_norm_rear_max = c.GRAVITY*static_mass_r - weight_transfer + downforce*(1-self.weight_dist) #note: this is (-)

			print("front, rear", f_norm_front_max, f_norm_rear_max)
			# pdb.set_trace()

			f_front = f_norm_front_max*self.long_tire
			f_rear = f_norm_rear_max*self.long_tire

			# print("front, rear", f_front, f_rear)
			# pdb.set_trace()

			f_app_brakes = self.mass*accel
			f_app_front = f_app_brakes*self.brake_bias
			f_app_rear = f_app_brakes*(1-self.brake_bias)

			# print(f_app_brakes, f_app_front, f_app_rear)
			# pdb.set_trace()

			while(f_app_front > f_front or f_app_rear > f_rear):
				accel -= 0.01
				mass_transfer = accel*self.mass*self.cog_height/self.wheel_base
				weight_transfer = mass_transfer*c.GRAVITY
				f_norm_front = c.GRAVITY*static_mass_fr + weight_transfer + downforce*self.weight_dist
				f_norm_rear = c.GRAVITY*static_mass_r - weight_transfer + downforce*(1-self.weight_dist)

				# print("hello", mass_transfer, weight_transfer, f_norm_front, f_norm_rear)
				# pdb.set_trace()

				f_front = f_norm_front*self.long_tire
				f_rear = f_norm_rear*self.long_tire
				f_app_brakes = self.mass*accel
				f_app_front = f_app_brakes*self.brake_bias
				f_app_rear = f_app_brakes*(1-self.brake_bias)
				#print("wheels locking")

				# print("hello", f_front, f_rear, f_app_brakes, f_app_front, f_app_rear)
				# pdb.set_trace()

			accel = f_app_brakes/self.mass
			accel_true = accel+(drag/self.mass)

			# print("hello", velo, accel, accel_true)
			# pdb.set_trace()

			print("before", velo**2 - 2*accel_true*self.step_size)
			vel_new = np.sqrt(velo**2 - 2*accel_true*self.step_size)
			print("vel_new", vel_new)
			time = np.abs(vel_new-velo)/accel_true
			distance.append(self.step_size*index)

			# print("hello", vel_new, time)
			# pdb.set_trace()

			if(index == 0):
				velo_out.append(velo)
				time_out.append(0)
			else:
				time_out.append(time_out[index-1] + time)
				velo_out.append(3.6*np.abs(vel_new))

			accel_out.append(accel_true/c.GRAVITY)
			weight_transfer_out.append(mass_transfer)
			force_rear_out.append(f_app_rear)
			force_front_out.append(f_app_front)
			brake_bias_ideal.append(f_front/(f_front+f_rear))
			velo = vel_new
			index += 1

		print("stats")
		print(distance)
		# #println(time_out)
		# #println(velo_out)
		# #println(accel_out)
		# #println(weight_transfer_out)
		# #println(force_rear_out)
		# #println(force_front_out)
		# #println(brake_bias_ideal)

		# pdb.set_trace()

		return distance, time_out, velo_out, accel_out, weight_transfer_out, force_rear_out, force_front_out, brake_bias_ideal

	def corner_calc(self, radius, corner_len):
		new_accel = 1
		error = 1;
		max_velo = self.rpm_to_rad_s(c.TORQUE_CURVE[1][-1])*self.wheel_radius/self.final_ratios[-2]

		while(error > 0.001):
			accel = new_accel
			velo = np.sqrt(accel*self.wheel_radius)
			if(velo > max_velo):
				velo = max_velo
				break
			else:
				downforce = c.LIFT_COEF*velo**2 #double check this
				lat_force = (self.mass*c.F_G + downforce)*self.lat_tire
				new_accel = lat_force/self.mass
				error = np.absolute(new_accel - accel)

		if (velo == max_velo):
			time = corner_len/velo
		else:
			velo = np.sqrt(new_accel*self.radius)
			time = corner_len/velo

		return time, velo

	def straight_calc(self, length, velo_in, velo_out):
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

		time = (self.accel_time[c]-self.accel_time[a]) + (self.deccel_time[b]-self.deccel_time[d])
		
		return time



















		
