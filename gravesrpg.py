import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

#A generic game object. A person, an item, an enemy, etc
class Object:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw(self):
        #Set the object's color and draw the character at the object's position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
        
    def clear(self):
        #Erase the character that represents the object from the screen
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)



class Tile:
    #A map tile
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        
        #A blocked tile also blocks sight by default
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

        

def make_map():
    global map
    
    #Fill map with empty floor tiles
    map = [[ Tile(False)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
        
        
        
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
        player.move(0, -1)
        
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)
    
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)
        
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)

        
        
#Initialize the game and start the main loop
libtcod.console_set_custom_font('dejavu10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'GravesRPG', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

player = Object(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, '@', libtcod.white)
npc = Object(SCREEN_WIDTH / 2 - 5, SCREEN_HEIGHT / 2, '@', libtcod.yellow)

objects = [npc, player]

while not libtcod.console_is_window_closed():

    #Draw all objects
    for object in objects:
        object.draw()
    
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()
    
    #Erase all objects before they move
    for object in objects:
        object.clear()
    
    exit = handle_keys()
    if exit:
        break