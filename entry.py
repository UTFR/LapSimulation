import tkinter as tk
from tkinter import ttk
from GUI_Object import GUI_Object

class Entry(GUI_Object):

	frame = None
	x_pos = 0
	y_pos = 0
	entry = None
	value = 0.0

	def __init__(self, frame, text='', width=10):
		super().__init__(frame)
		self.create_object(text,width)

	def create_object(self, text='', width=10):
		self.entry = ttk.Entry(self.frame,text=text, width=width)
		# self.entry.insert(0,"")
		self.entry.pack(side='left')
		self.entry.pack(side="top")
		
	def place_object(self,x,y,height=100,width=100):
		pass

	def read(self):
		if (self.entry.get() != ''):
			self.value = float(self.entry.get())
		return self.value

	def get_value(self):
		return self.value

	def set_value(self, value):
		self.value = value

	def display_val(self, val):
		self.value = val
		self.entry.insert(0,val)
