from . import renderer
import time
import keyboard
import random
from . import bot as b
from . import core as fs

#Initialisation of all the textures and tetrominos shapes
#Moreover tetrominos will be named blocks after in the code

texture = " %x"

tetrominos = [[[0,0,0,0],
               [1,1,1,1],
               [0,0,0,0],
               [0,0,0,0]], #the I
              [[1,1,1], 
               [0,0,1],
               [0,0,0]], #the J
              [[1,1,1],
               [1,0,0],
               [0,0,0]], #the L
              [[1, 1],
               [1, 1]], #the O
              [[0, 1, 1],
               [1, 1, 0],
               [0, 0, 0]], #the S
              [[1, 1, 1],
               [0, 1, 0],
               [0, 0, 0]], #the T
              [[1, 1, 0],
               [0, 1, 1],
               [0, 0, 0]]] #the Z

#Auxiliary functions

def draw_in_terminal(length,height,player_grid,player_block,coord_player_block,player_next_blocks,player_score,grid_bot,block_bot,coord_block_bot,bot_next_blocks,bot_score):
    '''
    Draw all the things that need to appear in the terminal
    '''
    
    #logo drawing
    logo_str="TETRIS"
    for i in range(len(logo_str)):    
        renderer.placerPixel(10+i,1,logo_str[i])

     
    #Player score
    player_score_str = 'Score joueur 1 : '
    for i in range(len(player_score_str)):    
        renderer.placerPixel(12+i,3,player_score_str[i])
    str_player_score = str(player_score)
    for i in range(len(str_player_score)):    
        renderer.placerPixel(29+i,3,str_player_score[i])
    
    x_serif_player = 15
    y_serif_player = 5
    
    #player grid 
    for i in range(height):
        l=0
        for j in range(length):
            l+=1 #le l permet d'avoir une longueur de jeu plus large
            x=player_grid[i][j]
            if x != 0:
                renderer.placerPixel(j+l+x_serif_player,i+y_serif_player,x)
    
    #player moving block
    y_player_block,x_player_block=coord_player_block
    for i in range(len(player_block)):
        l=x_player_block
        for j in range(len(player_block[i])):
            l+=1
            if player_block[i][j] == 1:
                renderer.placerPixel(l+j+x_player_block+x_serif_player,i+y_player_block+y_serif_player,texture[2])
    
    
    
    #player next blocks display
    m=5
    l=0
    for x in player_next_blocks:
        x_player_next_block,x_coord_player_next_block = x
        m+=7
        for i in range(len(x_player_next_block)):
            for j in range(len(x_player_next_block[i])):
                l+=1
                if x_player_next_block[i][j] == 1:
                    renderer.placerPixel(m+j,i+35,texture[2])

    
        
    x_serif_bot = renderer.terminal_length//2
    y_serif_bot = 5
    
    #bot grid
    for i in range(height):
        l=0
        for j in range(length):
            l+=1 #le l permet d'avoir une longueur de jeu plus large
            x=grid_bot[i][j]
            if x != 0:
                renderer.placerPixel(j+l+x_serif_bot,i+y_serif_bot,x)
                
    #bot moving block
    y_block_bot,x_block_bot=coord_block_bot
    for i in range(len(block_bot)):
        l=x_block_bot
        for j in range(len(block_bot[i])):
            l+=1
            if block_bot[i][j] == 1:
                renderer.placerPixel(l+j+x_block_bot+x_serif_bot,i+y_block_bot+y_serif_bot,texture[2])

    
    #bot score
    bot_score_str = 'Score ordinateur : '
    for i in range(len(bot_score_str)):    
        renderer.placerPixel(renderer.terminal_length//2+i,3,bot_score_str[i])
    
    str_bot_score = str(bot_score)
    for i in range(len(str_bot_score)):    
        renderer.placerPixel(renderer.terminal_length//2+19+i,3,str_bot_score[i])
    
    #Bot next blocks display
    m=5
    for x in bot_next_blocks:
        x_bot_next_block,x_coord_bot_next_block = x
        m+=7
        for i in range(len(x_bot_next_block)):
            for j in range(len(x_bot_next_block[i])):
                
                if x_bot_next_block[i][j] == 1:
                    renderer.placerPixel(m+j+renderer.terminal_length//2,i+35,texture[2])


def main():
    """Run the game: set up both grids, then loop until the game ends."""
    #Main variables initialisation

    length,height=12,21

    player_grid = fs.create_grid(length,height)
    player_block,coord_player_block= fs.block_apparition()
    player_next_blocks = [fs.block_apparition() for _ in range(10)]
    player_score = 0

    bot_grid = fs.create_grid(length,height)
    bot_block,coord_bot_block= fs.block_apparition()
    bot_next_blocks = [fs.block_apparition() for _ in range(10)]
    bot_score = 0

    bot_following_block,bot_following_block_coord=bot_next_blocks[0]
    wanted_bot_block,wanted_bot_block_coord = b.give_wanted_block_and_coord(player_grid,bot_grid,bot_block,bot_following_block)



    temps_initial = time.time() #give hour
    time_from_previous_speed_increase = time.time()
    speed = 0.5
    speed_buffer = 0.5


    result_bot_grid = []
    result_player_grid = []
    resultat_gap_rate= []

    bot_rate = b.grid_rate(bot_grid)
    player_rate = b.grid_rate(player_grid)

    result_bot_grid.append(bot_rate)
    result_player_grid.append(player_rate)
    resultat_gap_rate.append(player_rate - bot_rate)


    #Main loop

    hold = False #To know if a key is hold
    bot_hold= False

    while True:
        renderer.supprimer()
    
        '''
        Manages speed augmentation
        '''
        if time.time()-time_from_previous_speed_increase>=15.0:
            speed=speed*0.93
            speed_buffer = speed
            time_from_previous_speed_increase = time.time()
    
        '''
        Manages player movements 
        '''
        yb,xb=coord_bot_block
        yp,xp=coord_player_block
        if keyboard.is_pressed("up"):
            if not hold:
                player_block = fs.rotation(player_grid,player_block,coord_player_block)
            hold = True

        elif keyboard.is_pressed("left"):
        
            if not hold and not fs.collision(player_grid,player_block,(yp,xp-1)):
                coord_player_block = yp,xp-1
            hold = True

        elif keyboard.is_pressed("right"):
        
            if not hold and not fs.collision(player_grid,player_block,(yp,xp+1)):
                coord_player_block = yp,xp+1
            hold = True

        else:
            hold = False

        if keyboard.is_pressed("down"):
            speed = speed_buffer*0.1
        else:
            speed = speed_buffer
    
        '''
        Manages bot movement
        '''
        wanted_yb,wanted_xb=wanted_bot_block_coord
        if bot_block != wanted_bot_block:
            if not bot_hold:
                bot_block = fs.rotation(bot_grid,bot_block,coord_bot_block)
            #bot_hold = True

        elif xb>wanted_xb:
            if not bot_hold and not fs.collision(bot_grid,bot_block,(yb,xb-1)):
                coord_bot_block = yb,xb-1
            #bot_hold = True

        elif xb<wanted_xb:
        
            if not bot_hold and not fs.collision(bot_grid,bot_block,(yb,xb+1)):
                coord_bot_block = yb,xb+1
            #bot_hold = True

        else:
            bot_hold = False
    
        '''
        Manages moving blocks' descent and scores 
        '''
        if time.time()-temps_initial>=speed:
            # Executed all the "speed" secondes
        
        
            #if there is a collision in player's grid
        
            if fs.collision(player_grid,player_block,(yp+1,xp)):
            
                #if player can't play
                if yp == 0:
                    if player_score < bot_score: 
                        print("perdu !")
                        break
                    if fs.collision(bot_grid,bot_block,(yp+1,xp)):
                        if yp == 0:
                            if player_score == bot_score:
                                print("tie !")
                                break
                            if player_score < bot_score:
                                print("défaite !")
                    else:
                        coord_bot_block=yb+1,xb
                        temps_initial = time.time()
            
            
                #else (if the player can play but there is a collision in his grid)
                else:
                    fs.put_moving_block_in_grid(player_grid,player_block,coord_player_block)
                    nb_deleted_lines = fs.detect_and_delete_lines(player_grid)
                    player_score = fs.add_score(player_score,nb_deleted_lines,speed) 
                
                    player_block,coord_player_block= player_next_blocks.pop(0)
                
                    player_next_blocks.append(fs.block_apparition())
                
                    player_score = fs.add_score(player_score,nb_deleted_lines,speed)
                
                    bot_rate = b.grid_rate(bot_grid)
                    player_rate = b.grid_rate(player_grid)

                    result_bot_grid.append(bot_rate)
                    result_player_grid.append(player_rate)
                    resultat_gap_rate.append(player_rate - bot_rate)
                
                
                
            #if there is a collision in bot's grid
            elif fs.collision(bot_grid,bot_block,(yb+1,xb)):
            
                #if bot can't play
                if yb == 0:
                    if player_score > bot_score:
                        print("victoire !")
                        break
                    if fs.collision(player_grid,player_block,(yp+1,xp)):
                        if yp == 0:
                            if player_score == bot_score:
                                print("tie !")
                                break
                            if player_score < bot_score:
                                print("défaite !")
                    else:
                        coord_player_block=yp+1,xp
                        temps_initial = time.time()
            
                #else (if the bot can play but there is a collision in it grid)
                else:
                    fs.put_moving_block_in_grid(bot_grid,bot_block,coord_bot_block)
                    nb_deleted_lines_bot = fs.detect_and_delete_lines(bot_grid)
                    bot_score = fs.add_score(bot_score,nb_deleted_lines_bot,speed) 
                
                    bot_block,coord_bot_block= bot_next_blocks.pop(0)
                
                    bot_next_blocks.append(fs.block_apparition())
                
                    bot_score = fs.add_score(bot_score,nb_deleted_lines_bot,speed)
                
                    bot_following_block,bot_following_block_coord=bot_next_blocks[0]
                
                    wanted_bot_block,wanted_bot_block_coord = b.give_wanted_block_and_coord(player_grid,bot_grid,bot_block,bot_following_block)
                
                    bot_rate = b.grid_rate(bot_grid)
                    player_rate = b.grid_rate(player_grid)

                    result_bot_grid.append(bot_rate)
                    result_player_grid.append(player_rate)
                    resultat_gap_rate.append(player_rate - bot_rate)
                

        
            #Else (if both can play without collision)
            else:
                coord_player_block=yp+1,xp
                coord_bot_block=yb+1,xb
                temps_initial = time.time()
           
        draw_in_terminal(length,height,player_grid,player_block,coord_player_block,player_next_blocks,player_score,bot_grid,bot_block,coord_bot_block,bot_next_blocks,bot_score)
        renderer.afficher()

    print("bot result", result_bot_grid)
    print("player result", result_player_grid)
    print("gap_result", resultat_gap_rate)
    input()
    exit()
