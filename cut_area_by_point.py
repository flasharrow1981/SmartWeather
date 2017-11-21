
# coding: utf-8

# In[23]:


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
            for i in range (5):
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
            #读取最近点的索引号
            nearest = codes_grib_find_nearest(gid, lat, lon)[0]
            print(nearest.lat, nearest.lon, nearest.value, nearest.distance,
                  nearest.index)
            
            
            testnearest = codes_grib_find_nearest(gid,30,98.5)[0]
            print(testnearest.lat, testnearest.lon, testnearest.value, testnearest.distance,
                  testnearest.index)
            
            
            
            
            nearestIndex=nearest.index
            #数值预报范围,欧洲细网格实际为60～-10
            latRange=[-10,60]
            latdense=0.25
            latcount=(latRange[1]-latRange[0])/latdense+1
            
            lonRange=[60,150]
            londense=0.25
            loncount=(lonRange[1]-lonRange[0])/londense+1
            
            crange=9  #截取的范围大小
            radius=(crange-1)/2 #以中心点为核心上下左右各2 
            
            #开始截取
            for r in range(-1*radius,radius+1):
                cur_min=int(nearestIndex+r*loncount-radius)
                cur_max=int(nearestIndex+r*loncount+radius)
                
                print(cur_min,cur_max)
                curdata=values[cur_min:cur_max+1]
                print(curdata)
                print("-" * 100)
            
            
            
            print("value test：%.10e"%values[nearest.index])
            keyval = codes_get_string(gid, "shortName")
            print("%s = %s" % ("keyname", keyval))
            keyval = codes_get_string(gid, "level")
            print("%s = %s" % ("level", keyval))
            print("-" * 100)
            codes_release(gid)  
           

            
            

           #跳过的部分
            for i in range (1):
                gid = codes_grib_new_from_file(f)
                keyval = codes_get_string(gid, "shortName")
                print("%s = %s" % ("keyname", keyval))
                keyval = codes_get_string(gid, "level")
                print("%s = %s" % ("level", keyval))
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


