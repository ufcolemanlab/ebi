#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:46:50 2019

@author: jcoleman
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import codecs
from scipy.signal import savgol_filter
from scipy.signal import butter, lfilter

import Tkinter as tk
import tkFileDialog
from glob import glob
from collections import OrderedDict

# Enter parameters
filename_csv = 'kineticanalysistableresults.csv'
filedir = '/Users/jcoleman/Documents/--DATA--/octet_data_working/190701_Experiment1_cfos/Results/'
#filedir = '/Users/jcoleman/Documents/PYTHON/encor/octet/saved data/'
sensor_number = 3
dataTXTname = str(filedir) +"*.txt"
dataList = glob(dataTXTname)
filename_txt = []
for i in range(len(dataList)):
    temp1 = os.path.split(dataList[i])
    filename_txt.append(temp1[1])
    
    
    
filename_txt = ['A'+str(sensor_number)+'Results.txt',
                'B'+str(sensor_number)+'Results.txt',
                'C'+str(sensor_number)+'Results.txt',
                'D'+str(sensor_number)+'Results.txt',
                'E'+str(sensor_number)+'Results.txt',
                'F'+str(sensor_number)+'Results.txt',
                'G'+str(sensor_number)+'Results.txt']
filename_dat = 'aligny.dat'

fig_title = 'MCA-7D2-MBP'
filename_new = '062619_mca7D2mbp_kinetics'

plotfits = True #True if you want to plot curve fits (**Results.txt files)

# this allows text to be read in AI after export
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
# set plot font and size for the kernel
plt.rcParams["font.family"] = "arial"
plt.rcParams['font.size'] = 12 
# set line thickness etc
fit_thickness = 2.0
trace_thickness = 1.0

def load_filenames():
    
    root = tk.Tk()
    root.withdraw()
    root.update()
    
    directory = tkFileDialog.askdirectory(parent=root,title=
                                          'Choose directory with TXT, CSV files...')
        #'Choose directory with *.BIN, DATA_*.CSV, STD_*.tif, and ROI_*.zip files ...')
    
    #Setup file lists
    summaryCSVname = str(directory) +"/*.csv"
    dataTXTname = str(directory) +"/*.txt"

    summaryList = glob(summaryCSVname)
    dataList = glob(dataTXTname)
    
    #timestampList.sort()
        
    return summaryList, dataList


#% open kinetic analysis CSV file ('filedir+filename_csv')
def import_data(directory,filename,filetype):
    
    #codecs usage - https://stackoverflow.com/questions/7894856/line-contains-null-byte-in-csv-reader-python
    
    if filetype == 'dat':
        if '\0' in open(directory+filename).read():
            print "Processing DAT file..."
            a = csv.reader(codecs.open(directory+filename, 'rU', 'utf-16'), delimiter = '\t')
            a = list(a)
            b = np.array(a)
            #a_array.astype(float)
            reader = np.reshape(b, (9000,32), order='F')
            
        return reader
    
    if filetype == 'csv':
        print "Processing CSV file..."
        with open(directory+filename, 'rb') as csvfile:
        
            reader = csv.reader(csvfile, delimiter = ',')
            reader = list(reader)
            
        return reader
            
    if filetype == 'txt':
        print "Processing TXT file..."        
        with open(directory+filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter = '\t')#',')
            reader = list(reader)
            r = [row[0:3] for row in reader]
            del r[0:8]
        
        x = np.array(r).astype(np.float64)
        
        return x
            
    print "fIN."
    
    #return reader #, a, a_array
    
def butter_lowpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    
    return y

#%% code for plotting baseline-association-dissociation data
    
data_withbaseline = import_data(filedir,filename_dat, 'dat')
# chunk into len()/8 (ie #data points divided by #sensors; should be even)
data_x = np.array(data_withbaseline[:,16], dtype=float)
data_y = []

# plot data for each sensor (A-F)
sensorloc = range(24,31)
for i in range(len(filename_txt)):
    
    y = np.array(data_withbaseline[:,sensorloc[i]], dtype=float) #24-31 = sensors A-H, H is blank
    data_y.append(y) # = plt.plot(x,y)


#%% code for getting values from CSV file

data_kinetic = import_data(filedir,filename_csv, 'csv')
    
# find desired cells in list
kinetic_table = list()
table_cats = len(data_kinetic[0])  

