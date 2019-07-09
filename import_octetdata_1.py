#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:46:50 2019

@author: jcoleman
"""

import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk
import tkFileDialog
from glob import glob
from collections import OrderedDict
import csv

# Enter parameters
filename_csv = 'kineticanalysistableresults.csv'
filedir = '/Users/jcoleman/Documents/PYTHON/encor/octet/fitting results/'
filename_txt = ['A1Results.txt',
                'B1Results.txt',
                'C1Results.txt',
                'D1Results.txt',
                'E1Results.txt',
                'F1Results.txt',
                'G1Results.txt']

# this allows text to be read in AI after export
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
# set plot font and size for the kernel
plt.rcParams["font.family"] = "arial"
plt.rcParams['font.size'] = 12  

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
    
with open(filedir+filename_csv, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    reader = list(reader)
    
# find desired cells in list
kinetic_table = list()
table_cats = len(reader[0])  

for i in range(table_cats):
    # Find string keys from CSV file
    if 'KD (M)' in reader[0][i]:
        kinetic_table.append(reader[1][i])
        
    if 'Conc. (nM)' in reader[0][i]:
        samples_conc = dict()
        # Add iteratively to dict
        for j in range(len(reader)-1):        
            samples_conc[reader[j+1][11]] = reader[j+1][i]            

        kinetic_table.append(samples_conc)
        
    if 'kon(1/Ms)' in reader[0][i]:
        kinetic_table.append(reader[1][i])
        
    if 'kdis(1/s)' in reader[0][i]:
        kinetic_table.append(reader[1][i])
        
    if 'Full R^2' in reader[0][i]:
        kinetic_table.append(reader[1][i])
        
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

analyte_nm = [x + ' nM' for x in temp1]

#% iterate through result files ('filedir+filename_txt')

x_allresults = list()

# extract data and plot the raw data 
for i in range(len(filename_txt)):
                
    with open(filedir+filename_txt[i], 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = '\t')#',')
        reader = list(reader)
        r = [row[0:3] for row in reader]
        del r[0:8]
        
    x = np.array(r).astype(np.float64)  
    
    # x coordinates = x[:,0]; y coordinates RAW = x[:,1]; y coordinates FIT = x[:,21]
    # Plot raw signal, nm
    min_xal = np.min(x[:,0]) # use this value if plotting from '0' desired
    max_xal = np.max(x[:,0]) # use this value if plotting from '0' desired
    plt.plot(x[:,0], x[:,1], linewidth=0.5, label='raw')
    #plt.plot(x[:,0]-min_xal,x[:,1], linewidth=0.5, label='raw')
    
    #Iterate over the dictionary using for loop
    samples_conc_orderedKeys = sorted(samples_conc) #how to use values only?!
    leg1 = plt.legend(analyte_nm, loc='lower left', bbox_to_anchor=(1, 0.55))
    
    # append each results file to a list
    x_allresults.append(x)

#plot the curve-fit data
# legend outside
plt.tight_layout(rect=[0,0,1,1])

for i in range(len(filename_txt)):
    plt.plot(x_allresults[i][:,0],x_allresults[i][:,2], 'r-', linewidth=1)
    #plt.plot(x_allresults[i][:,0]-min_xal,x_allresults[i][:,2], 'r-', linewidth=1) # seperate loop?
    
# kon/koff transition line
transline = (min_xal + max_xal) / 2 # not exact this way - is there a value from csv file to use?
plt.axvline(x=transline, ymin=0, ymax=1, linewidth=1.0, color='k')

# add legends and title data   
plt.legend()    
leg2 = plt.legend(["global fit"], loc='upper left', bbox_to_anchor=(1, 0.5))
plt.gca().add_artist(leg2)
leg2.get_lines()[0].set_lw(1)
leg2.get_lines()[0].set_color('r')
plt.gca().add_artist(leg1)

plt.xlabel("Time (s)")
plt.ylabel("nm")

plt.title('MCA-1B7-FOX3 | KD (M) = ' + kinetic_table[0])

# save file as PNG and PDF
plt.savefig("output.png", bbox_inches="tight")
plt.savefig("output.pdf", bbox_inches="tight")

