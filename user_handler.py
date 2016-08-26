# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 12:19:01 2016

@author: s0939551
"""

import Tkinter as tk
import tkFileDialog
import functions as fn


class UserInputManager():
    ''' UserInputManager is UserInputManager()
        interp. A class which regroups the widgets the user can interact with
        as well as the methods needed to communicate those interactions with
        the rest of the program. eg. On press button generate a figure with XYZ
        data and show it to the user using a FigureFrame.showfigure() call.
        
        def function_for_UserInputManager(uim):
            ... UserInputManager.redraw_figures ; class attribute bool
            ... uim.master ; tk.Frame
            ... uim.UIMpanel ; tk.Frame
            ... uim.initiate_figures(self) ; method'''
    width = 0
    height = 0
            
    def __init__(self,master,free_entries = False):
        self.master = master
        
        UserInputManager.width = self.master.parent.winfo_screenwidth()-20
        UserInputManager.height = self.master.parent.winfo_screenheight()-100
        
        self.height = UserInputManager.height
        self.width = UserInputManager.width/2
        
        self.UIMpanel = tk.Frame(master, width = self.width, height = self.height) #Where all interactive widgets are
        self.UIMpanel.pack(side=tk.LEFT)
        
        self.top_frame = tk.Frame(self.UIMpanel, width = self.width, height = int(self.height*0.222)) #Where all interactive widgets are
        self.top_frame.pack(side=tk.TOP)
        
        self.xy_var_frame = tk.Frame(self.UIMpanel, width = self.width, height = int(self.height*0.5556)) #Where all interactive widgets are
        self.xy_var_frame.pack(side=tk.TOP)
        
        self.z_var_frame = tk.Frame(self.UIMpanel, width = self.width, height = int(self.height*0.16)) #Where all interactive widgets are
        self.z_var_frame.pack(side=tk.TOP)
        
        self.bottom_frame = tk.Frame(self.UIMpanel, width = self.width, height = int(self.height*0.1)) #Where all interactive widgets are
        self.bottom_frame.pack(side=tk.TOP)        
        
        xalign = 0.5
        
        #Adding instruction labels
        tk.Label(master = self.top_frame, anchor = 'w', justify= tk.LEFT, wraplength= int(UserInputManager.width*0.45), font = "Verdana 9 bold", text = '''Instructions:
        Make sure to check 3 tick-boxes to select which variables will be plotted along the x, y and z axis.
        The Avg. RT Eff. (%) and Avg. Air Eff. (%) are the only values which can be plotted along the z axis.
        Any parameter not selected as a variable must be given a value by selecting one of the option available when clicking on the button 'Select XXXX:'.
        /!\ Before proceeding to draw make sure all inputs are highlighted in green. If an error message appears double check your inputs.''').place(relx = 0.001, rely=0.001, anchor = 'nw')

        tk.Label(master = self.xy_var_frame, bg = 'light blue', anchor = 'w', justify= tk.LEFT, wraplength= UserInputManager.width/4,text = 'Parameters to choose from to plot on x or y axis.').place(relx = 0.01, rely=0.13, anchor = 'nw')
        tk.Label(master = self.z_var_frame, bg = 'dark green',anchor = 'w', justify= tk.LEFT, wraplength= int(UserInputManager.width*0.2),text = 'Efficincy results to plot on the z axis.').place(relx = 0.01, rely=0.01, anchor = 'nw')

        #choice entry widgets
        if free_entries:
            ec_depth = EntryChoice('Depth','Enter depth',self.UIMpanel,xalign,0.2,'nw', 'blue',True)
            ec_perm = EntryChoice('Perm','Enter permeability',self.UIMpanel,xalign,0.3,'nw', 'blue', True)
            ec_poro = EntryChoice('Poro','Enter porosity',self.UIMpanel,xalign,0.4,'nw','blue', True)
            ec_thick = EntryChoice('Thick','Enter thickness',self.UIMpanel,xalign,0.5,'nw','blue', True)
            
            ec_compeff = EntryChoice('Compressor Isentropic Efficiency','Enter compressor eff.',self.UIMpanel,xalign,0.6,'nw','blue', True)
            ec_turbeff = EntryChoice('Turbine Isentropic Efficiency','Enter turbine eff.',self.UIMpanel,xalign,0.7,'nw','blue', True)
            ec_compstage = EntryChoice('Compression Stages','Enter comp. stages',self.UIMpanel,xalign,0.8,'nw','blue', True)
    
            ec_aireff = EntryChoice('Avg. Air Eff. (%)','Enter Air eff.',self.UIMpanel,xalign,0.9,'nw','dark green', True)
            ec_rteff = EntryChoice('Avg. RT Eff. (%)','Enter RT. eff',self.UIMpanel,xalign,0.98,'nw','dark green', True)
            
        else:   
            ec_depth = DropDownChoice('Depth','Select depth (m)', ('200','800','2750','4000'),self.xy_var_frame,xalign,0.2,'nw','blue', True)
            ec_perm = DropDownChoice('Perm','Select permeability (md)',('100','650','1330'),self.xy_var_frame,xalign,0.3,'nw','blue', True)
            ec_poro = DropDownChoice('Poro','Select porosity (%)',('15','23','30'),self.xy_var_frame,xalign,0.4,'nw','blue', True)
            ec_thick = DropDownChoice('Thick','Select thickness (m)',('40','174','350'),self.xy_var_frame,xalign,0.5,'nw','blue', True)
            
            ec_compeff = DropDownChoice('Compressor Isentropic Efficiency','Select compressor eff.',('0.66','0.81','0.88'),self.xy_var_frame,xalign,0.6,'nw','blue', True)
            ec_turbeff = DropDownChoice('Turbine Isentropic Efficiency','Select turbine eff.',('0.66','0.85','0.88'),self.xy_var_frame,xalign,0.7,'nw','blue', True)
            ec_compstage = DropDownChoice('Compression Stages','Select comp. stages',('2','4','6'),self.xy_var_frame,xalign,0.8,'nw','blue', True)
    
            ec_aireff = DropDownChoice('Avg. Air Eff. (%)','Select Air eff.',('x'),self.z_var_frame,xalign,0.2,'nw','dark green', True)
            ec_rteff = DropDownChoice('Avg. RT Eff. (%)','Select RT. eff',('x'),self.z_var_frame,xalign,0.65,'nw','dark green', True)

        '''temporary inital values'''
        ec_depth.cb.cb.select()
        ec_perm.cb.cb.select()
        ec_depth.choice.set('selected as x')
        ec_poro.choice.set('15')
        ec_thick.choice.set('174')
        ec_compeff.choice.set('0.66')
        ec_turbeff.choice.set('0.66')
        ec_compstage.choice.set('2')
        
        self.ec_filename = EntryChoice('File','File',self.top_frame,xalign,0.85,'nw', 'black', False)
        
        tk.Button(self.top_frame, text='Browse', command = lambda: self.browse_dir1(self.ec_filename)).place(relx= xalign + 0.25, rely=0.82, anchor = 'nw')
        
        self.entry_list = [ec_depth,ec_poro,ec_thick,ec_perm,ec_compeff,ec_compstage,ec_turbeff,ec_aireff,ec_rteff]

        #bottom frame widgets
        #Quit button to destroy root and temrinate application
        button = tk.Button(master = self.bottom_frame, text='Quit', font = 'Bold', command = lambda: fn._quit(master.parent), fg= 'red')#command=_quit
        button.place(relx = xalign + 0.4, rely=0.4, anchor = tk.CENTER)

        #validation button
        self.button_draw = tk.Button(master = self.bottom_frame, text = 'Draw', command = lambda: self.initiate_figures(self.ec_filename.choice.get()))
        self.button_draw.place(relx= xalign + 0.28, rely=0.4, anchor = tk.CENTER)
        
    def extract_entries(self):
        keys = ['Depth','Poro','Thick','Perm','Compressor Isentropic Efficiency','Compression Stages',
        'Turbine Isentropic Efficiency']
        to_plot = [0,0,0]
        dico ={}
        for entry in self.entry_list:
            for key in keys:
                if entry.name == key and fn.isfloat(entry.choice.get()):
                    dico[key] = float(entry.choice.get())
                    break
                elif 'selected as x' in entry.choice.get():
                    to_plot[0] = entry.name
                    break
                elif 'selected as y' in entry.choice.get():
                    to_plot[1] = entry.name
                    break
                elif 'selected as z' in entry.choice.get():
                    to_plot[2] = entry.name
                    break
        print to_plot
        return dico,to_plot
        
    def initiate_figures(self,filename):
        '''running input checks'''
        if fn.input_check(filename, 'file'):
            continue_exec = True
        else:
            Popup(self,'Unable to find file')
            continue_exec = False
            
        for entry in self.entry_list[:-2]:#without the efficiencies
            if not fn.input_check(entry.choice.get(), 'number') and entry.cb.val.get() != 1:
                continue_exec = False
                Popup(self,'{} entry is not a number'.format(entry.name))
                
#        for entry in self.entry_list[-2:]:#just the efficiencies
        test = sum([1 for entry in self.entry_list[-2:] if entry.cb.val.get() == 1])
        if test > 1:
            continue_exec = False
            Popup(self,'You can only output one efficiency')
        elif test < 1:
            continue_exec = False
            Popup(self,'Please select an efficiency')
        
        '''if check passed continue run'''
        if continue_exec:  
            try:
                dico,to_plot = self.extract_entries()
                self.master.initiate_figures(filename,to_plot,dico)
            except:
                Popup(self,'Not enough data to plot')
        
    def update(self):
        total_selected = 0
        for w in self.entry_list:
            w.update()
            if 'selected as x' in w.choice.get(): total_selected += 1
            if 'selected as y' in w.choice.get(): total_selected += 1
            if 'selected as z' in w.choice.get(): total_selected += 1
        
        unvalide_filename = [unvalid_file for unvalid_file in [self.ec_filename] if not fn.input_check(self.ec_filename.choice.get(), 'file')]
        selected_z = [entry for entry in self.entry_list[-2:] if  'selected as z' in entry.choice.get()]
        list_of_unvalid = [entry for entry in self.entry_list[:-2] if not fn.input_check(entry.choice.get(), 'number') and entry.cb.val.get() != 1]\
                         +[unvalid for  unvalid in selected_z if len(selected_z) == 0]\
                         +unvalide_filename
       
        if total_selected == 3 and len(list_of_unvalid) == 0:
            for item in self.entry_list:
                item.choice_entry.configure(bg = 'green')
            self.ec_filename.choice_entry.configure(bg = 'green')
            if self.button_draw.cget('bg') != 'green':
                self.button_draw.config(state="normal", bg = 'green')
            else:
                self.button_draw.config(state="normal", bg = 'cyan')
        else:
            for item in self.entry_list:
                item.choice_entry.configure(bg = 'grey')
            self.ec_filename.choice_entry.configure(bg = 'grey')
            self.button_draw.config(state="disabled", bg = 'red')
                
        for item in list_of_unvalid:
            item.choice_entry.configure(bg = 'red')
            
    def browse_dir1(self,entry):
        inputfile = tkFileDialog.askopenfilename(parent = self.master,initialdir="R:/MyDocuments/DataSets/Isentropic_Efficiency_Summary_SA.csv",title='Pick a file')
        entry.choice.set(inputfile)
                
class Checkbox():
    ''' A class which creates an checkbox widget whith an associated
        variable self.val to access the widget's content when checked
        
        EntryChoice is EntryChoice(String,tk.Frame,Float[0,1],Float[0,1],String_from['top','left','center','bottom','right'])
        
        def function_for_CheckBox(cb):
            ... cb.val ; tk.StringVar()'''

    def __init__(self,master,x,y,anchor,command = None, text = None):
        #__init__(self,String,tk.Frame,Float[0,1],Float[0,1],String_from['top','left','center','bottom','right'])
        self.val = tk.IntVar()
        if text is None:
            self.cb = tk.Checkbutton(master, variable = self.val, command = command)
        else:
            self.cb = tk.Checkbutton(master, text = text, variable = self.val, command = self.update)
        self.cb.place(relx=x, rely=y, anchor = anchor)
        
    def update(self):
        return self.val.get()

        
class EntryChoice():
    ''' A class which creates an entry widget whith an associated
        variable self.choice to access the widget's content
        
        EntryChoice is EntryChoice(String,tk.Frame,Float[0,1],Float[0,1],String_from['top','left','center','bottom','right'])
        
        def function_for_EntryChoice(ec):
            ... ec.choice ; tk.StringVar()'''

    def __init__(self, name, label, master, x, y, anchor, fg, checkbox = False):
        #__init__(self,String,tk.Frame,Float[0,1],Float[0,1],String_from['top','left','center','bottom','right'])
        self.name = name        
        self.choice = tk.StringVar()
        self.choice.set(label)
        self.cb = None
        self.master = master
        self.label = label
        label_entry = tk.Label(master = master, text = name, fg = fg).place(relx= x - 0.15, rely=y, anchor = 'ne')
        self.choice_entry = tk.Entry(master = master, textvariable = self.choice)
        self.choice_entry.place(relx=x, rely=y, anchor = anchor)
        if checkbox: self.cb = Checkbox(master, x-0.8, y, 'ne' , command = self.update)
            
    def update(self):
        if self.cb is not None:
            check_status = self.cb.val.get()
            if check_status == 1:
                if self.name in ['Depth','Poro','Thick','Perm','Compressor Isentropic Efficiency','Compression Stages',
        'Turbine Isentropic Efficiency']:
                    selected = sum([1 for entry in self.master.master.master.userinputmanager.entry_list[:-2] if (entry.cb is not None and entry.cb.val.get() == 1)])
                    if selected - 1 == 0   and 'selected' not in self.choice.get():
                        self.choice.set('selected as x')
                    elif selected - 1 == 1   and 'selected' not in self.choice.get():
                        self.choice.set('selected as y')
                    elif 'selected' not in self.choice.get():
                        self.choice.set(self.label)
                        self.cb.cb.deselect()
                # for efficiency result checboxes        
                else:
                    selected = sum([1 for entry in self.master.master.master.userinputmanager.entry_list[-2:] if (entry.cb is not None and entry.cb.val.get() == 1)])
                    if selected - 1 == 0:
                        self.choice.set('selected as z')
                    else:
                        self.choice.set(self.label)
                        self.cb.cb.deselect()
            elif not fn.isfloat(self.choice.get()):
                self.choice.set(self.label)
                
class DropDownChoice():
    ''' A class which creates an entry widget whith an associated
        variable self.choice to access the widget's content
        
        EntryChoice is EntryChoice(String,tk.Frame,Float[0,1],Float[0,1],String_from['top','left','center','bottom','right'])
        
        def function_for_EntryChoice(ec):
            ... ec.choice ; tk.StringVar()'''

    def __init__(self, name, label, choices, master, x, y, anchor, fg, checkbox = False):
        #__init__(self,String,tk.Frame,Float[0,1],Float[0,1],String_from['top','left','center','bottom','right'])
        self.name = name        
        self.choice = tk.StringVar()
        self.choice.set(label)
        self.cb = None
        self.master = master
        self.label = label
        label_entry = tk.Label(master = master, text = name, fg = fg).place(relx= x - 0.15, rely=y, anchor = 'ne')
        self.choice_entry = apply(tk.OptionMenu,(master, self.choice) + tuple(choices))
        self.choice_entry.place(relx=x, rely=y, anchor = anchor)
        if checkbox: self.cb = Checkbox(master, x-0.1, y, 'nw', command = self.update)
            
    def update(self):
        if self.cb is not None:
            check_status = self.cb.val.get()
            if check_status == 1:
                if self.name in ['Depth','Poro','Thick','Perm','Compressor Isentropic Efficiency','Compression Stages',
        'Turbine Isentropic Efficiency']:
                    list_of_checked = [entry for entry in self.master.master.master.userinputmanager.entry_list[:-2] if (entry.cb is not None and entry.cb.val.get() == 1 and entry is not self)]
                    selected = len(list_of_checked)
                    if selected == 1 and 'selected' not in self.choice.get():
                        self.choice.set('selected as y')                    
                    elif selected == 0   and 'selected' not in self.choice.get():
                        self.choice.set('selected as x')
                    elif 'selected' not in self.choice.get():
#                        self.choice.set(self.label)
#                        self.cb.cb.deselect()
                        self.choice.set('selected as x')
                        xselction = [entry for entry in list_of_checked if 'x' in entry.choice.get()][0]
                        xselction.choice.set(list_of_checked[0].label)
                        xselction.cb.cb.deselect()
                        
                # for efficiency result checboxes        
                else:
                    list_of_checked = [entry for entry in self.master.master.master.userinputmanager.entry_list[-2:] if (entry.cb is not None and entry.cb.val.get() == 1 and entry is not self)]
                    selected = len(list_of_checked)
                    if selected != 0:
                        #resets non selected outputs
                        for item in list_of_checked:
                            item.choice.set(item.label)
                            item.cb.cb.deselect()
                    self.choice.set('selected as z')
                        
            elif not fn.isfloat(self.choice.get()):
                self.choice.set(self.label)

class Popup():
    def __init__(self,master,msg):           
        top = tk.Toplevel()
        top.title("About this application...")
        
        msg = tk.Message(top, text = msg)
        msg.pack()
        
        button = tk.Button(top, text = "Dismiss", command=top.destroy)
        button.pack()
        
