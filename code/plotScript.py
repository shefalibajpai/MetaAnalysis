import matplotlib.pyplot as plt
import numpy as np
import psycopg2 as psy
import os, sys
import csv
import codecs
import dbQuery as db
from mpl_toolkits.axes_grid1 import make_axes_locatable

USERNAME = 'shefali'
DATABASE = 'cbc_database'

def plotInterExpBabyCount(plotName = -1, username = USERNAME, database = DATABASE):
    """
    This function plots number of babies common in each pair of experiments. 
    """
    #estblishing connection to the database
    con = psy.connect(database= database, user = username)
    
    #fetch a list of experiment ids in the database
    exp_ids = db.getExperimentIdsDB(con)
    
    #initailizing a matrix to store results
    mtx = np.zeros((len(exp_ids), len(exp_ids)))
    
    for ii, exp_id1 in enumerate(exp_ids):
        for jj, exp_id2 in enumerate(exp_ids):
            #fetching list of babies which are common in pairs of experiments
            babies = db.getBabiesCommonInExp(con, exp_id1, exp_id2)
            mtx[ii,jj] = len(babies)
    
    
    y_labels = exp_ids
    x_labels = exp_ids
    
    width = len(x_labels)
    height = len(y_labels)
 
    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    ax.grid(which='major')
    res = ax.matshow(mtx, nterpolation='nearest', aspect='1', cmap=plt.cm.GnBu, extent=[0, width, height, 0])
    
    for x in range(width):
        for y in range(height):
            ax.annotate(str(int(mtx[x][y])), xy=(y+0.5, x+0.5), 
                    horizontalalignment='center',
                    verticalalignment='center')
        
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="5%", pad=0.4)
    cb = fig.colorbar(res, cax=cax, orientation = 'horizontal')

    #Axes
    ax.set_title("Baby count common in pairs of experiments")
    ax.set_xlabel("Experiment ID")
    ax.set_ylabel("Experiment ID")
    ax.set_xticks(range(width))
    ax.set_xticklabels(x_labels, rotation='vertical')
    ax.xaxis.labelpad = 0.5
    ax.set_yticks(range(height))
    ax.set_yticklabels(y_labels , rotation='horizontal')
    if plotName == -1:
        plt.show()
    else:
        plt.savefig(plotName)
    
    return True
    
