import omg, sys
from makenode import *
from picknode import *

bspwad = None
bspmap = None
mapbounds = None

def create_segs():
    output = []

    cur_seg = None
    temp_seg = None
    first_seg = None

    for n in range(len(bspmap.linedefs)):
        l = bspmap.linedefs[n]

        if l.front != -1:
            temp_seg = omg.mapedit.Seg()
            if (cur_seg != None):
                cur_seg.next = temp_seg
                cur_seg = temp_seg
                cur_seg.next = None
            else:
                first_seg = temp_seg
                cur_seg = temp_seg
                cur_seg.next = None
            cur_seg.vx_a = l.vx_a
            cur_seg.vx_b = l.vx_b
            dx = bspmap.vertexes[l.vx_a].x - bspmap.vertexes[l.vx_b].x
            dy = bspmap.vertexes[l.vx_a].y - bspmap.vertexes[l.vx_b].y
            cur_seg.angle = compute_angle(dx,dy)
            cur_seg.line = n
            cur_seg.offset = 0
            cur_seg.side = 0
            output.append(cur_seg)

        if l.front != -1:
            temp_seg = omg.mapedit.Seg()
            if (cur_seg != None):
                cur_seg.next = temp_seg
                cur_seg = temp_seg
                cur_seg.next = None
            else:
                first_seg = temp_seg
                cur_seg = temp_seg
                cur_seg.next = None
            cur_seg.vx_a = l.vx_b
            cur_seg.vx_b = l.vx_a
            dx = bspmap.vertexes[l.vx_b].x - bspmap.vertexes[l.vx_a].x
            dy = bspmap.vertexes[l.vx_b].y - bspmap.vertexes[l.vx_a].y
            cur_seg.angle = compute_angle(dx,dy)
            cur_seg.line = n
            cur_seg.offset = 0
            cur_seg.side = 1
            output.append(cur_seg)
    return output

def find_limits(segs):
    #find limits of a set of segs

    minx = 32767
    maxx = -32767
    miny = 32767
    maxy = -32767

    for s in segs:
        va = bspmap.vertexes[s.vx_a]
        vb = bspmap.vertexes[s.vx_b]

        if va.x < minx: minx = va.x
        if va.x > maxx: maxx = va.x
        if va.y < miny: miny = va.y
        if va.y > maxy: maxy = va.y
        if vb.x < minx: minx = vb.x
        if vb.x > maxx: maxx = vb.x
        if vb.y < miny: miny = vb.y
        if vb.y > maxy: maxy = vb.y

    return (minx,maxx,miny,maxy)

def split_dist(seg):
    dx = (bspmap.vertexes[bspmap.linedefs[seg.line].vx_a].x)-(bspmap.vertexes[seg.vx_a].x)
    dy = (bspmap.vertexes[bspmap.linedefs[seg.line].vx_a].y)-(bspmap.vertexes[seg.vx_a].y)

    if (dx == 0 && dy == 0): print("Trouble in SplitDist {},{}".format(dx,dy))
    t = math.sqrt((dx*dx) + (dy*dy))
    return math.floor(t)

def reverse_nodes(nodelist):
    return None

def create_blockmap():
    return None

# main program!
def bsp():
    tsegs = create_segs() #initally create segs

    global mapbounds
    mapbounds = find_limits(tsegs) #find limits of vertices, store as map limits
    print("Map goes from X ({},{}) Y ({},{})".format(*mapbounds)); 


    num_nodes = 0
    nodelist = create_node(tsegs) #recursively create nodes

    num_pnodes = 0
    pnode_indx = 0
    reverse_nodes(nodelist)

    blockmap_size = create_blockmap()

    # done

def process_map(mapid):
    global bspmap
    bspmap = omg.MapEditor(bspwad.maps[mapid])
    bspmap.segs     = []
    bspmap.ssectors = []
    bspmap.nodes    = []
    bspmap.blockmap = omg.Lump("")
    bspmap.reject   = omg.Lump("")
    bsp()
    bspwad.maps[mapid] = bspmap.to_lumps()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("usage:")
        print ("    pybsp.py input_wad output_path")
    else:
        in_path = sys.argv[1]
        out_path = sys.argv[2]
        bspwad = omg.WAD(in_path)
        #todo: run all maps
        process_map("MAP01")
        bspwad.to_file(out_path)
