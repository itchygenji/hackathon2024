# DO NOT EDIT -->
from pathlib    import Path
from typing     import Tuple
import numpy as np
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

#I'm trying to figure out how to even change the turret direction
    #print("Coord")
    #print(coord)
    #print("List of target")
    #print(LoT)

    currentTurret = 0
    firstEnemy = 1

    print("current direction")
    print(current_dir)
    
    print("length of list of targets")
    print(len(LoT))

    pewDirectionVector = 0


    if len(LoT)>1:
        print("First target's name")
        print(LoT[1][0])
        print("First target position")
        print(LoT[1][1])
        print("First target velocity")
        print(LoT[1][2])

        print("Coordinate of Current Turret")
        print(coord)
        print("Current direction")
        print(current_dir)
        print("Target direction")
        print(target_dir)

        print(f'Current Turret X: {LoT[currentTurret][1][0]}')
        print(f'Current Enemy X: {LoT[firstEnemy][1][0]}')
        print(f'Current Turret Y: {LoT[currentTurret][1][1]}')
        print(f'Current Enemy Y: {LoT[firstEnemy][1][1]}')

        xDif = (LoT[firstEnemy][1][0]-LoT[currentTurret][1][0])
        yDif = (LoT[firstEnemy][1][1]-LoT[currentTurret][1][1])
        pewDirectionVector = math.degrees(math.atan2(yDif,xDif))

        print(f'pewDirectionVector: {pewDirectionVector}')

    
#coord, tag : str, LoT : list, fire : bool, current_dir : float, target_dir : float



    # print("FAKE COORD POLAR")
    # print(coord.as_polar()[1])




    return (pewDirectionVector, True, False)

#End-def
