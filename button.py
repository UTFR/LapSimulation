import tkinter as tk
from tkinter import ttk
from GUI_Object import GUI_Object

class Button(GUI_Object):

	frame = None
	x_pos = 0
	y_pos = 0
	button = None
	text = ''
	func = None

	def __init__(self, frame, text):
		super().__init__(frame)
		self.create_object(text)
		self.button.pack()

	def __init__(self, frame, text, func):
		super().__init__(frame)
		self.func = func
		self.create_object(text)
		self.button.pack()

	def object_callback(self):
		print("pressed")

	def create_object(self, text):
		self.text = text
		if(self.func == None):
			self.button = ttk.Button(self.frame,
                   	text=text, 
                   command=self.object_callback)
		else:
			self.button = ttk.Button(self.frame,
                   	text=text, 
                   command=self.func)
		return self.button
		
	def place_object(self,x,y,height=100,width=100):
		self.button.grid(row=x, column=y, columnspan=6)