# -*- coding: utf-8 -*-
# Internals
from ..enemy     import Enemy
from ..game_data import GAMEFEET_PER_PIXEL, SCREEN_RES, MSEC_PER_UPDATE, check_sprite, OrderedUpdates, TgtSprite, all_base_sprites, PLAYER_BASE

from ..          import utils

# Third party
from pygame        import image, Rect, Surface, transform
from pygame.sprite import Sprite, spritecollideany, collide_mask

# Standard
from enum    import Enum
from marshal import load
from math    import isnan, nan, sqrt, degrees, radians
from pathlib import Path
from random  import random, randrange
from typing  import Union, List, Tuple

THIS_FOLDER = Path(__file__).parent


class Bullet(Sprite):
    
    BULLET_IMG = image.load(THIS_FOLDER / 'bullet.png')
    MUZZLE_VEL = 75*MSEC_PER_UPDATE / (GAMEFEET_PER_PIXEL*1000) # TODO: Slowed to make things interesting, may want to change for different turrets
    
    def __init__(self, spawn : utils.Vector2, offset : float, direction : float):
        super().__init__(all_base_sprites)
        self.image          = utils.init_img_rot(self.BULLET_IMG, direction)
        self.rect           = self.image.get_bounding_rect()
        self.__pos          = spawn + utils.Vector2.from_polar( (offset, direction) )
        self.rect.center    = self.__pos
        self.__vel          = utils.Vector2.from_polar( (self.MUZZLE_VEL, direction) )
    #End-def
    
    def update(self, screen_rect):
        self.__pos          += self.__vel
        self.rect.center     = self.__pos
        
        bKill  = bool(spritecollideany(self, Turret.sp_grp, collide_mask) ) | bool(collide_mask(self, PLAYER_BASE) ) | (not self.rect.colliderect(screen_rect) )
        if not bKill:
            tgt = spritecollideany(self, Enemy.sp_grp, collide_mask)
            if tgt:
                tgt.hit()
                bKill = True
            #End-if
        #End-if
        
        if bKill: self.kill()
    #End-def
#End-class

class Turret(TgtSprite):
    
    sp_grp = OrderedUpdates()
    
    FULL_SIZE           = 40
    HALF_SIZE           = FULL_SIZE/2
    BULLET_SPAWN_DIST   = HALF_SIZE*sqrt(2) + 5 # Might want to up this for larger turrets
    
    UPDATE_FACTOR = 4
    
    def __init__(self, a_type : str, spawn_x : float, spawn_y : float, tag : Union[str, None]): # Need additional argument for USR/SIM phase
        super().__init__(a_type, self.sp_grp)
        if tag: self.tag = tag
        else:   self.tag = str(id(self) )
        self.rect       = Rect(spawn_x - self.HALF_SIZE, spawn_y - self.HALF_SIZE, self.FULL_SIZE, self.FULL_SIZE)
        turrDataDir = THIS_FOLDER / a_type
        self.original_image = image.load(turrDataDir / 'sprite.png')
        # TODO: Should use a ".ini" file instead
        turrData = open(turrDataDir / 'param.bin', 'rb')
        self.acq_range  = load(turrData) / GAMEFEET_PER_PIXEL # ... especially since this isn't being used
        self.rot_speed  = MSEC_PER_UPDATE * load(turrData) / 1000
        self.rpt        = MSEC_PER_UPDATE * load(turrData) / 1000
        turrData.close()
        self.fire          = False
        self.current_dir   = utils.FULL_CIRCLE*(random() - 0.5)
        self.target_dir    = self.current_dir
        self.nf_dir        = 0
        self.image         = utils.init_img_rot(self.original_image, self.current_dir)
        
        self.ticks_since_last_user_update = randrange(self.UPDATE_FACTOR)
        self.round_load                   = 1
        self.cb_q                         = []
        self.waiting_for_tfunc            = False
        self.overrun_ctr                  = 0.0
        self.update_ctr                   = 0.0
    #End-def
    
    # TODO: Need to figure out why this does not line up with the barrel
    def fire_bullet(self): Bullet(utils.Vector2(self.rect.center), self.BULLET_SPAWN_DIST, self.current_dir)
    
    def update(self, all_tgts : Union[List[Tuple], None] = None):
        if all_tgts:
            if self.cb_q:
                self.target_dir, self.fire, in_rad, self.waiting_for_tfunc = self.cb_q.pop(0)
                if isnan(self.target_dir):  self.target_dir = self.current_dir
                elif in_rad:                self.target_dir = degrees(self.target_dir)
                self.target_dir = utils.ang_mod(self.target_dir)
            #End-if
            
            dir_error = utils.ang_mod(self.target_dir - self.current_dir)
            if self.ticks_since_last_user_update == 0:
                self.update_ctr += 1
                if self.waiting_for_tfunc:  self.overrun_ctr += 1
                else:                       utils.twr_func_sched(self, self.tgt_data[1], self.tag, all_tgts, self.fire, self.current_dir, self.target_dir)
                self.waiting_for_tfunc  = True
            #End-if
            self.ticks_since_last_user_update += 1
            self.ticks_since_last_user_update %= self.UPDATE_FACTOR
            
            # Update the current state
            if (dir_error != 0) and (self.nf_dir == 0):
                dir_check = abs(dir_error)
                sign        = dir_error/dir_check
                self.nf_dir = sign*self.rot_speed
            elif abs(dir_error) < abs(self.nf_dir):
                self.nf_dir = 0
                self.current_dir = self.target_dir
            #End-if
            self.current_dir = utils.ang_mod(self.current_dir + self.nf_dir)
            self.image = utils.init_img_rot(self.original_image, self.current_dir) # Has to be done on the **original** image or else the sprite will get corrupted
            self.rect  = self.image.get_rect(center=self.rect.center)
            
            # Fire the next bullet?
            if self.fire and self.round_load >= 1:
                self.fire_bullet()
                self.round_load -= 1
            #End-if
            if self.round_load < 1: self.round_load += self.rpt
        elif self in utils.curr_proc: self.cb_q += [(self.target_dir, self.fire, False, self.waiting_for_tfunc)]
        #End-if
    #End-def
    
    def twr_func_cb(self, args):
        nxt_tgt_dir = args[0]
        if args[-1]: nxt_tgt_dir = degrees(nxt_tgt_dir)
        if args[0] == None: print(f'CRASH: Null direction detected: {args}')
        self.cb_q  += [(*args, False)]
        utils.declare_finish(self)
    #End-def
    
    def err_cb(self, e):
        print(e)
        utils.declare_finish(self)
    #End-def
    
    @property
    def mouse_info(self) -> str: return f'{self.tag} --> {self.current_dir}'
    
    @property
    def overutilization(self) -> float: return self.overrun_ctr/self.update_ctr
#End-class