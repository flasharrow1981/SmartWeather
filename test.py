
# coding: utf-8

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
 
    
    while 1:
        gid = codes_grib_new_from_file(f)
        if gid is None:
            break
 
        codes_set(gid, "missingValue", missingValue)
 
        iterid = codes_grib_iterator_new(gid, 0)


        i = 0
        while 1:
            result = codes_grib_iterator_next(iterid)
            if not result:
                break
 
            [lat, lon, value] = result
            sys.stdout.write("-iterid= %d - " % (iterid))

            sys.stdout.write("- %d - lat=%.6e lon=%.6e value=" % (i, lat, lon))
 
            if value == missingValue:
                print("missing")
            else:
                print("%.6f" % value)
 
            i += 1
 
        codes_grib_iterator_delete(iterid)
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

