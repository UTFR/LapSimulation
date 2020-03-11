import tkinter as tk
from tkinter import ttk
from tkinter import *
from GUI_Object import GUI_Object

class Dropdown(GUI_Object):
	frame = None
	x_pos = 0
	y_pos = 0

	def __init__(self, frame, options):
		super().__init__(frame)
		self.create_object(options)

	def create_object(self, options):
		default = StringVar(self.frame)
		default.set(options[0])

		menu = ttk.OptionMenu(self.frame, default, *options)
		menu.pack(side="top")
		
	def place_object(self,x,y,height=100,width=100):
		pass