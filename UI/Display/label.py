import tkinter as tk
from tkinter import ttk
from UI.Display.GUI_Object import GUI_Object


class Label(GUI_Object):

	frame = None
	x_pos = 0
	y_pos = 0
	label = None

	def __init__(self, frame, text):
		super().__init__(frame)
		self.create_object(text)

	def object_callback(self):
		print("pressed")

	def create_object(self, text):
		self.label = ttk.Label(self.frame, text=text)
		self.label.pack(side="left")
		self.label.pack(side="bottom")
		
	def place_object(self, x, y, height=100, width=100):
		pass