for i in range(table_cats):
    # Find string keys from CSV file
    if 'KD (M)' in data_kinetic[0][i]:
        kinetic_table.append(data_kinetic[1][i])
        
    if 'Conc. (nM)' in data_kinetic[0][i]:
        samples_conc = dict()
        # Add iteratively to dict
        for j in range(len(data_kinetic)-1):        
            samples_conc[data_kinetic[j+1][11]] = data_kinetic[j+1][i]            

        kinetic_table.append(samples_conc)
        
    if 'kon(1/Ms)' in data_kinetic[0][i]:
        kinetic_table.append(data_kinetic[1][i])
        
    if 'kdis(1/s)' in data_kinetic[0][i]:
        kinetic_table.append(data_kinetic[1][i])
        
    if 'Full R^2' in data_kinetic[0][i]:
        kinetic_table.append(data_kinetic[1][i])
        
# get values for plot annotation/legend
print('kon (1/Ms) = ' + kinetic_table[2])
print('kdis (1/s) = ' + kinetic_table[3])
print('KD (M) = ' + kinetic_table[0])
print('R^2 = ' + kinetic_table[4])
print(sorted(kinetic_table[1].items(), key = 
             lambda kv:(kv[1], kv[0])))

#create a list of ORDERED analyte concentration values
temp1 = list()
for i in sorted (kinetic_table[1]): 
    
    print ((i, kinetic_table[1][i]))
    temp1.append(kinetic_table[1][i])

analyte_nm = [xx + ' nM' for xx in temp1]

#%% iterate through A*Results.txt files ('filedir+filename_txt')

x_allresults = list()

# extract data and plot the raw data 
for i in range(len(filename_txt)):
                
    xresults = import_data(filedir,filename_txt[i], 'txt') #[0]=time,[1]=norm,[2]=fit
    
    # append each results file to a list
    x_allresults.append(xresults)

#%% IN PROGRESS
plt.figure() 

# plot 'raw normalized' data ("Y Align")    
for i in range(len(data_y)):
    
    yhat = savgol_filter(data_y[i],75,5) # window size 51, polynomial order 3
                
    plt.plot(data_x, yhat, linewidth=trace_thickness, label='raw')
    #plt.plot(x[:,0]-min_xal,x[:,1], linewidth=0.5, label='raw')
    
    #Iterate over the dictionary using for loop
    samples_conc_orderedKeys = sorted(samples_conc) #how to use values only?!
    leg1 = plt.legend(analyte_nm, loc='lower left', bbox_to_anchor=(1, 0.55))
    
plt.tight_layout(rect=[0,0,1,1])

if plotfits is True:
    # plot 'curve fit' data
    for i in range(len(filename_txt)):
        plt.plot(x_allresults[i][:,0],x_allresults[i][:,2], 'r-', linewidth=1)
        #plt.plot(x_allresults[i][:,0]-min_xal,x_allresults[i][:,2], 'r-', linewidth=1) # seperate loop?
    
# kon/koff transition line
# kon/koff transition line
min_xall = np.min(data_x)
max_xall = np.max(data_x)
x_zeroed = data_x-min_xall

temp = np.ceil((max_xall - min_xall) / 3)
time1 = data_x[0] + temp
time2 = data_x[len(data_x)-1] - temp

plt.axvline(x=time1, ymin=0, ymax=1, linewidth=fit_thickness, color='k', ls='--')
plt.axvline(x=time2, ymin=0, ymax=1, linewidth=fit_thickness, color='k', ls='--')

# add legends and title data   
plt.legend()    
leg2 = plt.legend(["global fit"], loc='upper left', bbox_to_anchor=(1, 0.5))
plt.gca().add_artist(leg2)
leg2.get_lines()[0].set_lw(1)
leg2.get_lines()[0].set_color('r')
plt.gca().add_artist(leg1)

plt.xlabel("Time (s)")
plt.ylabel("nm")

plt.title(fig_title + ' | ${K_D}$ (M) = ' + kinetic_table[0])

# save file as PNG and PDF
plt.savefig(filedir + filename_new + ".png", bbox_inches="tight")
plt.savefig(filedir + filename_new + ".pdf", bbox_inches="tight")
plt.savefig(filedir + filename_new + ".tif", bbox_inches="tight")

