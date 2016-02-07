import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

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
        if not map[self.x + dx][self.y + dy].blocked:
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

        

class Rect:
    #A rectangular room
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
    
    def intersect(self, other):
        #Check if this and another Rect intersect
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
        
        
        
def make_map():
    global map, player
    
    #Fill map with blocked tiles
    map = [[ Tile(True)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
    
    #Dungeon generation
    rooms = []
    num_rooms = 0
    
    for r in range(MAX_ROOMS):
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)
        
        new_room = Rect(x, y, w, h)
        
        #Check if the room intersects with any others
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        
        if not failed:
            create_room(new_room)
            (new_x, new_y) = new_room.center()
            
            if num_rooms == 0:
                #Spawn the player in the center of the first room
                player.x = new_x
                player.y = new_y
            else:
                #Connect subsequent rooms to the previous with tunnels
                
                #Center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms - 1].center()
                
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #First go horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    #First go vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, new_x)
                    create_h_tunnel(prev_x, new_x, prev_y)
            
            rooms.append(new_room)
            num_rooms += 1
        
        
        
def create_room(room):
    global map
    #Make each tile in the rectangle passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False
            
            
            
def create_h_tunnel(x1, x2, y):
    global map
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False



def create_v_tunnel(y1, y2, x):
    global map
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
        
        
        
def render_all():
    #Draw all objects
    for object in objects:
        object.draw()
    
    #Draw the map
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
    
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        
        
        
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

player = Object(25, 23, '@', libtcod.white)
objects = [player]

make_map()

while not libtcod.console_is_window_closed():

    render_all()
    
    libtcod.console_flush()
    
    #Erase all objects before they move
    for object in objects:
        object.clear()
    
    exit = handle_keys()
    if exit:
        break