
# coding: utf-8

# In[13]:


# %load test.py


# In[ ]:


from __future__ import print_function
import traceback
import sys
 
from eccodes import *
 
INPUT = '/home/dp/data/ECMF_DAM/PUB/W_NAFP_C_ECMF_20171108054547_P_C1D11080000110800001'
VERBOSE = 1  # verbose error reporting
missingValue = 1e+20  # A value out of range 
 
def example():
    f = open(INPUT)
    message_count=codes_count_in_file(f) #文件中共有多少message
    print("message count %d" % (message_count))
    
    for i in range (5):
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
        #for i in range(len(values)):
        #   print("%d %.10e" % (i + 1, values[i]))
            #print('%d values found in %s' % (len(values), INPUT))

        #for key in ('max', 'min', 'average'):
           # print('%s=%.10e' % (key, codes_get(gid, key)))
            
            
            
        points = ((60, 60), (60, 61),(60,150),
                  (59.75,60))    
        for lat, lon in points:
            nearest = codes_grib_find_nearest(gid, lat, lon)[0]
            print(lat, lon)
            print(nearest.lat, nearest.lon, nearest.value, nearest.distance,
                  nearest.index)
            print("value test：%.10e"%values[nearest.index])
           
            
            
            

   

            print("-" * 100)
        codes_release(gid)
    #codes_release(gid)
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


