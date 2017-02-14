#!/bin/env python
# Stolen from Justin Roberts-Pierel, 2015 "read_and_map_mod_aerosol.py"
from pyhdf import SD
import numpy as np
#from mpl_toolkits.basemap import Basemap
#import matplotlib.pyplot as plt
import math
import glob

# South = 23deg16.28' East=16deg30'
hess_lat=-23.25
hess_lon=16.50
delta_pos=0.23 # 0.23 25x25 km2
degtokm=40000./360.

#    # Data of interest
#    # Valid Range: 0.0 to 3.1558E+9 seconds since 1 January 1993 00:00:00 
#    'Scan_Start_Time'
#    # Land only
#    # Type 0=mixed, 1=dust, 2=sulfate, 3=smoke, 4=heavy absorbing smoke
#    'Aerosol_Type_Land'
#    # Corrected OD : 470, 550, 660 um
#    'Corrected_Optical_Depth_Land'
#    # Corrected OD for small modes : 0 to 1
#    'Optical_Depth_Ratio_Small_Land' 
#    # AE from 470 to 670 um -1.0 to 5.0
#    'Angstrom_Exponent_Land'
#    # Cloud fraction, no Cirrus
#    'Cloud_Fraction_Land'
#    # Combined Land and Ocean
#    # High quality combined optical depth
#    'Optical_Depth_Land_And_Ocean'
#    # Good quality combined optical depth : 550 nm
#    'Image_Optical_Depth_Land_And_Ocean'
#    # Combined OD ratio of small mode 0 to 1
#    'Optical_Depth_Ratio_Small_Land_And_Ocean'    
#    # Deep Blue algorithm
#    'Deep_Blue_Aerosol_Optical_Depth_550_Land'
#    'Deep_Blue_Aerosol_Optical_Depth_Land' #  0.412, 0.47, and 0.66
#    'Deep_Blue_Angstrom_Exponent_Land' # -5; 5
#FULL_DATA_LIST=['Scan_Start_Time', 'Aerosol_Type_Land', 'Corrected_Optical_Depth_Land',
#           'Optical_Depth_Ratio_Small_Land',
#           'Angstrom_Exponent_Land', 'Cloud_Fraction_Land', 'Optical_Depth_Land_And_Ocean',
#           'Image_Optical_Depth_Land_And_Ocean', 'Optical_Depth_Ratio_Small_Land_And_Ocean',
#           'Deep_Blue_Aerosol_Optical_Depth_550_Land',
#           'Deep_Blue_Aerosol_Optical_Depth_Land' ,
#           'Deep_Blue_Angstrom_Exponent_Land']

# 3K files
# 'Angstrom_Exponent_Land','Cloud_Fraction_Land','Optical_Depth_Ratio_Small_Land_And_Ocean',
# 'Deep_Blue_Aerosol_Optical_Depth_550_Land', 'Deep_Blue_Aerosol_Optical_Depth_Land' ,
# ,'Deep_Blue_Angstrom_Exponent_Land'
DATA_LIST_3K=['Scan_Start_Time', 'Topographic_Altitude_Land',
              'Aerosol_Type_Land', 'Aerosol_Cloud_Fraction_Land', 
              'Optical_Depth_Ratio_Small_Land',
              'Optical_Depth_Land_And_Ocean',
              'Image_Optical_Depth_Land_And_Ocean',
              'Corrected_Optical_Depth_Land']

# 'Angstrom_Exponent_Land', 'Cloud_Fraction_Land' 'Optical_Depth_Ratio_Small_Land_And_Ocean',
# 'Deep_Blue_Aerosol_Optical_Depth_Land' 
# 3D 'Corrected_Optical_Depth_Land', ?
DATA_LIST_L2=['Scan_Start_Time', 'Topographic_Altitude_Land',
              'Aerosol_Type_Land', 'Aerosol_Cloud_Fraction_Land',
              'Optical_Depth_Ratio_Small_Land' ,
              'Optical_Depth_Land_And_Ocean',
              'Image_Optical_Depth_Land_And_Ocean',
              'Corrected_Optical_Depth_Land',
              'Deep_Blue_Aerosol_Optical_Depth_550_Land',           
              'Deep_Blue_Angstrom_Exponent_Land']



