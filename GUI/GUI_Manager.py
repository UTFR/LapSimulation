import tkinter as tk
class GUI_Manager:

	root = tk.Tk()
	frame = tk.Frame(root)
	frame.pack()

	def button_callback():
		print("pressed")

	def create_button(text):
		button = tk.Button(frame, 
                   text=text, 
                   fg="red",
                   command=button_callback)
		
	def place_button(x,y,height=100,width=100):
		