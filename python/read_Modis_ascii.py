# -*- coding: utf-8 -*-
"""
Read a simple ASCII file with MODIS data

ASCII file was created by extract_Modis_data.py

Created on Fri Feb  3 10:31:41 2017

@author: J. Bregeon
"""

from datetime import datetime

# open and read file content
def readTxt(fname):
    try:
        print('Opening %s'%fname)
        content=open(fname,'r').readlines()
    except:
        print('Could not open %s'%fname)
        raise
    return content[1:]
    
# ingest data from list
def ingest10k(content):
    dates=[]
    minsep_l=[]
    minsepkm_l=[]
    alt_l=[]
    aetype_l=[]
    cloudfrac_l=[]
    odratio_l=[]
    od_l=[]
    imgod_l=[]
    od470_l=[]
    od550_l=[]
    od660_l=[]
    dbod550_l=[]
    dbae_l=[]        
    for aline in content:
        # get data
        year, day, hour, minu, lat, lon, minsep, minsepkm, startime,\
        alt, aetype, cloudfrac, odratio, od, imgod, od470, od550, od660,\
        dbod550, dbae=aline.split()
#        print(year, day, hour, minu, lat, lon, minsep, minsepkm, startime,\
#        alt, aetype, cloudfrac, odratio, od, imgod, od470, od550, od660,\
#        dbod550, dbae)
        # create datetime object
        datefmt='%s/%03d/%02d-%02d'%(year,int(day),int(hour),int(minu))
        date=datetime.strptime(datefmt,'%Y/%j/%I-%M')
        
        dates.append(date)
        minsep_l.append(minsep)
        minsepkm_l.append(minsepkm)
        alt_l.append(alt)
        aetype_l.append(aetype)
        cloudfrac_l.append(cloudfrac)
        odratio_l.append(odratio)
        od_l.append(od)
        imgod_l.append(imgod)
        od470_l.append(od470)
        od550_l.append(od550)
        od660_l.append(od660)
        dbod550_l.append(dbod550)
        dbae_l.append(dbae)
    return dates, minsep_l, minsepkm_l, alt_l, aetype_l, cloudfrac_l, odratio_l,\
           od_l, imgod_l, od470_l, od550_l, od660_l, dbod550_l, dbae_l

# ingest data from list
def ingest3k(content):
    dates=[]
    minsep_l=[]
    minsepkm_l=[]
    alt_l=[]
    aetype_l=[]
    cloudfrac_l=[]
    odratio_l=[]
    od_l=[]
    imgod_l=[]
    od470_l=[]
    od550_l=[]
    od660_l=[]
    for aline in content:
        # get data
        year, day, hour, minu, lat, lon, minsep, minsepkm, startime,\
        alt, aetype, cloudfrac, odratio, od, imgod, od470, od550, od660=aline.split()
#        print(year, day, hour, minu, lat, lon, minsep, minsepkm, startime,\
#        alt, aetype, cloudfrac, odratio, od, imgod, od470, od550, od660)
        # create datetime object
        datefmt='%s/%03d/%02d-%02d'%(year,int(day),int(hour),int(minu))
        date=datetime.strptime(datefmt,'%Y/%j/%I-%M')
        
        dates.append(date)
        minsep_l.append(minsep)
        minsepkm_l.append(minsepkm)
        alt_l.append(alt)
        aetype_l.append(aetype)
        cloudfrac_l.append(cloudfrac)
        odratio_l.append(odratio)
        od_l.append(od)
        imgod_l.append(imgod)
        od470_l.append(od470)
        od550_l.append(od550)
        od660_l.append(od660)
    return dates, minsep_l, minsepkm_l, alt_l, aetype_l, cloudfrac_l, odratio_l,\
           od_l, imgod_l, od470_l, od550_l, od660_l

# Main for running
if __name__ == '__main__':
    # read file    
    cont=readTxt('all_modis_10k.txt')
    # ingest data 10k
    dates,minsep_l, minsepkm_l, alt_l, aetype_l, cloudfrac_l, odratio_l,\
    od_l, imgod_l, od470_l, od550_l, od660_l, dbod550_l, dbae_l=ingest10k(cont)
