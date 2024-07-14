# DO NOT EDIT -->
from pathlib    import Path
from typing     import Tuple
import numpy as np
import math
import datetime
from termcolor import colored

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

    print(f'tag IS:',tag)
    # Initializing Variables

    current_enemy = 2#Just update this if you add more towers to be exactly the amount of towers on the field
    if tag=='2':
        print("Going sicko mode")
        current_enemy=len(LoT)-1
    pew_direction_degree = 0
    current_turret_bullet_speed = 50
    current_turret_rotation_speed=55
    feet_to_pixel=10/40
    distance2pixel = 0

    # You need a check here in case there is no elgible enemies in the area
    if len(LoT)>current_enemy:

        current_turret_pos = LoT[int(tag)-1][1]
        current_target_pos = LoT[current_enemy][1]
        current_target_vel = LoT[current_enemy][2]

        if LoT[int(tag)-1][0]=="basic autocannon":#howitzer
            current_turret_bullet_speed = 70#howitzer is 50
            current_turret_rotation_speed=300#howitzer is 55

        current_distance = distance(current_target_pos, current_turret_pos)
        current_direction_degree = get_degree(current_target_pos, current_turret_pos)

        # pew_direction_degree = get_degree(current_target_pos, current_turret_pos)

        # #Maybe change to something more accurate in the future
        # estimated_distance_time = current_distance / current_turret_bullet_speed

        # We gotta do some funky math here boss
        # What we know = turret position, turret velocity(0),arget position, target velocity
        # predicted_target_pos_x = current_target_pos[0] + estimated_distance_time * current_target_vel[0] / feet_to_pixel
        # predicted_target_pos_y = current_target_pos[1] + estimated_distance_time * current_target_vel[1] / feet_to_pixel
        # predicted_target_pos = [current_target_pos[0],current_target_pos[1]]

        pew_direction_degree = pre_intersect_prediction(current_turret_pos,current_target_pos,current_target_vel,current_turret_bullet_speed)

    #print(colored('HEY HEY HEY','red'))
    
    
#coord, tag : str, LoT : list, fire : bool, current_dir : float, target_dir : float
    if (abs(current_dir-pew_direction_degree) > current_turret_rotation_speed):

        death = str(abs(current_dir-pew_direction_degree))
        print(colored('MAYDAY MAYDAY MAYDAY MAX GIMBAL LIMIT HIT '+death,'red'))


    return (pew_direction_degree, True, False)

#End-def

def get_degree(p1, p2):
    xDif = (p1[0]-p2[0])
    yDif = (p1[1]-p2[1])
    pew_direction_degree = math.degrees(math.atan2(yDif,xDif))
    return pew_direction_degree

