import omg, sys
from makenode import *
from picknode import *

bspwad = None
bspmap = None

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

    # you know how to do this

    return (x1,x2,y1,y2) # or something

def split_dist(seg):
    return None

def reverse_nodes(nodelist):
    return None

def create_blockmap():
    return None

# main program!
def bsp():
    tsegs = create_segs()

    limits = find_limits(tsegs)

    # mapminx = lminx
    # mapmaxx = lmaxx
    # mapminy = lminy
    # mapmaxy = lmaxy

    num_nodes = 0
    nodelist = create_node(tsegs)

    num_pnodes = 0
    pnode_indx = 0
    reverse_nodes(nodelist)

    # write built data here with omgifol, or have already done so in functions

    # end write

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
