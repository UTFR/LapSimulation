


def rpm_to_rad_s(self, rpm):
		return rpm*(np.pi)/30

def rad_s_to_rpm(self, rad_s):
	return rad_s*30/np.pi

def wheel_linear_velocity(radius,angular_v):
	return radius*angular_v

def wheel_angular_velocity(radius,linear_v):
	return rad_s_to_rpm(linear_v/radius)

def torque_from_car_rpm(car_rpm):
	torque_index = bisect_left(c.TORQUE_CURVE, car_rpm)
	if (car_rpm == c.TORQUE_CURVE[0][torque_index]):
		torque = c.TORQUE_CURVE[1][torque_index]
	else:
		linear_interpolation(torque_index,car_rpm)

def linear_interpolation(torque_index,car_rpm):
	torque_low = c.TORQUE_CURVE[1][torque_index-1]
	torque_high = c.TORQUE_CURVE[1][torque_index+1]
	return ((torque_high-torque_low)/500)*(car_rpm-c.TORQUE_CURVE[1][torque_index-1]) + torque_low

def calc_downforce(velocity): #check this
	return 0.5*c.LIFT_COEF*c.CHORD*c.WING_SPAN*c.AIR_DENSITY*velocity**2

def calc_weight_transfer(accel):
	if (velo == 0):
		return 0
	else:
		return accel*self.mass*c.GRAVITY*self.cog_height/self.wheel_base


