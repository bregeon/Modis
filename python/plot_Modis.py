# -*- coding: utf-8 -*-
"""
Plot Modis data

Created on Tue Jan 31 15:15:25 2017

@author: J. Bregeon
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from read_Modis_ascii import readTxt, ingest3k, ingest10k


def plotDataTrend(dates, data_l):
    fig, ax = plt.subplots(1)
    ax.plot(dates,data_l, 'ro')    
    
    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    
    # use a more precise date string for the x axis locations in the
    # toolbar   
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.title('HESS Atmo Monitoring')
    ax.set_xlabel("Date")
    #ax.set_ybound(0,15000)
    ax.set_ylabel("?")
    plt.show()

def plotODTrend(dates, data_l):
    fig, ax = plt.subplots(1)
    ax.plot(dates,data_l, 'ro')        
    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()    
    # use a more precise date string for the x axis locations in the
    # toolbar   
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.title('HESS Atmo Monitoring')
    ax.set_xlabel("Date")
    ax.set_ybound(-0.1,1.1)
    ax.set_ylabel("Optical Depth")
    plt.show()
    
def plotDataCorr(data1, data2):
    fig, ax = plt.subplots(1)
    ax.plot(data1,data2, 'ro')        
    plt.title('HESS Atmo Correlation')
    ax.set_xlabel("X")    
    ax.set_ylabel("Y")
    plt.show()

def myplot(dates, data_l):
    fig, ax = plt.subplots(1)
    ax.plot(dates,data_l, 'ro')        
    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()    
    # use a more precise date string for the x axis locations in the
    # toolbar   
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.title('HESS Atmo Monitoring')
    ax.set_xlabel("Date")
    ax.set_ybound(-0.05,1.05)
    ax.set_ylabel("Deep Blue Aerosol Optical Depth 550nm")
    plt.show()
    
# Main for running
if __name__ == '__main__':
    # read file    
    cont=readTxt('all_modis_10k.txt')
    # ingest data 10k
    dates,minsep_l, minsepkm_l, alt_l, aetype_l, cloudfrac_l, odratio_l,\
    od_l, imgod_l, od470_l, od550_l, od660_l, dbod550_l, dbae_l=ingest10k(cont)
    
    # ingest data 3k
#    dates,minsep_l, minsepkm_l, alt_l, aetype_l, cloudfrac_l, odratio_l,\
#    od_l, imgod_l, od470_l, od550_l, od660_l=ingest3k(cont)

    #plot
#    plotODTrend(dates, dbod550_l)

    # my plot    
    myplot(dates, dbod550_l)
    
#    # Type 0=mixed, 1=dust, 2=sulfate, 3=smoke, 4=heavy absorbing smoke
    