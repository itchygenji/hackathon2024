# -*- coding: utf-8 -*-
# Internals
from ..enemy     import Enemy
from ..game_data import GAMEFEET_PER_PIXEL, SCREEN_RES, MSEC_PER_UPDATE, check_sprite, OrderedUpdates, TgtSprite, all_base_sprites, PLAYER_BASE

from ..          import utils

# Third party
from pygame        import image, Rect, Surface, transform
from pygame.sprite import Sprite, spritecollideany, collide_mask

# Standard
from configparser import ConfigParser
from functools    import lru_cache, cached_property

from enum    import Enum
from math    import isnan, nan, sqrt, degrees, radians
from pathlib import Path
from random  import random, randrange
from typing  import Union, List, Tuple

THIS_FOLDER     = Path(__file__).parent
SEC_PER_UPDATE  = MSEC_PER_UPDATE / 1000
VEL_SCALE       = SEC_PER_UPDATE / GAMEFEET_PER_PIXEL

class Bullet(Sprite):
    
    BULLET_IMG = image.load(THIS_FOLDER / 'bullet.png')
    
    def __init__(self, spawn : utils.Vector2, offset : float, direction : float, muzzle_vel : float = 75, damage : int=1):
        super().__init__(all_base_sprites)
        self.image          = utils.init_img_rot(self.BULLET_IMG, direction)
        self.rect           = self.image.get_bounding_rect()
        self.__pos          = spawn + utils.Vector2.from_polar( (offset, direction) )
        self.rect.center    = self.__pos
        self.__vel          = utils.Vector2.from_polar( (muzzle_vel*VEL_SCALE, direction) )
        self.__dmg          = damage
    #End-def
    
    def update(self, screen_rect):
        self.__pos          += self.__vel
        self.rect.center     = self.__pos
        
        bKill  = bool(spritecollideany(self, Turret.sp_grp, collide_mask) ) | bool(collide_mask(self, PLAYER_BASE) ) | (not self.rect.colliderect(screen_rect) )
        if not bKill:
            tgt = spritecollideany(self, Enemy.sp_grp, collide_mask)
            if tgt:
                tgt.hit(self.__dmg)
                bKill = True
            #End-if
        #End-if
        
        if bKill: self.kill()
    #End-def
#End-class


@lru_cache
def get_ini_data(ini_path : Path, section : str = 'DEFAULT'):
    CFG_PARSE = ConfigParser()
    CFG_PARSE.read(ini_path)
    return CFG_PARSE[section]
#End-def

class Turret(TgtSprite):
    '''
    Base class for the player-defined turrets
    '''
    sp_grp    = OrderedUpdates()
    
    UPDATE_FACTOR = 4
    
    @staticmethod
    def get_type_data(a_type : str) -> dict:
        turrDataDir = THIS_FOLDER / a_type
        result = {'original_image' : image.load(turrDataDir / 'sprite.png') }
        ini_data = get_ini_data(turrDataDir / 'data.ini')
        for k in ['bullet_dmg', 'tpr']: result[k] = int(ini_data[k])
        for k in ['rot_speed', 'bullet_speed']: result[k] = float(ini_data[k])
        result['rot_speed'] *= SEC_PER_UPDATE
        return result
    #End-def
    
    def __init__(self, a_type : str, spawn_x : float, spawn_y : float, tag : Union[str, None]):
        '''
        Spawns a new turrent
        
        PARAMETERS
        ----------
        a_type : str
            Type of turret being spawned, should be named under the folder containing this script
        
        spawn_x, spawn_y : pixel
            Location of the turret
        
        tag : str or None
            A user-defined identifier if provided
        '''
        super().__init__(a_type, self.sp_grp)
        if tag: self.tag = tag
        else:   self.tag = str(id(self) )
        for at, v in self.get_type_data(a_type).items(): setattr(self, at, v)
        self.rect       = Rect(spawn_x - self.__half_size, spawn_y - self.__half_size, *([self.__full_size]*2) )
        
        self.fire          = False
        _, sp_pos, _       = self.tgt_data
        self.current_dir   = sp_pos.as_polar()[1]
        self.target_dir    = self.current_dir
        self.image         = utils.init_img_rot(self.original_image, self.current_dir)
        
        self.ticks_since_last_user_update = randrange(self.UPDATE_FACTOR)
        self.ttnr                         = 0
        self.cb_q                         = []
        self.waiting_for_tfunc            = False
        self.overrun_ctr                  = 0.0
        self.update_ctr                   = 0.0
    #End-def
    
    @cached_property
    def __full_size(self): return self.original_image.get_width()
    
    @cached_property
    def __half_size(self): return self.__full_size/2
    
    @cached_property
    def __bullet_spawn_dist(self): return self.__half_size*sqrt(2) + 5
    
    def fire_bullet(self): Bullet(utils.Vector2(self.rect.center), self.__bullet_spawn_dist, self.current_dir, self.bullet_speed, self.bullet_dmg)
    
    def update(self, all_tgts : Union[List[Tuple], None] = None):
        '''
        [pygame] Update function
        
        PARAMETERS
        ----------
        all_tgts : List[Tuple], None
            Passed into the user-defined twr_func as the `LoT`
        '''
        if all_tgts:
            if self.cb_q:
                self.target_dir, self.fire, in_rad, self.waiting_for_tfunc = self.cb_q.pop(0)
                if isnan(self.target_dir):  self.target_dir = self.current_dir
                elif in_rad:                self.target_dir = degrees(self.target_dir)
                self.target_dir = utils.ang_mod(self.target_dir)
            #End-if
            
            if self.ticks_since_last_user_update == 0:
                self.update_ctr += 1
                if self.waiting_for_tfunc:  self.overrun_ctr += 1
                else:                       utils.twr_func_sched(self, self.tgt_data[1], self.tag, all_tgts, self.fire, self.current_dir, self.target_dir)
                self.waiting_for_tfunc  = True
            #End-if
            self.ticks_since_last_user_update += 1
            self.ticks_since_last_user_update %= self.UPDATE_FACTOR
            
            # Update the current state
            dir_error = utils.ang_mod(self.target_dir - self.current_dir)
            if  abs(dir_error) > abs(self.rot_speed):
                if dir_error < 0: dir_error = -self.rot_speed
                else:             dir_error =  self.rot_speed
            #End-if
            self.current_dir = utils.ang_mod(self.current_dir + dir_error)
            self.image = utils.init_img_rot(self.original_image, self.current_dir) # Has to be done on the **original** image or else the sprite will get corrupted
            self.rect  = self.image.get_rect(center=self.rect.center)
            
            # Fire the next bullet?
            tick = 0
            if self.ttnr: tick = 1
            elif self.fire:
                self.fire_bullet()
                tick = 1
            #End-if
            self.ttnr = (self.ttnr + tick) % self.tpr
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
        print(f'**Error ({self.tag}): {e}')
        utils.declare_finish(self)
    #End-def
    
    @property
    def mouse_info(self) -> str: return f'{self.tag} --> {self.current_dir}'
    
    @property
    def overutilization(self) -> float: return self.overrun_ctr/self.update_ctr
#End-class