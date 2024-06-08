# -*- coding: utf-8 -*-
from ..game_data    import GAMEFEET_PER_PIXEL, SCREEN_RES, MSEC_PER_UPDATE, all_base_sprites, TgtSprite, ENEMY_PATH_PIX, get_dir_tup, PLAYER_BASE

from ..utils import Vector2

from pygame        import image, Rect, Surface
from pygame.sprite import Group, collide_mask

from enum    import Enum
from math    import sqrt
from marshal import load
from pathlib import Path

global PLAYER_BASE

THIS_FOLDER     = Path(__file__).parent
SEC_PER_UPDATE  = MSEC_PER_UPDATE / 1000

class Enemy(TgtSprite):
    # TODO [Velocity]: Remember that movement is constrained to horizontal and vertical.
    sp_grp = Group()
    killed = 0

    def __init__(self, a_type : str):
        super().__init__(a_type, all_base_sprites, self.sp_grp)
        self.__pos       = Vector2(ENEMY_PATH_PIX[0])
        turrDataDir      = THIS_FOLDER / a_type
        self.image       = image.load(turrDataDir / 'sprite.png')
        self.rect        = self.image.get_bounding_rect()
        self.rect.center = self.__pos
        self.__nxt_chkpkt_idx  = 1
        # TODO: Should use a ".ini" file instead
        with open(turrDataDir / 'param.bin', 'rb') as turrData:
            self.__hp       = load(turrData)
            self.__frm_spd  = SEC_PER_UPDATE * load(turrData) / GAMEFEET_PER_PIXEL
        #End-with
    #End-def
    
    def update(self, _):
        nxt_cp_vec = Vector2(ENEMY_PATH_PIX[self.__nxt_chkpkt_idx])
        dgo = nxt_cp_vec - self.__pos
        if dgo.magnitude() < self.__frm_spd:
            self.__pos               = nxt_cp_vec
            self.__nxt_chkpkt_idx   += 1
            self.__pos              += (self.__frm_spd - dgo.magnitude() )*Vector2(get_dir_tup(self.__nxt_chkpkt_idx) )
        else: self.__pos += self.__frame_dpix
        #End-if
        self.rect.center = self.__pos
        if collide_mask(self, PLAYER_BASE):
            PLAYER_BASE.inc_damage()
            self.kill()
        #End-if
    #End-def
    
    @classmethod
    def reg_kill(cls): cls.killed += 1
    
    def hit(self, damage : int = 1):
        self.__hp -= damage
        if self.__hp <= 0:
            self.reg_kill()
            self.kill()
        #End-if
    #End-def
    
    @property
    def __frame_dpix(self): return Vector2(*[self.__frm_spd*c_ for c_ in get_dir_tup(self.__nxt_chkpkt_idx)])
    
    @property
    def velocity(self): return self.__frame_dpix / SEC_PER_UPDATE
#End-class