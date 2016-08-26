# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 11:01:26 2016

@author: s0939551
"""
import csv
import numpy as np
import os
from matplotlib.mlab import griddata
import math

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def conditional_filedata_extraction(filename, to_plot, dico):
    '''   String,[3*String],[Numbers or '-'] -> None
    extracts data based on the requested values and requested output to_plot'''
    
    return file_extract(filename, to_plot, dico)

        
class FileData(list):
    '''FileData takes three list arguments and nest's them into a single list [[],[],[]]
    interp. the first list is the x values, the second the y values and the thrid the z values
    def function_for_FileData(fd):
        ... fd[0] : list
        ... fd[0] : list
        ... fd[0] : list'''
        
    def __init__(self,xs,ys,zs):
        [self.append(ls) for ls in [xs,ys,zs]]
        
def x_array(xinputs,yinputs):
    return np.array([sorted(set(xinputs)) for n in range(len(set(yinputs)))])

def y_array(yinputs,xinputs):
    return np.array([[n]*len(set(xinputs)) for n in sorted(set(yinputs))])
    
def file_extract(filename, to_extract, headers):
    ''' String [String String String] Dict{*String:Number}-> List List List
        Extract the data from a file by verifying the value for each column
        header. Outputs 3 lists which contain the data corresponding to to_extract
        if the header value corresponds
        return [5,7,5,7],[0,0,1,1],[10,20,30,40]
    '''
    with open(filename, "r") as myfile:
       data = csv.reader(myfile, delimiter=',')  #makes a generator from data
       for row in data:
           index_to_header = {n:header for n,header in enumerate(row)}
           header_to_index = {header:n for n,header in enumerate(row)}
           break
       #next(data) #skips first line
       xdat,ydat,zdat = [],[],[]
       filels = []
       print headers
       for row in data:
           filels.append(row)
           if False not in [True if index_to_header[col] not in headers.keys() or float(headers[index_to_header[col]]) == float(val)  else False for col,val in enumerate(row)]:
               for n,ls in enumerate([xdat,ydat]):
                    if row[header_to_index[to_extract[n]]] != '':
                        ls.append(float(row[header_to_index[to_extract[n]]]))
                    else:
                        ls.append(np.nan)

       xarray = x_array(xdat,ydat)# np.array([sorted(set(xdat)) for n in range(len(set(ydat)))])
       yarray = y_array(ydat,xdat)# np.array([[n]*len(set(xdat)) for n in sorted(set(ydat))])
       
       newx = [item for sublist in xarray.tolist() for item in sublist]
       newy = [item for sublist in yarray.tolist() for item in sublist]
       
       myfile.seek(0) #goes back to first character in the file
       next(data) #goes to first data line after headers
       for n in range(len(newx)):
           myfile.seek(0) #goes back to first character in the file
           next(data) #goes to first data line after headers
           for row in data:
              if False not in [True if index_to_header[col] not in headers.keys() or float(headers[index_to_header[col]]) == float(val)  else False for col,val in enumerate(row)]:
                   if float(row[header_to_index[to_extract[0]]]) == newx[n] and float(row[header_to_index[to_extract[1]]]) == newy[n]:
                       zdat.append(float(row[header_to_index[to_extract[2]]])) if row[header_to_index[to_extract[2]]] != '' else zdat.append(np.nan)
    
    return FileData(xdat,ydat,zdat)

    
def isfloat(n):
    try:
        float(n)
        return True
    except ValueError:
        return False
        
def get_1percent(value):
    return round((math.ceil(value)/100),len(str(value).split('.')[1]))
        
        
def input_check(user_input, inputstyle):
    if inputstyle == 'number':
        return isfloat(user_input)
    if inputstyle == 'file':
        return os.path.exists(user_input)
    
        
def _quit(frame):
    frame.quit()     # stops mainloop
    frame.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

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
        
def extrapolate_array(array):
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

    return array
    
def interpolation(data):
    x,y,z = data
    xi,yi = np.linspace(min(x),max(x),10),np.linspace(min(y),max(y),10)
    zi = griddata(x,y,z,xi,yi,interp='linear')
    return xi,yi,zi


