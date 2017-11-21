
# coding: utf-8

# In[3]:


# %load test.py


# In[ ]:


from __future__ import print_function
import traceback
import sys
import glob
 
from eccodes import *
 
INPUT = '/home/dp/data/ECMF_DAM/PUB/W_NAFP_C_ECMF_20171108054547_P_C1D11080000110800001'
STATIONINPUT='/home/dp/data/stationTest.txt'
VERBOSE = 1  # verbose error reporting
missingValue = 1e+20  # A value out of range 
 
def example():
    f = open(INPUT)
    
    for line in open(STATIONINPUT):
        lineSplit=line.split(" ")
        dateTime=lineSplit[0][4:]+lineSplit[1]+lineSplit[2]
        dateTime_2=dateTime+dateTime+"1"
        fileNameMatch=r"/home/dp/data/ECMF_DAM/PUB/W_NAFP_C_ECMF_*"+dateTime_2
        list=glob.glob(fileNameMatch)
        
        
        print(list)#文件名列表
    
    
        for onefile in list:
            f=open(onefile)
            message_count=codes_count_in_file(f) #文件中共有多少message
            print("message count %d" % (message_count))
            
            #跳过的部分
            for i in range (1):
                gid = codes_grib_new_from_file(f)
                keyval = codes_get_string(gid, "shortName")
                print("%s = %s" % ("keyname", keyval))
                keyval = codes_get_string(gid, "level")
                print("%s = %s" % ("level", keyval))
                print("-" * 100)
                codes_release(gid)  
                
            #需要的部分
            
            gid = codes_grib_new_from_file(f)
            values = codes_get_values(gid)
            print('len:%d' %(len(values)))
            
            
            lat=float(lineSplit[3])
            lon=float(lineSplit[4])
            print(lat, lon)
            nearest = codes_grib_find_nearest(gid, lat, lon)[0]
            print(nearest.lat, nearest.lon, nearest.value, nearest.distance,
                  nearest.index)
            print("value test：%.10e"%values[nearest.index])
            keyval = codes_get_string(gid, "shortName")
            print("%s = %s" % ("keyname", keyval))
            keyval = codes_get_string(gid, "level")
            print("%s = %s" % ("level", keyval))
            print("-" * 100)
            codes_release(gid)  
           

            
            

            for i in range (1):
                gid = codes_grib_new_from_file(f)
                #if gid is None:
                #    break



                iterid = codes_keys_iterator_new(gid, "ls")
                while codes_keys_iterator_next(iterid):
                        keyname = codes_keys_iterator_get_name(iterid)
                        keyval = codes_get_string(iterid, keyname)
                        print("%s = %s" % (keyname, keyval))

                codes_keys_iterator_delete(iterid)


                values = codes_get_values(gid)
                print('len:%d' %(len(values)))
                print("-" * 100)
                
                codes_release(gid)
            f.close()
    
    
 
 
 
def main():
    try:
        example()
    except CodesInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(err.msg + '\n')
 
        return 1
 
 
if __name__ == "__main__":
    sys.exit(main())


