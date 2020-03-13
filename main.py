from Car.car import Car
from Competitions.competition import Competition
from Competitions.michigan import Michigan


def main():
	car = Car()  # inputs tbd
	comp = Michigan(car)
	endurance_time = comp.run_endurance()
	# print(endurance_time)


if __name__ == '__main__':
	main()
