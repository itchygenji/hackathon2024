# -*- coding: utf-8 -*-
from pygame        import image, Rect, Surface
from pygame.math   import Vector2
from pygame.sprite import spritecollide, OrderedUpdates, Sprite

from abc        import ABC
from functools  import lru_cache
from numbers    import Real
from pathlib    import Path
from typing     import Tuple

GAMEFEET_PER_PIXEL = 10/40

THIS_FOLDER = Path(__file__).parent

BACKGROUND = image.load(THIS_FOLDER / 'Play Area.jpg')

SCREEN_RES = (1024, 1024)

SIM_RATE = 120

MSEC_PER_UPDATE = 1000/SIM_RATE

LEVELS = []

all_base_sprites = OrderedUpdates()

def check_sprite(subj : Sprite, dokill : bool = False) -> set: return set(spritecollide(subj, all_base_sprites, dokill))

class PlayerBase(Sprite):
    
    _instance   = None
    damage      = 0
    next_attack = dict()
    
    def __init__(self): raise RuntimeError('Use instance method')
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            super(PlayerBase, cls._instance).__init__(all_base_sprites)
            cls._instance.image       = image.load(THIS_FOLDER / 'Pill Box.png')
            cls._instance.rect        = Rect(cls._instance.image.get_bounding_rect() )
            cls._instance.rect.center = (SCREEN_RES[0]/2, SCREEN_RES[1]/2)
        return cls._instance
    #End-def
    
    def inc_damage(self): self.damage += 1
#End-class
PLAYER_BASE = PlayerBase.instance()
CENTER      = Vector2(PLAYER_BASE.rect.center)

@lru_cache
def rel_to_pb(v) -> Vector2: return Vector2(v) - CENTER

class TgtSprite(Sprite, ABC):
    
    def __init__(self, name : str, *grps):
        super().__init__(*grps)
        self.__name = name
    #End-def
    
    @property
    def velocity(self) -> Vector2: return Vector2(0, 0)
    
    @property
    def tgt_data(self) -> Tuple[str, Vector2, Vector2]: return str(self), rel_to_pb(self.rect.center), self.velocity
    
    def __str__(self): return self.__name
#End-class

ENEMY_PATH_BASE = [ \
    (    1,  0.8 ), \
    (-0.95,  0.8 ), \
    (-0.95, -0.65), \
    ( 0.85, -0.65), \
    ( 0.85,  0.55), \
    (-0.75,  0.55), \
    (-0.75, -0.5 ), \
    (-0.68 , -0.5 ), \
    (-0.68 ,  0.4 ), \
    ( 0.6 ,  0.4 ), \
    ( 0.6 , -0.02), \
    ( 0.02, -0.02)  \
    ]

@lru_cache
def delta_sign(s, e) -> int:
    if      e > s: return 1
    elif    e < s: return -1
    else:          return 0
#End-def

@lru_cache
def get_dir_tup(nxt_cp_idx : int) -> Tuple[int, int]:
    if (nxt_cp_idx >= 1) and (nxt_cp_idx < len(ENEMY_PATH_BASE) ): return tuple([delta_sign(s, e) for s, e in zip(ENEMY_PATH_BASE[nxt_cp_idx - 1], ENEMY_PATH_BASE[nxt_cp_idx])])
    return (0, 0)
#End-def


ENEMY_PATH_WIDTH        = 33
ENEMY_PATH_WIDTH_HALF   = int(ENEMY_PATH_WIDTH/2) - 1

ENEMY_PATH_PIX = [tuple([int(p*(s+1)/2) for p, s in zip(SCREEN_RES, scl)]) for scl in ENEMY_PATH_BASE]

ENEMY_PATH_CORNERS = [Rect(c - ENEMY_PATH_WIDTH_HALF, r - ENEMY_PATH_WIDTH_HALF, *[ENEMY_PATH_WIDTH]*2) for c, r in ENEMY_PATH_PIX[:-1] ]