import tkinter as tk
from tkinter import *
from tkinter import ttk
from button import Button
from notebook import Notebook
from graph import Graph
from label import Label
from entry import Entry

class GUI_Manager:
	frame = None
	root = None
	label_dict = {}
	entry_dict = {}

	def __init__(self):
		self.root = tk.Tk()
		self.root.wm_title("Embedding in Tk")
		# root.geometry("500x500")
		self.frame = ttk.Frame(self.root)
		self.frame.pack()

		notebook = self.create_general_notebook()
		self.create_car_page(notebook, 0)
		self.create_design_page(notebook,1)

		self.root.mainloop()

	def create_general_notebook(self):
		n = Notebook(self.frame)
		n.add_pages(['Car','Design','Simulate','Analysis'])
		return n


	def create_car_page(self, notebook, page_num):
		frame = notebook.get_frame(page_num)
		n = Notebook(frame)
		n.add_pages(['General Data', 'Aero Data', 'Tire Data', 'Engine Data', 'Drive Train Data'])

		general_frame = n.get_frame(0)

		self.entry_dict["Mass"] = Entry(general_frame)
		self.label_dict["Mass"] = Label(general_frame, "Mass")

		self.entry_dict["Brake Bias"] = Entry(general_frame)
		self.label_dict["Brake Bias"] = Label(general_frame, "Brake Bias")

		self.entry_dict["C.O.G. Height"] = Entry(general_frame)
		self.label_dict["C.O.G. Height"] = Label(general_frame, "C.O.G. Height")

		self.entry_dict["Weight Dist."] = Entry(general_frame)
		self.label_dict["Weight Dist."] = Label(general_frame, "Weight Dist.")

		aero_frame = n.get_frame(1)

		self.entry_dict["Aero Balance"] = Entry(aero_frame)
		self.label_dict["Aero Balance"] = Label(aero_frame, "Aero Balance")

		self.entry_dict["Frontal Area"] = Entry(aero_frame)
		self.label_dict["Frontal Area"] = Label(aero_frame, "Frontal Area")

		self.entry_dict["Downforce"] = Entry(aero_frame)
		self.label_dict["Downforce"] = Label(aero_frame, "Downforce")

		self.entry_dict["Drag"] = Entry(aero_frame)
		self.label_dict["Drag"] = Label(aero_frame, "Drag")

		aero_frame = n.get_frame(2)

		self.entry_dict["Wheel Base"] = Entry(aero_frame)
		self.label_dict["Wheel Base"] = Label(aero_frame, "Wheel Base")

		self.entry_dict["Lat Tire"] = Entry(aero_frame)
		self.label_dict["Lat Tire"] = Label(aero_frame, "Lat Tire")

		self.entry_dict["Long Tire"] = Entry(aero_frame)
		self.label_dict["Long Tire"] = Label(aero_frame, "Long Tire")

		self.entry_dict["Wheel Radius"] = Entry(aero_frame)
		self.label_dict["Wheel Radius"] = Label(aero_frame, "Wheel Radius")

		aero_frame = n.get_frame(3)

		self.label_dict["Wheel Base"] = Label(aero_frame, "TBD")

		aero_frame = n.get_frame(4)

		self.label_dict["Wheel Base"] = Label(aero_frame, "TBD")


	def create_design_page(self,notebook,page_num):
		frame = notebook.get_frame(page_num)

		variable = StringVar(frame)
		variable.set("Mass") # default value

		w1 = ttk.OptionMenu(frame, variable, "Mass","Brake Bias", "C.O.G. Height", "Brake Bias", "Weight Dist.",\
			"Aero Balance","Frontal Area","Downforce","Drag","Wheel Base","Lat Tire","Long Tire","Wheel Radius")
		w1.pack()

		w2 = ttk.OptionMenu(frame, variable, "Mass","Brake Bias", "C.O.G. Height", "Brake Bias", "Weight Dist.",\
			"Aero Balance","Frontal Area","Downforce","Drag","Wheel Base","Lat Tire","Long Tire","Wheel Radius")
		w2.pack()


