# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 11:41:02 2016

@author: s0939551
"""
import Tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import ticker
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import functions as fn


class FigureFrame:
    #FigureFrame is FigureFrame()
    #interp. a class which creates frame, inside a root window, in which figures can be drawn.
    #def function_for_FigureFrame(ff):
    #   ... ff.master ; tk.Frame
    #   ... ff.Fpanel ; tk.Frame
    #   ... ff.show_figure(Figure) ; method


    def __init__(self, master):
        self.master = master
        self.Fpanel = tk.Frame(self.master) #Figure Panel, where figures are displaced
        self.Fpanel.pack(side=tk.RIGHT)
        self.canvas = None
        self.fig3d = None
        self.fig2d = None

    def show_figure(self,figure):
        #Figure -> None
        #displays a figure in the Fpanel of self.
        self.canvas = FigureCanvasTkAgg(figure, master=self.Fpanel)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#        self.master.bind("<B1-Motion>", self.camera)
        
    def clear_frames(self):
        self.Fpanel.destroy()
        self.Fpanel = tk.Frame(self.master)
        self.Fpanel.pack(side=tk.RIGHT)
        
#    def camera(self,event):
#        self.master.configure(cursor = 'crosshair')
#        self.fig3d.DDD.view_init(elev= event.y, azim= -(event.x))
#        self.canvas.show()
        
class ContourSets(dict):
    #Binds 3 lists into a dictionary of the form
    '''{0: [500, 700, 1000, 2000, 2999],
        1: [50, 209, 500, 999],
        2: [2, 3]}
    def function_for_ContourSets(cs):
        ... cs[0] ; list
        ... cs[1] ; list
        ... cs[2] ; list
    '''
    def __init__(self, data):
      contours = [sorted(set(ls)) for ls in data]
      max_z = int(round(np.nanmax(contours[-1])/10,0)*10)
      contours[-1] = range(int(round(np.nanmin(contours[-1])/10,0)*10),max_z,10)
      if contours[-1] != max_z: contours[-1].append(max_z)
      print contours
      super(ContourSets, self).__init__((num, value) for (num, value) in enumerate(list(contours)))

class Figure3D:
    #Creates a 3D figure based on data
    def __init__(self,title,labels, contours, data, colorbar = True):
        #__init__(self, String, [String*3], ContourSets, NumpyArray, Boolean)
        ##Surface 3D plot DDD
        #figure creation
        self.fig = plt.figure(figsize=(7.5, 3.6), dpi=120) #creates a figure
        self.DDD = self.fig.gca(projection='3d') # makes a 3D projection
        
        #plotting data
        self.plot(data)
        
        #Plotting contours projected in 2D
        self.add_contours(data,contours,[max(contours[0]),max(contours[1]),0])
        
        #Setting Initial limits for contours        
        self.set_axis_lims([min(contours[0]),max(contours[0])+1,min(contours[1]),max(contours[1])+1,min(contours[2]),max(contours[2])+1])
        
        ##Formatting of axes and title
        xlab,ylab,zlab = labels
        self.DDD.set_title(title)
        self.DDD.set_xlabel(xlab, fontsize=8)
        self.DDD.set_ylabel(ylab, fontsize=8)
        self.DDD.set_zlabel(zlab, fontsize=8)
        self.DDD.invert_xaxis() # invert x axis to make it easier to read
        # We change the fontsize of minor ticks label 
        self.DDD.tick_params(axis='both', which='major', labelsize=6)
        self.DDD.tick_params(axis='both', which='minor', labelsize=8)
        self.DDD.patch.set_alpha(0.5) #setting background transparency to 0.5
        
        #Adding a colorbar for the efficiency
        if colorbar: self.add_colorbar(0.8,0.05,7,zlab)
        ##end of 3D figure creation
        
    def plot(self,data):
        #Data to plot
        X,Y,Z = data
       
        #plot surface
        #vmin = np.nanmin(Z), vmax = np.nanmax(Z) needed to ignore nan values in colorbar
        self.surf = self.DDD.plot_surface(X, Y, Z, alpha=0.25,rstride=1, cstride=1, cmap=cm.coolwarm, lw = 0.5, vmin = np.nanmin(Z), vmax = np.nanmax(Z))# surface plotting
        
    def add_colorbar(self,shrink,pad,bins,zlab):
        #Adding a colorbar for the efficiency
        cb =self.fig.colorbar(self.surf,shrink=shrink, pad = pad)
        tick_locator = ticker.MaxNLocator(nbins=bins)
        cb.locator = tick_locator
        cb.update_ticks()
        
    def add_contours(self,data,contours,offsets):
        #Gca NumpyArray NumpyArray NumpyArray ContourSets [Int*3] -> None
        #add the countour to the figure
        #Plots contours projected in 2D
        X,Y,Z = data
        self.DDD.contour(X, Y, Z, contours[2], zdir='z',offset=offsets[2],  cmap=cm.coolwarm)#
        self.DDD.contour(X, Y, Z, contours[0], zdir='x',offset=offsets[0],  cmap=cm.winter)#
        self.DDD.contour(X, Y, Z, contours[1], zdir='y',offset=offsets[1],  cmap=cm.winter)#
        
    def set_axis_lims(self,limits):
        #Gca [xmin,xmax,ymin,ymax,zmin,zmax] -> None
        #Sets the limits of the 3 axis, x,y and z
        xmin,xmax,ymin,ymax,zmin,zmax = limits
        self.DDD.set_xlim(xmin, xmax)
        self.DDD.set_ylim(ymin, ymax)
        self.DDD.set_zlim(zmin, zmax)
        
class Figure3D_Extrapolated:
    #Creates a 3D figure based on data
    def __init__(self,title,labels, contours, data, data_extrapolated, colorbar = True):
        #__init__(self, String, [String*3], ContourSets, NumpyArray, Boolean)
        ##Surface 3D plot DDD
        #figure creation
        self.fig = plt.figure(figsize=(7.5, 3.6), dpi=120) #creates a figure
        self.DDD = self.fig.gca(projection='3d') # makes a 3D projection
        
        #plotting extrapolated data
        self.plot(data_extrapolated,0.25)        
        
        #plotting data unextrapolated data
        self.plot(data,1)
        
        #Plotting contours projected in 2D
        self.add_contours(data,contours,[max(contours[0]),max(contours[1]),0])
        
        #Setting Initial limits for axis
        X,Y,Z = data_extrapolated
        X = [item for sublist in X.tolist() for item in sublist]
        Y = [item for sublist in Y.tolist() for item in sublist]
        Z = [item for sublist in Z.tolist() for item in sublist]
        self.set_axis_lims([min(X),max(X)+fn.get_1percent(max(X)),min(Y),max(Y)+fn.get_1percent(max(Y)),min(Z),max(Z)+fn.get_1percent(max(Z))])
        
        ##Formatting of axes and title
        xlab,ylab,zlab = labels
        self.DDD.set_title(title)
        self.DDD.set_xlabel(xlab, fontsize=8)
        self.DDD.set_ylabel(ylab, fontsize=8)
        self.DDD.set_zlabel(zlab, fontsize=8)
        self.DDD.invert_xaxis() # invert x axis to make it easier to read
        # We change the fontsize of minor ticks label 
        self.DDD.tick_params(axis='both', which='major', labelsize=6)
        self.DDD.tick_params(axis='both', which='minor', labelsize=8)
        self.DDD.patch.set_alpha(0.5) #setting background transparency to 0.5
        
        #Adding a colorbar for the efficiency
        if colorbar: self.add_colorbar(0.8,0.05,7,zlab)
        ##end of 3D figure creation
        
    def plot(self,data, alpha):
        #Data to plot
        X,Y,Z = data
       
        #plot surface
        #vmin = np.nanmin(Z), vmax = np.nanmax(Z) needed to ignore nan values in colorbar
        self.surf = self.DDD.plot_surface(X, Y, Z, alpha = alpha,rstride=1, cstride=1, cmap=cm.coolwarm, lw = 0.5, vmin = np.nanmin(Z), vmax = np.nanmax(Z))# surface plotting
        
    def add_colorbar(self,shrink,pad,bins,zlab):
        #Adding a colorbar for the efficiency
        cb =self.fig.colorbar(self.surf,shrink=shrink, pad = pad)
        tick_locator = ticker.MaxNLocator(nbins=bins)
        cb.locator = tick_locator
        cb.update_ticks()
        
    def add_contours(self,data,contours,offsets):
        #Gca NumpyArray NumpyArray NumpyArray ContourSets [Int*3] -> None
        #add the countour to the figure
        #Plots contours projected in 2D
        X,Y,Z = data
        self.DDD.contour(X, Y, Z, contours[2], zdir='z',offset=offsets[2],  cmap=cm.coolwarm)#
        self.DDD.contour(X, Y, Z, contours[0], zdir='x',offset=offsets[0],  cmap=cm.winter)#
        self.DDD.contour(X, Y, Z, contours[1], zdir='y',offset=offsets[1],  cmap=cm.winter)#
        
    def set_axis_lims(self,limits):
        #Gca [xmin,xmax,ymin,ymax,zmin,zmax] -> None
        #Sets the limits of the 3 axis, x,y and z
        xmin,xmax,ymin,ymax,zmin,zmax = limits
        self.DDD.set_xlim(xmin, xmax)
        self.DDD.set_ylim(ymin, ymax)
        self.DDD.set_zlim(zmin, zmax)
        
    
            
class Figure2D:
    #Creates a 3D figure based on data
    def __init__(self,title,labels, data, colorbar = True):
        #__init__(self, String, [String*3], [NumpyArray*3], Boolean)
        #figure creation
        ##2D plot of the data as: DD
        
        #Figure text
        xlab,ylab,zlab = labels

        #Figure creation
        self.fig = plt.figure(figsize=(7.5, 3.6), dpi=120)
        self.DD = self.fig.add_subplot(111)
        #projected fill contours to show the efficiency as a 2D color surface
        cDD = self.plot(data)
        #adding a colourbar
        cbar = self.fig.colorbar(cDD)
        cbar.set_label(zlab)
        
        #Formatting of the 2D figure and titles
        self.DD.set_title(title)
        self.DD.set_xlabel(xlab, fontsize=8)
        self.DD.set_ylabel(ylab, fontsize=8)
        
    def plot(self,data):
        X,Y,Z = data
        return self.DD.contourf(X, Y, Z, cmap=cm.coolwarm)
        
class Figure2D_Extrapolated:
    #Creates a 3D figure based on data
    def __init__(self,title,labels, data, data_extrapolated, colorbar = True):
        #__init__(self, String, [String*3], [NumpyArray*3], Boolean)
        #figure creation
        ##2D plot of the data as: DD
        
        #Figure text
        xlab,ylab,zlab = labels

        #Figure creation
        self.fig = plt.figure(figsize=(7.5, 3.6), dpi=120)
        self.DD = self.fig.add_subplot(111)
        #projected fill contours to show the efficiency as a 2D color surface
        #plot extrapolated data
        self.plot(data_extrapolated, 0.5)
        #plot normal data
        cDD = self.plot(data, 1)

        #adding a colourbar
        cbar = self.fig.colorbar(cDD)
        cbar.set_label(zlab)
        
        #Formatting of the 2D figure and titles
        self.DD.set_title(title)
        self.DD.set_xlabel(xlab, fontsize=8)
        self.DD.set_ylabel(ylab, fontsize=8)
        
    def plot(self,data,alpha):
        X,Y,Z = data
        return self.DD.contourf(X, Y, Z, cmap=cm.coolwarm, alpha = alpha)


