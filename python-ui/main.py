import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
import matplotlib
matplotlib.use("Agg")

def main():
	ui = UI()
	ui.run()

class UI:
	def __init__(self) -> None:
		self.root = tk.Tk()
		self.label = tk.Label(text="Realtime graph test")
		self.label.pack()
		self.fig = plt.figure(figsize=(10, 5), dpi=100)

		self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
		self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		plt.grid("both")
		style.use("ggplot")

		self.ax1 = plt.subplot(111)
		self.line1, = self.ax1.plot([0], [0])

		self.data_x = [0]
		self.data_y = [0]

	def run(self):
		self.update_plot()
		self.root.mainloop()
	

# function to update ploat
	def update_plot(self):
		data_y = get_data() 
		self.data_y.append(self.data_y[-1] + data_y)
		self.data_x.append(self.data_x[-1] + 1)
		if len(self.data_x) >= 101:
			self.data_x = self.data_x[1:]
		if len(self.data_y) >= 101:
			self.data_y = self.data_y[1:]
		print("x", end="")
		print(self.data_x)
		print("y", end="")
		print(self.data_y)
		self.line1.set_xdata(self.data_x)
		self.line1.set_ydata(self.data_y)
		self.ax1.set_ylim([min(self.data_y), max(self.data_y)])
		self.ax1.set_xlim([self.data_x[0],self.data_x[0] + 100])
		plt.grid("both")
		self.canvas.draw()
		self.canvas.flush_events()
        # update plot again after 10ms. You can change the delay to whatever you want
		self.root.after(10, self.update_plot)
	
def get_data():
	return random.choice([-0.1, 0.1])


if __name__ == "__main__":
	main()
