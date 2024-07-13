# DO NOT EDIT -->
from pathlib    import Path
from typing     import Tuple
import numpy as np
import math
from datetime import datetime

THIS_FOLDER = Path(__file__).resolve().parent
TWR_POS = []
with open(THIS_FOLDER / 'twr.csv', 'r') as twr_h:
    for ln in twr_h:
        ln_parts = ln.strip().split(',') + [None]
        for idx in range(1, 3): ln_parts[idx] = int(ln_parts[idx])
        TWR_POS += [tuple(ln_parts + [None])]
    #End-for
#End-with
# <-- DO NOT EDIT

def twr_func(coord, tag : str, LoT : list, fire : bool, current_dir : float, target_dir : float) -> Tuple[float, bool, bool]:
    '''
    Add in your turret logic here
    
    Notes:
    - "2D-Vector" == pygame.math.Vector2d using pixels
    - angle == float in degrees
    
    PARAMETERS
    ----------
    coord : 2D-Vector
        Location of the subject tower relative to the home base
    
    tag : str
        An identifier defined by you
    
    LoT : list
        "List of Targets", each entry in this list has the following structure
        - Target Type : str
        - Target Position : 2D-Vector
        - Target Velocity : 2D-Vector
    
    fire : bool
        Indicates whether or not the next round will be fired when chambered
    
    current_dir : angle
        Current bearing of the gun
    
    target_dir : angle
        Target bearing of the gun
    
    RETURNS
    -------
    target_dir
        As defined in `PARAMETERS`
    
    fire
        As defined in `PARAMETERS`
    
    target_dir_is_radians : bool
        Indicates if the output target_dir is in radians
    
    '''

#I'm trying to figure out how to even change the turret direction
    #print("Coord")
    #print(coord)
    #print("List of target")
    #print(LoT)
    #Howitzer bullet speed 50
    #Autocannon bullet speed 70

    # Initializing Variables
    current_turret = 0
    current_enemy = 1
    pew_direction_degree = 0
    current_turret_bullet_speed = 50

    distance2pixel = 0

    # You need a check here in case there is no elgible enemies in the area
    if len(LoT)>1:

        current_turret_pos = LoT[current_turret][1]
        current_target_pos = LoT[current_enemy][1]
        current_target_vel = LoT[current_enemy][2]

        if LoT[current_turret][0]=="basic autocannon":
            current_turret_bullet_speed = 70

        current_distance = distance(current_target_pos, current_turret_pos)
        current_direction_degree = get_degree(current_target_pos, current_turret_pos)

        pew_direction_degree = get_degree(current_target_pos, current_turret_pos)

        #Maybe change to something more accurate in the future
        estimated_distance_time = current_distance / current_turret_bullet_speed
        predicted_target_pos_x = current_target_pos[0] + estimated_distance_time * current_target_vel[0]
        predicted_target_pos_y = current_target_pos[1] + estimated_distance_time * current_target_vel[1]
        predicted_target_pos = [current_target_pos[0],current_target_pos[1]]

    
#coord, tag : str, LoT : list, fire : bool, current_dir : float, target_dir : float


    return (pew_direction_degree, True, False)

#End-def

def get_degree(p1, p2):
    xDif = (p1[0]-p2[0])
    yDif = (p1[1]-p2[1])
    pew_direction_degree = math.degrees(math.atan2(yDif,xDif))
    return pew_direction_degree

def distance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

