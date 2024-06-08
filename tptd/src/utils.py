# -*- coding: utf-8 -*-
# Internals
from ..usr  import twr_func

# Third-party
from pygame import Rect, Surface, transform
from pygame.math import Vector2

# Standard Library
from functools              import lru_cache
from math                   import radians, cos, sin
from multiprocessing.pool   import Pool
from os                     import cpu_count

FULL_CIRCLE    = 360
HALF_CIRCLE    = FULL_CIRCLE/2
QTR_CIRCLE     = FULL_CIRCLE/4
IM_ROT         = 3*QTR_CIRCLE

@lru_cache
def init_img_rot(img : Surface, rot : float) -> Surface: return transform.rotate(img, IM_ROT - rot)

def cosd(deg : float) -> float: return cos(radians(deg) )
def sind(deg : float) -> float: return sin(radians(deg) )

@lru_cache
def ang_mod(deg : float) -> float:
    if      deg >  HALF_CIRCLE: return ang_mod(deg - FULL_CIRCLE)
    elif    deg < -HALF_CIRCLE: return ang_mod(deg + FULL_CIRCLE)
    return deg
#End-def

MAX_PROC  = cpu_count() - 3
mp_pool   = Pool(MAX_PROC)
curr_proc = dict()
blocked   = []

def check_pool() -> bool: return len(curr_proc) < MAX_PROC

def apply_call(obj, args : tuple):
    if obj not in curr_proc:    curr_proc[obj] = mp_pool.apply_async(twr_func, args, callback=obj.twr_func_cb, error_callback=obj.err_cb)
#End-def

def declare_finish(obj):
    del curr_proc[obj]
    if blocked: apply_call(*blocked.pop(0) )
#End-def

def twr_func_sched(obj, *args): # Leave as generic to avoid circular imports
    if check_pool():    apply_call(obj, args)
    else:               blocked += [(obj, args)]
#End-def