

class Data_Collection:
	track_len = 0
	data_corner = []
	data_straight = []


	def __init__(self, car, comp):
		self.data_corner = comp.data_corner
		self.data_straight = comp.data_straight
		self.track_len = sum(self.data_corner[1]) + sum(self.data_straight[1])

	def track_velocity(vel_arr, corner_arr):
		vel_arr = []
		for i in range(track_len):
			if (i%2 == 0):
				vel_arr = vel_arr + corner_arr
			else:
				vel_arr = vel_arr + straight_arr
		return vel_arr
