import omg, sys, math

bspwad = None
bspmap = None
mapbounds = None

#picknode.c

def pick_node(seg):
    return None

def do_lines_intersect():
    return None

def compute_intersection(outx,outy):
    return None

#makenode.c

def create_node(segs):
    
    temp_node = omg.mapedit.Node()
    
    d_s_data = divide_segs(segs) #divide seg

    temp_node.x_start = d_s_data[0][0] #store data
    temp_node.y_start = d_s_data[0][1]
    temp_node.x_vector = d_s_data[0][2]
    temp_node.y_vector = d_s_data[0][3]

    left_segs = d_s_data[1]
    right_segs = d_s_data[2]

    lsegs_limits = find_limits(left_segs)

    temp_node.left_bbox_left = lsegs_limits[0]
    temp_node.left_bbox_right = lsegs_limits[1]
    temp_node.left_bbox_top = lsegs_limits[2]
    temp_node.left_bbox_bottom = lsegs_limits[3]

    if is_it_convex(left_segs):
        temp_node.left_index = create_node(left_segs)
    else:
        temp_node.left_index = create_ssector(left_segs) | 0x8000


    rsegs_limits = find_limits(right_segs)

    temp_node.right_bbox_left = rsegs_limits[0]
    temp_node.right_bbox_right = rsegs_limits[1]
    temp_node.right_bbox_top = rsegs_limits[2]
    temp_node.right_bbox_bottom = rsegs_limits[3]

    if is_it_convex(right_segs):
        temp_node.right_index = create_node(right_segs)
    else:
        temp_node.right_index = create_ssector(right_segs) | 0x8000

    return temp_node

def divide_segs(segs):
    node_x = mapbounds[0]
    node_y = mapbounds[1]
    node_w = mapbounds[2]
    node_h = mapbounds[3]
    left_segs = []
    right_segs = []
    wat = math.floor(len(segs)/2)
    for i in range(len(segs)):
        if i < wat:
            left_segs.append(segs[i])
        else:
            right_segs.append(segs[i])
    return ((node_x,node_y,node_w,node_h),left_segs,right_segs)

def is_it_convex(segs):

    def get_sector(seg):
        if seg.side==1: return bspmap.sidedefs[bspmap.linedefs[seg.line].back].sector
        return bspmap.sidedefs[bspmap.linedefs[seg.line].front].sector

    sector = get_sector(seg[0])
   
    for s in segs:
        if get_sector(seg) != sector: return True

   #  for(line=ts;line;line=line->next)
   #      {
   #      psx = vertices[line->start].x;
   #      psy = vertices[line->start].y;
   #      pex = vertices[line->end].x;
   #      pey = vertices[line->end].y;
   #      pdx = (psx - pex);                                  /* Partition line DX,DY*/
   #      pdy = (psy - pey);
   #      for(check=ts;check;check=check->next)
   #          {
   #          if(line!=check)
   #              {
   #              lsx = vertices[check->start].x; /* Calculate this here, cos it doesn't*/
   #              lsy = vertices[check->start].y; /* change for all the interations of*/
   #              lex = vertices[check->end].x;       /* the inner loop!*/
   #              ley = vertices[check->end].y;
   #              val = DoLinesIntersect();
   #              if(val&34) return TRUE;
   #              }
   #          }
   #      }

   #  /* no need to split the list: these Segs can be put in a SSector */
   # return FALSE;

def create_ssector(segs):
    new_ssector = omg.mapedit.SubSector()

    new_ssector.seg_a = len(bspmap.segs)
    new_ssector.numsegs = len(segs)

    for s in segs:
        ns = omg.mapedit.Seg()
        ns.vx_a = s.vx_a
        ns.vx_b = s.vx_b
        ns.angle = s.angle
        ns.line = s.line
        ns.side = s.side
        ns.offset = s.offset
        bspmap.segs.append(ns)

    bspmap.ssectors.append(new_ssector)
    return len(bspmap.ssectors)-1

def compute_angle(dx,dy):
   w = math.atan2(dy, dx) * (65536/(math.pi*2));

   if(w<0): w = 65536+w
    
   return w

#bsp.c

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

    if (dx == 0 and dy == 0): print("Trouble in SplitDist {},{}".format(dx,dy))
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