# Angluar separation
def AngularSep_Haversine(Theta_a,Phi_a,Theta_b,Phi_b):
    """ Return the angular separation between two directions (in degrees)
        From http://en.wikipedia.org/wiki/Haversine_formula
        and also https://confluence.slac.stanford.edu/display/SCIGRPS/2008/10/26/On+Calculating+Angular+Distances
    This uses the equation:
    
    sin( ang_sep / 2)^2 = sin( d_lat / 2 )^2 + cos( Theta_a ) cos( Theta_b ) sin( d_phi / 2 )^2
    
    Where d_lat and d_phi are the difference in latitude.
    
    This has the advantage of having very small rounding errors near zero
    """
    halfDelTheta = 0.5 * math.radians( Theta_a - Theta_b )
    halfDelPhi = 0.5 * math.radians( Phi_a - Phi_b )
    sinHalfDelTheta = math.sin(halfDelTheta)
    sinHalfDelPhi = math.sin(halfDelPhi)
    arc2 = (sinHalfDelTheta*sinHalfDelTheta) + math.cos( math.radians(Theta_a) ) * math.cos( math.radians(Theta_b) ) * sinHalfDelPhi * sinHalfDelPhi
    angSep = 2. * math.asin( math.sqrt(arc2) )
    return math.degrees(angSep)

# Test Angular separation calculation on one point
def test_AngSep(filename):
    try:
        hdf=SD.SD(filename)
    except:
        print('Unable to open file: \n' + filename + '\n Skipping...')
        raise   
    # Get lat and lon info
    lat = hdf.select('Latitude')
    latitude = lat[:]
    lon = hdf.select('Longitude')
    longitude = lon[:]
    sep=AngularSep_Haversine(latitude[0][0], longitude[0][0], hess_lat, hess_lon)
    print('%.2f %.2f %.2f %.2f'%(latitude[0][0], longitude[0][0], sep, sep*degtokm))    

def goDebug(FILE_NAME):
    print('Opening %s'%FILE_NAME)
    try:
        hdf=SD.SD(FILE_NAME)
        if "MOD04_3K" in FILE_NAME[:8]:
            DATA_LIST=DATA_LIST_3K
        elif "MOD04_L2" in FILE_NAME[:8]:
            DATA_LIST=DATA_LIST_L2
        else:
            print("Unknwon file type ?")
            DATA_LIST=DATA_LIST_L2
    except:
        print('Unable to open file: \n' + FILE_NAME + '\n Skipping...')
        raise
    return hdf, DATA_LIST
    
# get raw science data
def getRawSDSData(hdf, sds_name):
    sds_od=hdf.select(sds_name)
    attributes=sds_od.attributes()
    scale_factor=attributes['scale_factor']
    #get valid range for AOD SDS
    sds_range=sds_od.getrange()
    min_range=min(sds_range)
    max_range=max(sds_range)    
    #get SDS data
    data=sds_od.get()
    return (data, scale_factor, min_range, max_range)


# get scaled data
def getScaledSDSData(hdf, sds_name):
    data, scale_factor, min_range, max_range = getRawSDSData(hdf, sds_name)
    return (data*scale_factor, min_range*scale_factor, max_range*scale_factor)

    
# get info from one file
def processOne(FILE_NAME, debug=True):
    if debug:
        print('Opening %s'%FILE_NAME)
    try:
        hdf=SD.SD(FILE_NAME)
        if "MOD04_3K" in FILE_NAME:
            DATA_LIST=DATA_LIST_3K
        elif "MOD04_L2" in FILE_NAME:
            DATA_LIST=DATA_LIST_L2
        else:
            print("Unknwon file type ?")
            DATA_LIST=DATA_LIST_L2
    except:
        print('Unable to open file: \n' + FILE_NAME + '\n Skipping...')
        raise
    # parse file name to get date time
    yearday=FILE_NAME.split('/')[-1].split('.')[1][1:]
    year=int(yearday[:4])
    day=int(yearday[4:])
    hourmin=FILE_NAME.split('/')[-1].split('.')[2]
    hour=int(hourmin[:2])
    minu=int(hourmin[2:])
    txt='%s %s %s %s '%(year, day, hour, minu)
    
    # Get lat and lon info
    lat = hdf.select('Latitude')
    latitude = lat[:]
    lon = hdf.select('Longitude')
    longitude = lon[:]
    # get tiles close enough
    good_lon=abs(longitude-hess_lon)<delta_pos
    good_lat=abs(latitude-hess_lat )<delta_pos
    good_pos_ind=np.nonzero(good_lon*good_lat)
    #if debug:
    #    print('Indices of good positions:\n',good_pos_ind)
    #return good_pos_ind

    # Get AOD data
