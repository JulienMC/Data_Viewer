# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:39:58 2016

@author: s0939551
"""

from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
import functions as fn

file_dat = fn.file_extract('M:/MyDocuments/DataSets/Isentropic_Efficiency_Summary_SA.csv',
                            ['Depth','Perm','Avg. RT Eff. (%)'],
                             {'Poro':15,
                              'Thick':350,
                              'Compressor Isentropic Efficiency': 0.66,
                              'Compression Stages':2.0,
                              'Turbine Isentropic Efficiency':0.66})
# make up data.
#npts = int(raw_input('enter # of random points to plot:'))
seed(0)
npts = 200
x = uniform(-2, 2, npts)
y = uniform(-2, 2, npts)
z = x*np.exp(-x**2 - y**2)
#print file_dat
x,y,z = file_dat
# define grid.
#xi = np.linspace(-2.1, 2.1, 10)
#yi = np.linspace(-2.1, 2.1, 10)
print 'filedata',file_dat

xi = np.linspace(min(x), max(x), 100)
yi = np.linspace(min(y), max(y), 100)

# grid the data.
zi = griddata(x, y, z, xi, yi, interp='linear')
# contour the gridded data, plotting dots at the nonuniform data points.
CS = plt.contour(xi, yi, zi, 20, linewidths=0.5)
CS = plt.contourf(xi, yi, zi, 20, cmap=plt.cm.rainbow,
                  vmax=abs(zi).max(), vmin=abs(zi).min(),rasterized=False)
plt.colorbar()  # draw colorbar
# plot data points.
plt.scatter(x, y, marker='o', c='b', s=10, zorder=10)
plt.xlim(min(x), max(x))
plt.ylim(min(y), max(y))
plt.title('griddata test (%d points)' % npts)
plt.show()

import pandas as pd
z_interp = pd.DataFrame(z).interpolate(method='linear', axis=0).values
print zi,z_interp

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
    def __init__(self,inputs):
        x_input_list,y_input_list,z_input_list = inputs
        self.append(np.array([sorted(set(x_input_list), key=int) for n in range(len(set(y_input_list)))]))
        self.append(np.array([[n]*len(set(x_input_list)) for n in sorted(set(y_input_list), key=int)]))
        self.append(np.array([c for c in fn.chunks(z_input_list,len(set(x_input_list)))]))
        #self.interpolation(inputs)
        print self[2]
        self[2] = pd.DataFrame(self[2]).interpolate(method='linear', axis=0).values
        print self[2]
        
    def interpolation(self,data):
        x,y,z = data
        xi,yi = np.linspace(min(x),max(x),10),np.linspace(min(y),max(y),10)
        zi = griddata(x,y,z,xi,yi,interp='linear')
        return xi,yi,zi

plt.contourf(x, y, z_interp, 20, cmap=plt.cm.rainbow,
                  vmax=abs(z_interp).max(), vmin=abs(z_interp).min(),rasterized=False)
plt.show()


a = np.array([[np.nan,42.7,43.3,46.1],[np.nan,44,44.6,np.nan],[42.1,44,45,46.2]])

#quad for c1 r1

import check

def crop_array(array,c,r):
    ''' np.array int int -> np.array
        crops the array passed in a 3x3 array
        centered on the value located at column
        c and row r of the original array
        
        checks:
        a = np.array([[np.nan,42.7,43.3,46.1],[np.nan,44,44.6,np.nan],[42.1,44,45,46.2]])
        b = a = np.array([[np.nan,42.7,43.3],[np.nan,44,44.6],[42.1,44,45]])
        check.expect('crop_array',crop_array(a,1,1),b)'''
    #get lenght and height of array
    row_nb, col_nb = len(array),len(array[0])
    #check if c and r are at the edges and calculates array accordingly
    if r == 0:
        selected_rows = array.tolist()[r:r+2]
    elif r == row_nb:
        selected_rows = array.tolist()[r-1:r+1]
    else:
        selected_rows = array.tolist()[r-1:r+2]
        
    if c == 0:
        cropped_array = np.array([[row[c],row[c+1]] for row in selected_rows])
    elif c == col_nb-1:
        cropped_array = np.array([[row[c-1],row[c]] for row in selected_rows])
    else:
        cropped_array = np.array([[row[c-1],row[c],row[c+1]] for row in selected_rows])
    print cropped_array    
    return cropped_array

def avg_array(array):
    ''' np.array -> float
        takes an array and averages all the values from it and returns that
        value as a float. /!\ does not take into account any 0 from the original array
    '''

    #makes all nan values 0.0
    zero_list = np.array([0 if np.isnan(val) else val for val in [item for sublist in array.tolist() for item in sublist]])
    non_zero_values = len([1 for x in zero_list if x != 0])
    #average
    avg = sum(zero_list)/non_zero_values
    
    return avg
    
def nan_to_null(array):
    ''' takes an array, checks for nan values and if they are found replaces them.'''
    row_nb, col_nb = len(array),len(array[0])
    
    #makes all nan values 0.0
    zero_list = np.array([0 if np.isnan(val) else val for val in [item for sublist in array.tolist() for item in sublist]])
    zero_array = np.resize(zero_list,(row_nb,col_nb))
    
    return zero_array
    
def crop_and_replace(array,c,r):
    ''' np.array -> np.array
        creats a copy of the array and replaces the value at
        column c and row r by the average of the non-nan and 0 values
        around it. Returns the NEW array'''
    cropped_array = crop_array(array,c,r)
    avg =   avg_array(cropped_array)
    new_array = array
    new_array[r][c] = avg
    return new_array
    
def get_nan_locs(array):
    ''' np.array -> [*tulp]
        a Generator which scans an array and returns the column and row of any nan value found
        as a tulp '''
    col_nb = len(array[0])
    for n,val in enumerate([item for sublist in array.tolist() for item in sublist]):
        if np.isnan(val):
            yield (n-(n/col_nb)*col_nb, n/col_nb)
        
def interpolate_array(array):
    ''' np.array -> np.array
        takes in an array, scans it for nan values,
        if any are found they are replaced by the
        average of the non-nan values in it's imediate
        vincinity (i.e 3x3 array centered on the nan value).'''
    avg_ls = []
    # first, get's all the averages so that averaged values do not count in subsequent
    # averages' calculations
    for (c,r) in get_nan_locs(array):
        cropped_array = crop_array(array,c,r)
        avg_ls.append(avg_array(cropped_array))
        
    # then replace all the averages in the array
    for n,(c,r) in enumerate(get_nan_locs(array)):
        array[r][c] = avg_ls[n]

    print array        
    return array
        
b = crop_array(a,1,1)