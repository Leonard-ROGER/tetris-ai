from . import renderer
import time
import keyboard
from . import bot
from . import core

#Auxiliary functions

def draw_in_terminal(length,height,player_grid,player_block,coord_player_block,player_next_blocks,player_score,grid_bot,block_bot,coord_block_bot,bot_next_blocks,bot_score):
    """
    Draw both games (player on the left, bot on the right) in the renderer's image.

    Args:
        length: Number of columns of a grid.
        height: Number of rows of a grid.
        player_grid: The player's grid.
        player_block: The player's moving block matrix.
        coord_player_block: (y, x) coordinates of the player's moving block.
        player_next_blocks: List of (block, coord) upcoming for the player.
        player_score: The player's score.
        grid_bot: The bot's grid.
        block_bot: The bot's moving block matrix.
        coord_block_bot: (y, x) coordinates of the bot's moving block.
        bot_next_blocks: List of (block, coord) upcoming for the bot.
        bot_score: The bot's score.
    """
    
    #logo drawing
    logo_str="TETRIS"
    for i in range(len(logo_str)):    
        renderer.place_pixel(10+i,1,logo_str[i])

     
    #Player score
    player_score_str = 'Score joueur 1 : '
    for i in range(len(player_score_str)):    
        renderer.place_pixel(12+i,3,player_score_str[i])
    str_player_score = str(player_score)
    for i in range(len(str_player_score)):    
        renderer.place_pixel(29+i,3,str_player_score[i])
    
    x_offset_player = 15
    y_offset_player = 5
    
    #player grid 
    for i in range(height):
        col_offset=0
        for j in range(length):
            col_offset+=1 #col_offset doubles the horizontal spacing: each cell takes 2 terminal columns
            cell=player_grid[i][j]
            if cell != 0:
                renderer.place_pixel(j+col_offset+x_offset_player,i+y_offset_player,cell)
    
    #player moving block
    y_player_block,x_player_block=coord_player_block
    for i in range(len(player_block)):
        col_offset=x_player_block
        for j in range(len(player_block[i])):
            col_offset+=1
            if player_block[i][j] == 1:
                renderer.place_pixel(col_offset+j+x_player_block+x_offset_player,i+y_player_block+y_offset_player,core.texture[2])
    
    
    
    #player next blocks display
    next_x=5
    col_offset=0
    for next_entry in player_next_blocks:
        x_player_next_block,x_coord_player_next_block = next_entry
        next_x+=7
        for i in range(len(x_player_next_block)):
            for j in range(len(x_player_next_block[i])):
                col_offset+=1
                if x_player_next_block[i][j] == 1:
                    renderer.place_pixel(next_x+j,i+35,core.texture[2])

    
        
    x_offset_bot = renderer.terminal_length//2
    y_offset_bot = 5
    
    #bot grid
    for i in range(height):
        col_offset=0
        for j in range(length):
            col_offset+=1 #col_offset doubles the horizontal spacing: each cell takes 2 terminal columns
            cell=grid_bot[i][j]
            if cell != 0:
                renderer.place_pixel(j+col_offset+x_offset_bot,i+y_offset_bot,cell)
                
    #bot moving block
    y_block_bot,x_block_bot=coord_block_bot
    for i in range(len(block_bot)):
        col_offset=x_block_bot
        for j in range(len(block_bot[i])):
            col_offset+=1
            if block_bot[i][j] == 1:
                renderer.place_pixel(col_offset+j+x_block_bot+x_offset_bot,i+y_block_bot+y_offset_bot,core.texture[2])

    
    #bot score
    bot_score_str = 'Score ordinateur : '
    for i in range(len(bot_score_str)):    
        renderer.place_pixel(renderer.terminal_length//2+i,3,bot_score_str[i])
    
    str_bot_score = str(bot_score)
    for i in range(len(str_bot_score)):    
        renderer.place_pixel(renderer.terminal_length//2+19+i,3,str_bot_score[i])
    
    #Bot next blocks display
    next_x=5
    for next_entry in bot_next_blocks:
        x_bot_next_block,x_coord_bot_next_block = next_entry
        next_x+=7
        for i in range(len(x_bot_next_block)):
            for j in range(len(x_bot_next_block[i])):
                
                if x_bot_next_block[i][j] == 1:
                    renderer.place_pixel(next_x+j+renderer.terminal_length//2,i+35,core.texture[2])


def main():
    """Run the game: set up both grids, then loop until the game ends."""
    #Main variables initialisation

    length,height=core.length,core.height

    player_grid = core.create_grid(length,height)
    player_block,coord_player_block= core.block_apparition()
    player_next_blocks = [core.block_apparition() for _ in range(10)]
    player_score = 0

    bot_grid = core.create_grid(length,height)
    bot_block,coord_bot_block= core.block_apparition()
    bot_next_blocks = [core.block_apparition() for _ in range(10)]
    bot_score = 0

    bot_following_block,bot_following_block_coord=bot_next_blocks[0]
    wanted_bot_block,wanted_bot_block_coord = bot.give_wanted_block_and_coord(player_grid,bot_grid,bot_block,bot_following_block)



    initial_time = time.time() #give hour
    time_from_previous_speed_increase = time.time()
    speed = 0.5
    speed_buffer = 0.5


    result_bot_grid = []
    result_player_grid = []
    gap_rate_result= []

    bot_rate = bot.grid_rate(bot_grid)
    player_rate = bot.grid_rate(player_grid)

    result_bot_grid.append(bot_rate)
    result_player_grid.append(player_rate)
    gap_rate_result.append(player_rate - bot_rate)


    #Main loop

    hold = False #To know if a key is hold
    bot_hold= False

    while True:
        renderer.clear()
    
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
        bot_y,bot_x=coord_bot_block
        player_y,player_x=coord_player_block
        if keyboard.is_pressed("up"):
            if not hold:
                player_block = core.rotation(player_grid,player_block,coord_player_block)
            hold = True

        elif keyboard.is_pressed("left"):
        
            if not hold and not core.collision(player_grid,player_block,(player_y,player_x-1)):
                coord_player_block = player_y,player_x-1
            hold = True

        elif keyboard.is_pressed("right"):
        
            if not hold and not core.collision(player_grid,player_block,(player_y,player_x+1)):
                coord_player_block = player_y,player_x+1
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
                bot_block = core.rotation(bot_grid,bot_block,coord_bot_block)
            #bot_hold = True

        elif bot_x>wanted_xb:
            if not bot_hold and not core.collision(bot_grid,bot_block,(bot_y,bot_x-1)):
                coord_bot_block = bot_y,bot_x-1
            #bot_hold = True

        elif bot_x<wanted_xb:
        
            if not bot_hold and not core.collision(bot_grid,bot_block,(bot_y,bot_x+1)):
                coord_bot_block = bot_y,bot_x+1
            #bot_hold = True

        else:
            bot_hold = False
    
        '''
        Manages moving blocks' descent and scores 
        '''
        if time.time()-initial_time>=speed:
            # Executed all the "speed" secondes
        
        
            #if there is a collision in player's grid
        
            if core.collision(player_grid,player_block,(player_y+1,player_x)):
            
                #if player can't play
                if player_y == 0:
                    if player_score < bot_score: 
                        print("perdu !")
                        break
                    if core.collision(bot_grid,bot_block,(player_y+1,player_x)):
                        if player_y == 0:
                            if player_score == bot_score:
                                print("tie !")
                                break
                            if player_score < bot_score:
                                print("défaite !")
                    else:
                        coord_bot_block=bot_y+1,bot_x
                        initial_time = time.time()
            
            
                #else (if the player can play but there is a collision in his grid)
                else:
                    core.put_moving_block_in_grid(player_grid,player_block,coord_player_block)
                    nb_deleted_lines = core.detect_and_delete_lines(player_grid)
                    player_score = core.add_score(player_score,nb_deleted_lines,speed) 
                
                    player_block,coord_player_block= player_next_blocks.pop(0)
                
                    player_next_blocks.append(core.block_apparition())

                    bot_rate = bot.grid_rate(bot_grid)
                    player_rate = bot.grid_rate(player_grid)

                    result_bot_grid.append(bot_rate)
                    result_player_grid.append(player_rate)
                    gap_rate_result.append(player_rate - bot_rate)
                
                
                
            #if there is a collision in bot's grid
            elif core.collision(bot_grid,bot_block,(bot_y+1,bot_x)):
            
                #if bot can't play
                if bot_y == 0:
                    if player_score > bot_score:
                        print("victoire !")
                        break
                    if core.collision(player_grid,player_block,(player_y+1,player_x)):
                        if player_y == 0:
                            if player_score == bot_score:
                                print("tie !")
                                break
                            if player_score < bot_score:
                                print("défaite !")
                    else:
                        coord_player_block=player_y+1,player_x
                        initial_time = time.time()
            
                #else (if the bot can play but there is a collision in it grid)
                else:
                    core.put_moving_block_in_grid(bot_grid,bot_block,coord_bot_block)
                    nb_deleted_lines_bot = core.detect_and_delete_lines(bot_grid)
                    bot_score = core.add_score(bot_score,nb_deleted_lines_bot,speed) 
                
                    bot_block,coord_bot_block= bot_next_blocks.pop(0)
                
                    bot_next_blocks.append(core.block_apparition())

                    bot_following_block,bot_following_block_coord=bot_next_blocks[0]
                
                    wanted_bot_block,wanted_bot_block_coord = bot.give_wanted_block_and_coord(player_grid,bot_grid,bot_block,bot_following_block)
                
                    bot_rate = bot.grid_rate(bot_grid)
                    player_rate = bot.grid_rate(player_grid)

                    result_bot_grid.append(bot_rate)
                    result_player_grid.append(player_rate)
                    gap_rate_result.append(player_rate - bot_rate)
                

        
            #Else (if both can play without collision)
            else:
                coord_player_block=player_y+1,player_x
                coord_bot_block=bot_y+1,bot_x
                initial_time = time.time()
           
        draw_in_terminal(length,height,player_grid,player_block,coord_player_block,player_next_blocks,player_score,bot_grid,bot_block,coord_bot_block,bot_next_blocks,bot_score)
        renderer.display()

    print("bot result", result_bot_grid)
    print("player result", result_player_grid)
    print("gap_result", gap_rate_result)
    input()
    exit()


if __name__ == "__main__":
    main()
