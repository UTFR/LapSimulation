import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from GUI_Object import GUI_Object
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

class Graph(GUI_Object):
	frame = None
	graph = None

	def __init__(self,frame):
		super().__init__(frame)

	def plot_2_param(self, param_x, param_y, x=2, y=3):
		fig = plt.Figure(figsize=(x,y))
		fig.add_subplot(111).plot(param_x, param_y)
		self.draw_plot(fig)

	def plot_3_param(self, param_x ,param_y, param_z, x=5, y=4):
		pass

	def draw_plot(self, fig):
		canvas = FigureCanvasTkAgg(fig, master=self.frame)  # A tk.DrawingArea.
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		toolbar = NavigationToolbar2Tk(canvas, self.frame)
		toolbar.update()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
