# compare the results of pybsp and bsp.exe against map01 of doom2

import os, omg, time

def compare_maps(map1,map2):
    checks = ["vertexes","linedefs","sidedefs","sectors","segs","ssectors","nodes"]
    for c in checks:
        if len(getattr(map1,c)) == len(getattr(map2,c)):
            print ("{} matches".format(c))
        else:
            print("*{} doesn't match*".format(c))

bsp_start = time.time()
os.system("bsp.mscl.exe test-built.wad output-bsp.wad")
bsp_end = time.time()
pybsp_start = time.time()
os.system("python pybsp.py test-built.wad output-pybsp.wad")
pybsp_end = time.time()

print("bsp.exe time: {}".format(bsp_end-bsp_start))
print("pybsp.py time: {}".format(pybsp_end-pybsp_start))



wad1 = omg.WAD("output-bsp.wad")
wad2 = omg.WAD("output-pybsp.wad")
map1 = omg.MapEditor(wad1.maps["MAP01"])
map2 = omg.MapEditor(wad2.maps["MAP01"])

compare_maps(map1,map2)