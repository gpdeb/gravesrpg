import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

libtcod.console_set_custom_font('dejavu10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'GravesRPG', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

playerx = SCREEN_WIDTH / 2
playery = SCREEN_HEIGHT / 2

def handle_keys():
    global playerx, playery

    key = libtcod.console_wait_for_keypress(True)
    
    #Alt + Enter: toggle fullscreen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    
    #Escape: exit the game
    elif key.vk == libtcod.KEY_ESCAPE:
        return True
    
    #Movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        playery -= 1
        
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        playery += 1
    
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        playerx -= 1
        
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        playerx += 1

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_put_char(con, playerx, playery, '@', libtcod.BKGND_NONE)
    
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()
    
    libtcod.console_put_char(con, playerx, playery, ' ', libtcod.BKGND_NONE)
    
    exit = handle_keys()
    if exit:
        break