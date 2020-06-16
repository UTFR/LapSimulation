from car import Car
from car_calculations import Car_Calc
from competition import Competition
from michigan import Michigan

def main():
	#car = Car()
	car = Car_Calc() #inputs tbd
	comp = Michigan(car)
	endurance_time = comp.run_endurance()
	# print(endurance_time)



if __name__ == '__main__':
	main()