def distance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def pre_intersect_prediction(pTurret,pTarget,vTarget,bulletVel):

    print("**********************************NEW FRAME**********************************")
    # #Velocity Data in PIXELS from pygame
    print(f'pTurret:',pTurret)
    print(f'pTarget:',pTarget)
    print(f'vTarget:',vTarget)
    print(f'bulletVel',bulletVel)

    x1=pTurret[0]/4#X position for bullet/turret
    y1=pTurret[1]/4#Y position for bullet/turret
    x2=pTarget[0]/4#X position for target
    y2=pTarget[1]/4#Y position for target
    vtx=vTarget[0]/4
    vty=vTarget[1]/4
    vb=bulletVel
    theta = 0

    shootEarlier=1
    # print("HARD CODED UNITS ")
    # x1=-100
    # x2=322
    # y1=0
    # y2=409
    # vtx=-100
    # vb=45

    # print((-2*vtx)*(x2-x1))
    # print(-((2*vtx*(x2-x1))**2-4*(vtx**2-vb**2)*((x2-x1)**2)+(y2-y1)**2)**0.5)
    # print((2*vtx*(x2-x1))**2)
    # print(-4*(vtx**2-vb**2)*(((x2-x1)**2)+(y2-y1)**2))
    if vtx !=0:
        # If the target has a x velocity
        if vtx > 0:
            print("")
        else:
            if x1 < x2 :#Basically if the target is to the right of the turret
                if y2==409/4:#Basically if you are on the first line path
                    shootEarlier=1
                    print("BOT")
                else:
                    print("")
                    shootEarlier=1
            else:
                print("")
        print("EEEEEEEEEEEEEEEEE")
        a=vtx**2-vb**2
        b=(2*vtx)*(x2-x1)
        c=((x2-x1)**2)+((y2-y1)**2)

        t=(-b-((b)**2-4*(a)*(c))**0.5)/(2*(a))
        x4=x2+vtx*t*shootEarlier
        theta = math.degrees(math.atan2((y2-y1),(x4-x1)))
        
        # print("TARGET MOVING IN THE X DIRECTION")
        # print(f't:',t)
        # print(f'x2:',x2)
        # print(f'x1:',x1)
        # print(f'PREDICTION/x4=x2+vtx*t(OG target path):',x4)
        # print(f'PREDICTION/x4=x1+vb*cos(theta in rad)(OG bullet path)',x1+t*vb*math.cos(math.radians(theta)))
        # print(f'theta:',theta) 

    else:
        # If the target has a y velocity
        if vty > 0:
            print("")
        else:
            if y1 < y2 :#Basically if the target is to the below of the turret(yaxis is reversed)
                if y2==409/4:#Basically if you are on the first line path
                    shootEarlier=1
                    print("")
                else:
                    print("")
                    shootEarlier=1
            else:
                print("")

        a=vty**2-vb**2
        b=(2*vty)*(y2-y1)
        c=((y2-y1)**2)+((x2-x1)**2)

        t=(-b-((b)**2-4*(a)*(c))**0.5)/(2*(a))
        y4=y2+vty*t*shootEarlier
        theta = 90-math.degrees(math.atan2((x2-x1),(y4-y1)))

        
        print("TARGET MOVING IN THE Y DIRECTION")
        print(f't:',t)
        print(f'y2:',y2)
        print(f'y1:',y1)
        print(f'PREDICTION/x4=x2+vtx*t(OG target path):',y4)
        print(f'PREDICTION/x4=x1+vb*cos(theta in rad)(OG bullet path)',y1+t*vb*math.sin(math.radians(theta)))
        print(f'theta:',theta) 



    
    
    return theta

    # now = datetime.datetime.now()
    # print("**********************************NEW FRAME**********************************")
    # print(f'Current Time:',now)

    # #Velocity Data in PIXELS from pygame
    # print(f'pTurret:',pTurret)
    # print(f'pTarget:',pTarget)
    # print(f'vTarget:',vTarget)
    # print(f'bulletVel',bulletVel)
    
    # feet_to_pixel=10/40
    # #30 Hertz sim
    # xb0=pTurret[0]
    # xt0=pTarget[0]
    # yb0=pTurret[1]
    # yt0=pTarget[1]
    # h=xt0-xb0
    # print(f'h:',h)

    # vtx=vTarget[0]
    # vty=vTarget[1]

    # angle = 0

    # if vtx != 0:
    #     #Basically if the current target is moving horizontally and below
    #     print(f'vtx:',vtx)
    #     print(f'xb0:',xb0)
        
    #     #Super goofy equation that was derived
    #     t=(-2*xt0*vtx-((2*xt0*vtx)**2-4*(vtx**2-bulletVel**2)*(xt0**2+abs(yt0-yb0)**2))**0.5)/(2*(vtx**2-bulletVel**2))
    #     xPredict=xt0+vtx*t
    #     print(f't:',t)  
    #     print(f'PREDICTION:',xPredict)
    #     print(yt0-yb0)
    #     angle = math.degrees(math.atan2(abs(yt0-yb0),xPredict))
    #     print(f'ANGLE:',angle)
    #     print(angle)
    # else:
    #     print("HALT")

    #return angle


