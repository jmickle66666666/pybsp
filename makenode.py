import math

def create_node():
    return None

def divide_segs(temp_seg,right_seg,left_seg):
    return None

def is_it_convex(seg):
    return None

def create_ssector(seg):
    return None

def compute_angle(dx,dy):
   w = math.atan2(dy, dx) * (65536/(math.pi*2));

   if(w<0): w = 65536+w
    
   return w