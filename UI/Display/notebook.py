from UI.Display.GUI_Object import GUI_Object
import tkinter as tk
from tkinter import ttk


class Notebook(GUI_Object):
	frame = None
	x_pos = 0
	y_pos = 0
	notebook = None
	page_frames = []

	def __init__(self, frame):
		super().__init__(frame)
		self.page_frames = []
		self.create_object()
		self.notebook.pack()

	def object_callback(self):
		pass

	def create_object(self):
		n = ttk.Notebook(self.frame)
		self.notebook = n

	def add_pages(self, text):
		numpages = len(text)
		for i in range(numpages):
			f = ttk.Frame(self.frame)
			self.notebook.add(f, text=text[i])
			self.page_frames.append(f)

	def get_frame(self, frame_num):
		frame = self.page_frames[frame_num]
		return frame
		
	def place_object(self,x,y,height=100,width=100):
		self.notebook.grid(row=x, column=y, columnspan=6)
