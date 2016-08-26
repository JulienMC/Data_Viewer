# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 15:57:29 2016

@author: s0939551
"""

import Tkinter as tk
import numpy as np
import functions as fn
import figure_classes as fc
import user_handler as uh
import time
from matplotlib.mlab import griddata
import os

##setting up root window and frames

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.figureframe = fc.FigureFrame(self)
        self.userinputmanager = uh.UserInputManager(self)
        self.timer = Timer(self)
        
        self.fullscreen()
        
##        self.statusbar = Statusbar(self, ...)
##        self.toolbar = Toolbar(self, ...)
##        self.navbar = Navbar(self, ...)
##        self.main = Main(self, ...)
#
#        self.statusbar.pack(side="bottom", fill="x")
#        self.toolbar.pack(side="top", fill="x")
#        self.navbar.pack(side="left", fill="y")
#        self.main.pack(side="right", fill="both", expand=True)
        
        file_dat = fn.file_extract('M:/MyDocuments/DataSets/Isentropic_Efficiency_Summary_SA.csv',
                                    ['Depth','Perm','Avg. RT Eff. (%)'],
                                     {'Poro':15,
                                      'Thick':350,
                                      'Compressor Isentropic Efficiency': 0.66,
                                      'Compression Stages':2.0,
                                      'Turbine Isentropic Efficiency':0.66})
        contours = fc.ContourSets(file_dat)
        data = Data(file_dat)
        data_extrapolated = Data(file_dat, True)
        
        self.figureframe.fig3d = fc.Figure3D_Extrapolated('CAES-PM Efficiency against Depth and Permeability',['Depth (m)','Permeability (md)','Avg. RT Eff. (%)'],contours,data,data_extrapolated,True)
        self.figureframe.show_figure(self.figureframe.fig3d.fig)
        
        self.figureframe.fig2d = fc.Figure2D_Extrapolated('CAES-PM Efficiency against Depth and Permeability',['Depth (m)','Permeability (md)','Avg. RT Eff. (%)'],data, data_extrapolated,True)
        self.figureframe.show_figure(self.figureframe.fig2d.fig)

        self.updates()
        
    def initiate_figures(self,filename, to_plot, dico):
        '''   MainApplication,String,[3*String],[Numbers or '-'] -> None
        extracts data and calls the figureframe methods to plot the figures'''
        self.figureframe.clear_frames()
        file_dat = fn.file_extract(filename, to_plot, dico)
        contours = fc.ContourSets(file_dat)
        #getting file_dat data ready to be fed into the Figure() instances
        data = Data(file_dat)
        data_extrapolated = Data(file_dat, True)
        print 'DATA',data
        print 'EXTRAPOLATED', data_extrapolated
        self.figureframe.fig3d = fc.Figure3D_Extrapolated('CAES-PM {} against {} and {}'.format(to_plot[2],to_plot[0],to_plot[1]),[to_plot[0],to_plot[1],to_plot[2]],contours, data, data_extrapolated,True)
        self.figureframe.show_figure(self.figureframe.fig3d.fig)
        self.figureframe.fig2d = fc.Figure2D_Extrapolated('CAES-PM {} against {} and {}'.format(to_plot[2],to_plot[0],to_plot[1]),[to_plot[0],to_plot[1],to_plot[2]], data, data_extrapolated,True)
        self.figureframe.show_figure(self.figureframe.fig2d.fig)
        
    def updates(self):
        self.userinputmanager.update()
        
    def fullscreen(self):
        self._geom='200x200+0+0'
        self.parent.geometry("{0}x{1}+0+0".format(
            self.parent.winfo_screenwidth()-20, self.parent.winfo_screenheight()-100))
        self.parent.bind('<Escape>',self.toggle_geom)

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
        
class Timer():
    def __init__(self,master):
        self.master = master
#        self.label = tk.Label(text="")
#        self.label.pack()
        self.update_clock()

    def update_clock(self):
#        now = time.strftime("%H:%M:%S")
#        self.label.configure(text=now)
        self.master.after(1000, self.update_clock)
        self.master.updates()

        
class Data(list):
    # Data is Data(FileData)
    # interp. takes in a list containing three nested lists representing X,Y,Z data to plot
    # and returns a list of three 1D arrays with X,Y,Z values in the ascending order.
    # def function_for_data(d):
    #    ... d[0] ; np.array
    #    ... d[1] ; np.array
    #    ... d[2] ; np.array

    ''' Takes a list of input in the form [[x1,x2,...,xn],[y1,y2,...,yn],[z1,z2,...,zn]] and stores
        three numpy arrays.
        the lenght of all arrays are len(set([x1,x2,...,xn]))
        
        example:
        X = np.array([[500,700,1000,2000,3000],[500,700,1000,2000,3000],[500,700,1000,2000,3000],[500,700,1000,2000,3000]])
        Y = np.array([[50,50,50,50,50],[209,209,209,209,209],[500,500,500,500,500],[1000,1000,1000,1000,1000]])
        Z = np.array([[0,0,33,64,71],[44,62,69,74,76],[59,67,72,75,77],[63,68,73,76,77]])
    '''
    def __init__(self,inputs, extrapolation = False, new_type = False):
        x_input_list,y_input_list,z_input_list = inputs
        print 'x',x_input_list
        print 'y',y_input_list
        print 'z',z_input_list        
        
        self.append(fn.x_array(x_input_list,y_input_list))# np.array([sorted(set(x_input_list)) for n in range(len(set(y_input_list)))]))
        self.append(fn.y_array(y_input_list,x_input_list) )# np.array([[n]*len(set(x_input_list)) for n in sorted(set(y_input_list))]))
        self.append(np.array([c for c in fn.chunks(z_input_list,len(set(x_input_list)))]))
      
        if extrapolation: fn.extrapolate_array(self[2])
        
        # increase number of contours. not working yet
        if new_type:
            x = [item for sublist in self[0].tolist() for item in sublist]
            y = [item for sublist in self[1].tolist() for item in sublist]
            z = [item for sublist in self[2].tolist() for item in sublist]
            self[0],self[1],self[2] = fn.interpolation([x,y,z])
            
def resize(event):
    print("New size is: {}x{}".format(event.width, event.height))
        
if __name__ == "__main__":
    #setting up main window        
    root = tk.Tk()
#    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#    root.geometry("%dx%d+0+0" % (w-20, h-100))
#    root.bind("<Configure>", resize)
    #launching application
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    


    
