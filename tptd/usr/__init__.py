# DO NOT EDIT -->
from pathlib    import Path
from typing     import Tuple
import math

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
    current_enemy = 2#Just update this if you add more towers to be exactly the amount of towers on the field
    enemy_count = len(LoT)-2

    if enemy_count<1:
        return (current_dir, True, False)

    if enemy_count < 8:
        if tag=='2':
            if LoT[current_enemy][2][1] > 0:
                return (268 , True, False)
            else:
                return (177 , True, False)
        else:
            if LoT[current_enemy][2][1] > 0:
                return (267 , True, False)
            else:
                return (174 , True, False)
    else:
        if tag=='2':
            if LoT[current_enemy][2][1] > 0:
                return (268 , True, False)
            else:
                return (current_dir, True, False)
        else:
            if LoT[current_enemy][2][1] > 0:
                return (267 , True, False)
            else:
                return (current_dir, True, False)
    return (current_dir, True, False)




    if enemy_count < 26:
        if tag=='2':
            if LoT[current_enemy][2][1] > 0:
                return (268 , True, False)
            else:
                return (177 , True, False)
        else:
            if LoT[current_enemy][2][1] > 0:
                return (267 , True, False)
            else:
                return (174 , True, False)
    else:#If 26/27 (aka when speedy bois spawn)
        if tag=='2':
                return (268 , True, False)
        else:
                return (267 , True, False)

    return (current_dir, True, False)
    # Some variable initialization for later
    pew_direction_degree = 0

    # You need a check here in case there is no elgible enemies in the area
    if len(LoT)>current_enemy:

        if tag=='2':
            #current_enemy=len(LoT)-1#Basically tell the 2nd tower to always hit last for DPS
            #if LoT[current_enemy][1][1][1]
            if LoT[current_enemy][2][1] > 0:
                #print(LoT[current_enemy][2][1])
                return (268 , True, False)

            return (177 , True, False)

        else:
            if LoT[current_enemy][2][1] > 0:
                return (267 , True, False)
            return (174 , True, False)

        # Grabbing the random variables that we need from LoT
        current_turret_pos = LoT[int(tag)-1][1]
        current_target = LoT[current_enemy]
        current_target_pos = current_target[1]
        current_target_vel = current_target[2]

        # Call to a function that magically does all the calcs
        pew_direction_degree = pre_intersect_prediction(current_turret_pos,current_target_pos,current_target_vel,current_turret_bullet_speed)

#coord, tag : str, LoT : list, fire : bool, current_dir : float, target_dir : float

    return (pew_direction_degree, True, False)

#End-def

def pre_intersect_prediction(pTurret,pTarget,vTarget,bulletVel):

    x1=pTurret[0]/4#X position for bullet/turret
    y1=pTurret[1]/4#Y position for bullet/turret
    x2=pTarget[0]/4#X position for target
    y2=pTarget[1]/4#Y position for target
    vtx=vTarget[0]/4
    vty=vTarget[1]/4
    vb=bulletVel

    if vtx !=0:
        # If the turret is handling a horizontally moving target
        a=vtx**2-vb**2
        b=(2*vtx)*(x2-x1)
        c=((x2-x1)**2)+((y2-y1)**2)

        # Solve with quadratic equation
        t=(-b-((b)**2-4*(a)*(c))**0.5)/(2*(a))
        x4=x2+vtx*t
        theta = math.degrees(math.atan2((y2-y1),(x4-x1)))

    else:
        # If the turret is handling a vertically moving target
        a=vty**2-vb**2
        b=(2*vty)*(y2-y1)
        c=((y2-y1)**2)+((x2-x1)**2)

        # Solve with quadratic equation
        t=(-b-((b)**2-4*(a)*(c))**0.5)/(2*(a))
        y4=y2+vty*t
        theta = 90-math.degrees(math.atan2((x2-x1),(y4-y1)))

    return theta