#    od_data, od_scale, od_min, od_max = getRawSDSData(hdf, 'Image_Optical_Depth_Land_And_Ocean')
    od_data, od_min, od_max = getScaledSDSData(hdf, 'Image_Optical_Depth_Land_And_Ocean')
    if debug:
        print('od\t%.2f %.2f'% (od_min, od_max))
    t_data, t_min, t_max = getScaledSDSData(hdf, 'Scan_Start_Time')
    if debug:
        print('time\t%.2f %.2f'% (t_min, t_max))
    
    ALL_DATA_DICT={}
    for sds_name in DATA_LIST:
        if debug:
            print('get %s data'%sds_name)
        ALL_DATA_DICT[sds_name]=getScaledSDSData(hdf, sds_name)

#    for i,j in zip(good_pos_ind[0], good_pos_ind[1]):
#        lat=latitude[i,j]
#        lon=longitude[i,j]            
#        sep=AngularSep_Haversine(lat, lon, hess_lat, hess_lon)
#        #od=od_data[i,j]
#        #time=t_data[i,j]
#        #print('%.2f %.2f %.2f %.1f %.2f %.1f'%(lat, lon, sep, sep*degtokm, od, time))
#        print('\n%.2f %.2f %.2f %.1f '%(lat, lon, sep, sep*degtokm)),
#        for sds_name in DATA_LIST:
#            #print(sds_name),
#            point=ALL_DATA_DICT[sds_name][0][i,j]
#            print('%.2f '%point),
    min_sep=10
    i_min=-1
    j_min=-1
    for i,j in zip(good_pos_ind[0], good_pos_ind[1]):
        lat=latitude[i,j]
        lon=longitude[i,j]            
        sep=AngularSep_Haversine(lat, lon, hess_lat, hess_lon)
        if sep<min_sep:
            i_min=i
            j_min=j
            min_sep=sep
        
    txt+='%.2f %.2f %.2f %.1f '%(latitude[i_min,j_min], longitude[i_min,j_min], min_sep, min_sep*degtokm)
    for sds_name in DATA_LIST:
        ndim=ALL_DATA_DICT[sds_name][0].ndim
        shape=ALL_DATA_DICT[sds_name][0].shape
        if debug:
            print(sds_name, ndim, shape)
        if ndim==3:
            for i in range(shape[0]):
                point=ALL_DATA_DICT[sds_name][0][i][i_min,j_min]
                txt+='%.2f '%point
        elif ndim==2:
            point=ALL_DATA_DICT[sds_name][0][i_min,j_min]
            txt+='%.2f '%point        
    return txt


# process all files
def processAll(directory='/ams/bregeon/Hess/Lidar/Modis/data3k/', outFile='all_modisK.txt'):    
    allfiles=glob.glob(directory+"/*.hdf")
    allfiles.sort()
    buff=[]
    for one in allfiles:
        txt=processOne(one, False)
        print(txt)
        buff.append('\n'+txt)
    outFile=open(outFile,'w')
    outFile.writelines(buff)
    outFile.close()


if __name__ == '__main__':
    # for testing
    FILE_NAME='MOD04_L2.A2013315.0920.006.2015071041708.hdf'
#    FILE_NAME='MOD04_3K.A2013258.0925.006.2015069054335.hdf'
    #test_AngSep(FILE_NAME)
    #hdf=goDebug(FILE_NAME)
#    txt=processOne(FILE_NAME, True)
#    print(txt)
    processAll(directory='/tmp/modis/data3k/', outFile='test.txt')
    # @TODO get mean, stddev from 3x3 grid around nearest point