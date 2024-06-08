# DO NOT EDIT -->
from pathlib    import Path
from typing     import Tuple

THIS_FOLDER = Path(__file__).resolve().parent
TWR_POS = []
with open(THIS_FOLDER / 'twr.csv', 'r') as twr_h:
    for ln in twr_h:
        ln_parts = ln.strip().split(',')
        t_args = [int(ln_parts.pop(0) ) for c in range(2)]
        if ln_parts: t_args += [ln_parts.pop(0)]
        TWR_POS += [tuple(t_args)]
    #End-for
#End-with
# <-- DO NOT EDIT
from random import uniform, choice, randint

def twr_func(coord, tag : str, LoT : list, fire : bool, current_dir : float, target_dir : float) -> Tuple[float, bool, bool]:
    '''
    Add in your turret logic here
    
    Must return the following:
    (target_dir (float), fire (bool), target_dir is in radians (bool) )
    '''
#End-def
