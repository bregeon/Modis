# -*- coding: utf-8 -*-
"""
Open an ASCII file with MODIS data and look for data closest
to be associated to list of HESS runs

Created on Fri Feb  3 10:36:41 2017

@author: J. Bregeon
"""

from datetime import datetime
from bisect import bisect

from read_Modis_ascii import readTxt, ingest10k

LIDAR_CRAB_RUNS_LIST = [78815, 78922, 79556, 79858, 79859, 79860, 79862,
                        79881, 79882, 79884, 79885, 80026, 80081, 80086,
                        80124, 80129, 80154]

def read_HESS_RunDate(fname='Run_Date_list.txt'):
    content=open(fname).readlines()
    RUN_DATE_DICT={}
    for line in content[1:]:
        run=int(line.split()[0])
        strdate=line.split()[1]
        #2011-07-12_03:47:30
        date=datetime.strptime(strdate,'%Y-%m-%d_%H:%M:%S') 
        RUN_DATE_DICT[run]=date
    return RUN_DATE_DICT
       

# Main for running
if __name__ == '__main__':
    # read file    
    cont=readTxt('all_modis_10k.txt')
    # ingest data 10k
    modis_dates,minsep_l, minsepkm_l, alt_l, aetype_l, cloudfrac_l, odratio_l,\
    od_l, imgod_l, od470_l, od550_l, od660_l, dbod550_l, dbae_l=ingest10k(cont)
 
    # get data
    runDateDict=read_HESS_RunDate('Run_Date_list.txt')
    print("Run Date dhours1 sep1 aetype1 cloudfrac1 dbod1 dbae1 dhours2 sep2 aetype2 cloudfrac2 dbod2 dbae2")    

    # run on a list
#    for run in LIDAR_CRAB_RUNS_LIST:
    allruns=runDateDict.keys()    
    allruns.sort()
    for run in allruns:
        run_date=runDateDict[run]
        m=bisect(modis_dates, run_date)
        deltat_a=modis_dates[m-1]-run_date
        dhours_a=deltat_a.total_seconds()/3600.
        deltat_b=modis_dates[m]-run_date
        dhours_b=deltat_b.total_seconds()/3600.
#        print("%s %s %s %.1f %s %s %s %.1f %s %s"%(run, run_date,\
#            modis_dates[m-1], dhours_a, minsepkm_l[m-1], dbod550_l[m-1],\
#            modis_dates[m], dhours_b, minsepkm_l[m], dbod550_l[m]))
        print("%s %s %.1f %s %s %s %s %s %.1f %s %s %s %s %s"%(run, run_date,\
            dhours_a, minsepkm_l[m-1], aetype_l[m-1], cloudfrac_l[m-1], dbod550_l[m-1], dbae_l[m-1],\
            dhours_b, minsepkm_l[m],   aetype_l[m],   cloudfrac_l[m],   dbod550_l[m],   dbae_l[m]))        

# Ae Type 0=mixed, 1=dust, 2=sulfate, 3=smoke, 4=heavy absorbing smoke