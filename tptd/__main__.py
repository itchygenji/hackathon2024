# -*- coding: utf-8 -*-
from .src.asset     import Turret
from .src.enemy     import Enemy
from .src.game_data import *
from .src           import utils
from .usr           import TWR_POS

import pygame

from functools  import lru_cache
from pathlib    import Path
from sys        import argv
from typing     import List

THIS_FOLDER = Path(__file__).parent

global PLAYER_BASE


# initializing the constructor 
pygame.init() 

# screen resolution
SCREEN_RES = (1024,1024) 

# opens up a window 
screen = pygame.display.set_mode(SCREEN_RES) 
  
# white color 
color = (255,255,255) 
  
# light shade of the button 
color_light = (170,170,170) 
  
# dark shade of the button 
color_dark = (100,100,100) 

# path color
path_color = (152,118,84)

# defining a font 
smallfont = pygame.font.SysFont('Corbel',35)

@lru_cache
def gen_txt_img(txt : str) -> pygame.Surface: return smallfont.render(txt, True, color)

TXT_OFFSET = utils.Vector2(5, 5)
def draw_txt(txt : str, pos : utils.Vector2): screen.blit(gen_txt_img(txt), pos + TXT_OFFSET)

pygame.time.set_timer(pygame.USEREVENT, int(MSEC_PER_UPDATE) )

loop_count   = 0
SHELL_UPDATE = 50

def draw_enemy_path() -> List[pygame.rect.Rect]:
    for c_r in ENEMY_PATH_CORNERS: pygame.draw.rect(screen, path_color, c_r)
    return [pygame.draw.line(screen, path_color, start_pix, end_pix, ENEMY_PATH_WIDTH) for start_pix, end_pix in zip(ENEMY_PATH_PIX[:-1], ENEMY_PATH_PIX[1:])] + ENEMY_PATH_CORNERS
#End-def

bad_twr_rects = []

enemy_wave = [ [100, 'Evil Spider'] for i in range(10)]
curr_enemy = enemy_wave.pop(0)

num_twr         = 0
final_score_msg = ''

if __name__ == '__main__':
    path_rects = draw_enemy_path()
    for twr in TWR_POS:
        curr_twr = Turret('Basic Autocannon', twr[0] + PLAYER_BASE.rect.centerx, twr[1] + PLAYER_BASE.rect.centery, *twr[2:])
        if curr_twr.rect.collidelist(path_rects) >= 0:
            print(f'Cannot spawn tower at position: {curr_twr.rect.center}')
            curr_twr.kill()
        else: num_twr += 1
        #End-if
    #End-for
    game_over = False
    while not game_over:
          
        for ev in pygame.event.get(): 
              
            if ev.type == pygame.QUIT: game_over = True
            
            match ev.type:
                case pygame.USEREVENT:
                    if utils.blocked: Turret.sp_grp.update()
                    else:
                        Turret.sp_grp.update([tgt.tgt_data for tgt in (Turret.sp_grp.sprites() + Enemy.sp_grp.sprites() )])
                        all_base_sprites.update(screen.get_rect() )
                        curr_enemy[0] -= 1
                        if curr_enemy[0] == 0:
                            Enemy(curr_enemy[1])
                            if enemy_wave: curr_enemy = enemy_wave.pop(0)
                            else:          curr_enemy = [-1, '']
                        #End-if
                    #End-if
                #End-case
            #End-match
        #End-for
                    
        screen.blit(BACKGROUND, (0,0) )
        draw_enemy_path()
        Turret.sp_grp.draw(screen)
        all_base_sprites.draw(screen)
        
        all_twr = Turret.sp_grp.sprites()
        mouse_pos = pygame.mouse.get_pos()
        mouse_chk = None
        while all_twr:
            curr_twr = all_twr.pop()
            if curr_twr.rect.collidepoint(mouse_pos):
                mouse_chk = curr_twr.mouse_info
                all_twr   = []
            #End-if
        #End-while
        if mouse_chk: draw_txt(mouse_chk, mouse_pos)

        # updates the frames of the game 
        pygame.display.flip()
        
        if not (bool(enemy_wave) or bool(Enemy.sp_grp.sprites() ) ):
            game_over       = True
            final_score_msg = f'''
            Towers Deployed:        {num_twr}
            Enemies neutralized:    {Enemy.killed}
            Enemies survided:       {PLAYER_BASE.damage}
            --------------------------------
            FINAL SCORE:            {5*Enemy.killed - PLAYER_BASE.damage - 10*num_twr}
            '''
        #End-if
    #End-while
    
    pygame.quit()
    print(final_score_msg)
#End-if