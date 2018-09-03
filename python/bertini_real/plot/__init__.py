#Nicolle Ho
#University of Notre Dame
#Spring 2017

# Danielle Brake
# Fall 2018

import os
from bertini_real.brdata import BRData
from bertini_real.surface import Surface, Curve
import bertini_real.util
import dill
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



class Options(object):
	def __init__(self):
		self.option1 = "value1"



class Plotter(object):


	def __init__(self, data = None, options = Options()):

		if data is None:
			self.ReadMostRecent()
		else:
			self.decomposition = data

		self.options = options



	def plot(self):

		print("plotting object of dimension " + str(self.decomposition.dimension))
		
		self.make_figure()
		self.make_axes()
			

		# this should be conditionally done based on some flag
		self.PlotVertices()

		if self.decomposition.dimension == 1:
			self.PlotCurve(self.decomposition)
		elif self.decomposition.dimension == 2:
			self.Plotsurface(self.decomposition)

		self.label_axes()
		self.apply_title()


		plt.show()




	def make_figure(self):
		self.fig = plt.figure()




	def make_axes(self):
		if self.decomposition.num_variables==2:
			self.ax = self.fig.add_subplot(111)
		else:
			self.ax = self.fig.add_subplot(111, projection='3d')



	def apply_title(self):
		plt.title(os.getcwd().split(os.sep)[-1])



	def label_axes(self):
		#todo: these should be set from the decomposition, not assumed to be x,y,z
		self.ax.set_xlabel("x")
		self.ax.set_ylabel("y")
		if self.decomposition.dimension is 2:
			self.ax.set_zlabel("z")

		




	def ReadMostRecent(self):
		filenum = bertini_real.util.highest_filenumber()

		fileName = "BRdata" + str(filenum) + ".pkl"

		print("reading from file " + fileName)

		fileObject = open(fileName,'rb')
		self.decomposition = dill.load(fileObject)
		fileObject.close()


	'''
	renders all vertices

	todo: make them colored based on a function
	'''
	def PlotVertices(self):

		xs = []
		ys = []
		zs = []

		for v in self.decomposition.vertices:
			xs.append(v['point'][0].real)
			ys.append(v['point'][1].real)

			if self.decomposition.num_variables>2:
				zs.append(v['point'][2].real)


		if self.decomposition.num_variables==2:
			self.ax.scatter(xs, ys)#v['point'][
		else:
			self.ax.scatter(xs, ys, zs, zdir='z', s=5, c=None, depthshade=True)#v['point'][

	def PlotCurve(self, curve):
		num_nondegen_edges=0
		nondegen=[]
		for i in range(curve.curve.num_edges):
			e=curve.curve.edges[i]
			if e[0]!=e[1]!=e[2]:
				num_nondegen_edges=num_nondegen_edges+1
				nondegen.append(i)

		colormap = plt.cm.inferno
		color_list=([colormap(i) for i in np.linspace(0, 1,num_nondegen_edges)])

		for i in range(num_nondegen_edges):
			color=color_list[i]
			self.PlotEdge(curve,nondegen[i],color)

	def PlotEdge(self, curve, edge_index,color):

		xs=[]
		ys=[]
		zs=[]

		inds = self.decomposition.curve.sampler_data[edge_index]
		for i in inds:
			v = self.decomposition.vertices[i]
			xs.append(v['point'][0].real)
			ys.append(v['point'][1].real)
			if self.decomposition.num_variables>2:
				zs.append(v['point'][2].real)

		if self.decomposition.num_variables==2:
			self.ax.plot(xs, ys, c=color)#v['point'][
		else:
			self.ax.plot(xs, ys, zs, zdir='z', c=color)#v['point']


	def Plotsurface(self, surf):
		print("Plotsurface unimplemented yet.")






def plot(data = None):

	b = Plotter(data)
	b.plot();
	return b




