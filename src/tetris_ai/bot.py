import function_stock as fs
import copy
from random import randint 

free_grid=fs.create_grid(fs.length,fs.height)

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

t_variety=[[[1,1,1], 
            [0,1,0],
            [0,0,0]],
           [[0,0,1], 
            [0,1,1],
            [0,0,1]],
           [[0,0,0], 
            [0,1,0],
            [1,1,1]],
           [[1,0,0], 
            [1,1,0],
            [1,0,0]]]

z_variety=[[[1,1,0], 
            [0,1,1],
            [0,0,0]],
           [[0,0,1], 
            [0,1,1],
            [0,1,0]],
           [[0,0,0], 
            [1,1,0],
            [0,1,1]],
           [[0,1,0], 
            [1,1,0],
            [1,0,0]]]

s_variety=[[[0,1,1], 
            [1,1,0],
            [0,0,0]],
           [[0,1,0], 
            [0,1,1],
            [0,0,1]],
           [[0,0,0], 
            [0,1,1],
            [1,1,0]],
           [[1,0,0], 
            [1,1,0],
            [0,1,0]]]

o_variety=[[[1,1],
           [1,1]]]

l_variety=[[[1,1,1], 
            [1,0,0],
            [0,0,0]],
           [[0,1,1], 
            [0,0,1],
            [0,0,1]],
           [[0,0,0], 
            [0,0,1],
            [1,1,1]],
           [[1,0,0], 
            [1,0,0],
            [1,1,0]]]

j_variety=[[[1,1,1], 
            [0,0,1],
            [0,0,0]],
           [[0,0,1], 
            [0,0,1],
            [0,1,1]],
           [[0,0,0], 
            [1,0,0],
            [1,1,1]],
           [[1,1,0], 
            [1,0,0],
            [1,0,0]]]

i_variety=[[[0,0,0,0],
           [1,1,1,1],
           [0,0,0,0],
           [0,0,0,0]],
           [[0,1,0,0],
            [0,1,0,0],
            [0,1,0,0],
            [0,1,0,0]]]

all_variety = [t_variety,z_variety,s_variety,o_variety,l_variety,j_variety,i_variety]

def get_varity(block):
    for i in range(len(all_variety)):
        if block in all_variety[i]:
            return all_variety[i]
 

def get_possibles_positions(grid,block):
    possible_positions=[]
    for x in get_varity(block):
        for j in range(0,fs.length-1):
            if not fs.collision_for_bot(free_grid,x,(0,j)):
                i=0
                while i<(fs.height-1) and (not fs.collision_for_bot(grid,x,(i+1,j))):
                    i+=1
                possible_positions.append((x,(i,j)))
    return possible_positions

def list_all_grids_possible(grid,block):
    possible_positions=get_possibles_positions(grid,block)
    possible_grids=[]
    for i in range(len(possible_positions)):
        temp_grid=copy.deepcopy(grid)
        temp_block,temp_coord_block=possible_positions[i]
        fs.put_moving_block_in_grid(temp_grid,temp_block,temp_coord_block)
        n = fs.detect_and_delete_lines(temp_grid)
        possible_grids.append(temp_grid)
    return possible_grids

def tower_height(grid):
    max=0
    for i in range(0,fs.height-1):
        for j in range(1,fs.length-1):
            if grid[i][j] != 0:
                return fs.height - (i+1)
    return 0


def count_holes(grid):
    nb_holes = 0
    
    for j in range(1,len(grid[0])-1):
        check = False
        for i in range(len(grid)-1):
            if grid[i][j] != 0:
                check = True
            elif check and grid[i][j] == 0:
                nb_holes += 1
    return nb_holes

def height_gap(grid):
    l= []
    for j in range(1,len(grid[0])-1):
        check = True
        for i in range(len(grid)-1):
            if grid[i][j] != 0 and check:
                check = False
                l.append(i)
        if check:
            l.append(fs.height-2)
    return max(l) - min(l)
            

def grid_rate(grid):
    return tower_height(grid)+count_holes(grid)+height_gap(grid)

def create_graph(grid,block1,block2):
    graph_positions= get_possibles_positions(grid,block1)
    graph_grids = list_all_grids_possible(grid,block1)
    for i in range(len(graph_positions)):
        graph_positions[i]=get_possibles_positions(graph_grids[i],block2)
        graph_grids[i]=list_all_grids_possible(graph_grids[i],block2)
    return graph_positions,graph_grids

def create_rating_list(grid_list):
    rating=[[] for _ in range(len(grid_list))]
    for i in range(len(grid_list)):
        for j in range(len(grid_list[i])):
            rating[i].append(grid_rate(grid_list[i][j]))
    return rating

def choose_min_path(rating):
    min_weight= rating[0][0]
    i_min = 0
    for i in range(len(rating)):
        for j in range(len(rating[i])):
            if min_weight > rating[i][j]:
                min_weight = rating[i][j]
                i_min=i
    return i_min

def choose_max_path(rating):
    max_weight= rating[0][0]
    i_max = 0
    for i in range(len(rating)):
        for j in range(len(rating[i])):
            if max_weight < rating[i][j]:
                max_weight = rating[i][j]
                i_max=i
    return i_max

def choose_random_path(rating):
    return randint(0, len(rating)-1)

def choose_path(player_grid,bot_grid,rating):
    player_rating,bot_rating = grid_rate(player_grid),grid_rate(bot_grid)
    rating_gap =player_rating - bot_rating
    #rating_gap = 0
    if rating_gap < 1 :
        return choose_min_path(rating)
    elif 1<= rating_gap <= 8:
        return choose_random_path(rating)
    else:
        return choose_max_path(rating)

def give_wanted_block_and_coord(player_grid,bot_grid,block1,block2):
    graph_possibilities,graph_grids = create_graph(bot_grid,block1,block2)
    rating_list=create_rating_list(graph_grids)
    i= choose_path(player_grid,bot_grid,rating_list)
    list_moves = get_possibles_positions(bot_grid,block1)
    return list_moves[i]