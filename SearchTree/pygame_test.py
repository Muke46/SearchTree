from math import sqrt
import os.path
import pygame as pg

# Place a picture called "sheet.png" in the same folder as this program!
# Zoom with mousewheel, pan with left mouse button
# Print a snapshot of the screen with "P"

sprite_sheet = pg.image.load('D:\\Files\\Git\\SearchTree\\SearchTree\\map2.png')
SCREEN_WIDTH = sprite_sheet.get_rect().size[0]
SCREEN_HEIGHT = sprite_sheet.get_rect().size[1]
screen = pg.display.set_mode((1600, 900))
clock = pg.time.Clock()
zoom_event = False
scale_up = 1.2
scale_down = 0.8

map=dict()
pos=dict()
lst=[]
circle_radious=10
start=(0,0)
startNode=None
index=0

class GameState:
    def __init__(self):
        self.tab = 1
        self.zoom = 0.5
        self.world_offset_x = 0
        self.world_offset_y = 0
        self.update_screen = True
        self.panning = False
        self.pan_start_pos = None
        self.draw_line = False
        self.legacy_screen = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


game_state = GameState()


def world_2_screen(world_x, world_y):
    screen_x = (world_x - game_state.world_offset_x) * game_state.zoom
    screen_y = (world_y - game_state.world_offset_y) * game_state.zoom
    return [screen_x, screen_y]


def screen_2_world(screen_x, screen_y):
    world_x = (screen_x / game_state.zoom) + game_state.world_offset_x
    world_y = (screen_y / game_state.zoom) + game_state.world_offset_y
    return [world_x, world_y]

def isOnNode(x,y):
    for name,coords in pos.items():
        if(sqrt(pow(coords[0]-x,2)+pow(coords[1]-y,2)))<circle_radious*2:
            return name
    return None

# game loop
loop = True
while loop:
    # Banner FPS
    pg.display.set_caption('(%d FPS)' % (clock.get_fps()))
    # Mouse screen coords
    mouse_x, mouse_y = pg.mouse.get_pos()

    world_left, world_top = screen_2_world(0, 0)
    mouse_x1=mouse_x/game_state.zoom+world_left
    mouse_y1=mouse_y/game_state.zoom+world_top
    

    # event handler
    for event in pg.event.get():
        mouse_x1=mouse_x/game_state.zoom+world_left
        mouse_y1=mouse_y/game_state.zoom+world_top
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if game_state.tab == 1:
                    game_state.tab = 2
                elif game_state.tab == 2:
                    game_state.tab = 1
            elif event.key == pg.K_p:
                pg.image.save(screen, "NEW.png")

        elif event.type == pg.MOUSEBUTTONDOWN: #Right button
            if event.button == 4 or event.button == 5:
                # X and Y before the zoom
                mouseworld_x_before, mouseworld_y_before = screen_2_world(mouse_x, mouse_y)

                # ZOOM IN/OUT
                if event.button == 4 and game_state.zoom < 10:
                    game_state.zoom *= scale_up
                elif event.button == 5 and game_state.zoom > 0.5:
                    game_state.zoom *= scale_down

                # X and Y after the zoom
                mouseworld_x_after, mouseworld_y_after = screen_2_world(mouse_x, mouse_y)

                # Do the difference between before and after, and add it to the offset
                game_state.world_offset_x += mouseworld_x_before - mouseworld_x_after
                game_state.world_offset_y += mouseworld_y_before - mouseworld_y_after

            elif event.button == 2:
                # PAN START
                game_state.panning = True
                game_state.pan_start_pos = mouse_x, mouse_y

            elif event.button == 1:
                n=isOnNode(mouse_x1,mouse_y1)
                if n != None:
                    game_state.draw_line=True
                    start=(mouse_x1,mouse_y1)
                    startNode=n

                else:
                    pos[index]=(mouse_x1,mouse_y1)
                    map[index]=[]
                    index+=1

            elif event.button ==3 :
                n=isOnNode(mouse_x1,mouse_y1)
                if n != None:
                    del pos[n]
                    del map[n]
                    for st,end in map.items(): #remove all transitions
                        if n in end:
                            end.remove(n)

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 2 and game_state.panning:
                # PAN STOP
                game_state.panning = False
            if event.button == 1 and game_state.draw_line:
                # DRAW STOP
                game_state.draw_line = False
                n=isOnNode(mouse_x1,mouse_y1)
                if n != None:
                    map[n].append(startNode)
                    map[startNode].append(n)



    if game_state.panning:# Pans the screen if the left mouse button is held
        game_state.world_offset_x -= (mouse_x - game_state.pan_start_pos[0]) / game_state.zoom
        game_state.world_offset_y -= (mouse_y - game_state.pan_start_pos[1]) / game_state.zoom
        game_state.pan_start_pos = mouse_x, mouse_y

    # Draw the screen
    if game_state.tab == 1:
        # Sets variables for the section of the legacy screen to be zoomed
        world_left, world_top = screen_2_world(0, 0)
        world_right, world_bottom = SCREEN_WIDTH/game_state.zoom, SCREEN_HEIGHT/game_state.zoom
        game_state.legacy_screen.blit(sprite_sheet, (0, 0))
        mouse_x1=mouse_x/game_state.zoom+world_left
        mouse_y1=mouse_y/game_state.zoom+world_top
        if game_state.draw_line:
            start_x=start[0]/game_state.zoom+world_left
            start_y=start[1]/game_state.zoom+world_left
            pg.draw.line(game_state.legacy_screen, (0,0,255),start,(mouse_x1,mouse_y1),8)
        for st,end in map.items():
            for el in map[st]:
                pg.draw.line(game_state.legacy_screen, (0,0,255),pos[st],pos[el],8)
        for name,coords in pos.items():
            pg.draw.circle(game_state.legacy_screen, (0, 0, 255), coords, circle_radious)
            pg.draw.circle(game_state.legacy_screen, (255, 255, 255), coords, circle_radious-2)
        # Makes a temp surface with the dimensions of a smaller section of the legacy screen (for zooming).
        new_screen = pg.Surface((world_right, world_bottom))
        # Blits the smaller section of the legacy screen to the temp screen
        new_screen.blit(game_state.legacy_screen, (0, 0), (world_left, world_top, world_right, world_bottom))
        # Blits the final cut-out to the main screen, and scales the image to fit with the screen height and width
        screen.fill((255, 255, 255))
        screen.blit(pg.transform.scale(new_screen, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    

    # looping
    pg.display.update()
    clock.tick(30)