from . import core
import copy
from random import randint 

free_grid=core.create_grid(core.length,core.height)

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

def get_variety(block):
    """
    Find all the rotations of a tetromino.

    Args:
        block: A tetromino matrix, in any of its rotations.

    Returns:
        The list of distinct rotations it belongs to (None if unknown).
    """
    for i in range(len(all_variety)):
        if block in all_variety[i]:
            return all_variety[i]
 

def get_possibles_positions(grid,block):
    """
    List every landing position of a block: each rotation, in each column.

    Args:
        grid: The bot's grid.
        block: The tetromino matrix to place.

    Returns:
        A list of (rotation, (y, x)): the rotated matrix and the coordinates
        where it lands after being dropped.
    """
    possible_positions=[]
    for rotation in get_variety(block):
        for j in range(0,core.length-1):
            if not core.collision_for_bot(free_grid,rotation,(0,j)):
                i=0
                while i<(core.height-1) and (not core.collision_for_bot(grid,rotation,(i+1,j))):
                    i+=1
                possible_positions.append((rotation,(i,j)))
    return possible_positions

def list_all_grids_possible(grid,block):
    """
    Simulate every possible placement of a block.

    Args:
        grid: The bot's grid (not modified).
        block: The tetromino matrix to place.

    Returns:
        A list of grids, one per position given by get_possibles_positions,
        with the block placed and complete lines deleted.
    """
    possible_positions=get_possibles_positions(grid,block)
    possible_grids=[]
    for i in range(len(possible_positions)):
        temp_grid=copy.deepcopy(grid)
        temp_block,temp_coord_block=possible_positions[i]
        core.put_moving_block_in_grid(temp_grid,temp_block,temp_coord_block)
        core.detect_and_delete_lines(temp_grid)
        possible_grids.append(temp_grid)
    return possible_grids

def tower_height(grid):
    """
    Compute the height of the highest column.

    Args:
        grid: The game grid.

    Returns:
        The number of rows between the floor and the highest filled cell.
    """
    for i in range(0,core.height-1):
        for j in range(1,core.length-1):
            if grid[i][j] != 0:
                return core.height - (i+1)
    return 0


def count_holes(grid):
    """
    Count the empty cells that have a filled cell somewhere above them.

    Args:
        grid: The game grid.

    Returns:
        The number of holes.
    """
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
    """
    Measure how uneven the surface is.

    Args:
        grid: The game grid.

    Returns:
        The difference between the highest and the lowest column.
    """
    column_tops= []
    for j in range(1,len(grid[0])-1):
        check = True
        for i in range(len(grid)-1):
            if grid[i][j] != 0 and check:
                check = False
                column_tops.append(i)
        if check:
            column_tops.append(core.height-2)
    return max(column_tops) - min(column_tops)
            

def grid_rate(grid):
    """
    Rate a grid: the lower, the better.

    Args:
        grid: The game grid.

    Returns:
        The sum of the tower height, the number of holes and the height gap.
    """
    return tower_height(grid)+count_holes(grid)+height_gap(grid)

def create_graph(grid,block1,block2):
    """
    Build the tree of every placement of block1 followed by every placement of block2.

    Args:
        grid: The bot's grid.
        block1: The current block.
        block2: The next block.

    Returns:
        A tuple (positions, grids). For each placement i of block1,
        positions[i] and grids[i] list the placements of block2 and the
        resulting grids.
    """
    graph_positions= get_possibles_positions(grid,block1)
    graph_grids = list_all_grids_possible(grid,block1)
    for i in range(len(graph_positions)):
        graph_positions[i]=get_possibles_positions(graph_grids[i],block2)
        graph_grids[i]=list_all_grids_possible(graph_grids[i],block2)
    return graph_positions,graph_grids

def create_rating_list(grid_list):
    """
    Rate every grid of the tree built by create_graph.

    Args:
        grid_list: List (per placement of block1) of lists of grids.

    Returns:
        A list of lists with the same shape, containing grid_rate of each grid.
    """
    rating=[[] for _ in range(len(grid_list))]
    for i in range(len(grid_list)):
        for j in range(len(grid_list[i])):
            rating[i].append(grid_rate(grid_list[i][j]))
    return rating

def choose_min_path(rating):
    """
    Choose the placement of block1 leading to the best (lowest) rating.

    Args:
        rating: Rating list from create_rating_list.

    Returns:
        The index of the placement of block1.
    """
    min_weight= rating[0][0]
    i_min = 0
    for i in range(len(rating)):
        for j in range(len(rating[i])):
            if min_weight > rating[i][j]:
                min_weight = rating[i][j]
                i_min=i
    return i_min

def choose_max_path(rating):
    """
    Choose the placement of block1 leading to the worst (highest) rating.

    Args:
        rating: Rating list from create_rating_list.

    Returns:
        The index of the placement of block1.
    """
    max_weight= rating[0][0]
    i_max = 0
    for i in range(len(rating)):
        for j in range(len(rating[i])):
            if max_weight < rating[i][j]:
                max_weight = rating[i][j]
                i_max=i
    return i_max

def choose_random_path(rating):
    """
    Choose a placement of block1 at random.

    Args:
        rating: Rating list from create_rating_list (only its length is used).

    Returns:
        The index of the placement of block1.
    """
    return randint(0, len(rating)-1)

def choose_path(player_grid,bot_grid,rating):
    """
    Choose a placement according to the gap between the player's and the bot's grids.
    Gap below 1: best move. Gap from 1 to 8: random move. Gap above 8: worst move.

    Args:
        player_grid: The player's grid.
        bot_grid: The bot's grid.
        rating: Rating list from create_rating_list.

    Returns:
        The index of the chosen placement of block1.
    """
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
    """
    Decide where and how the bot wants to place its current block.

    Args:
        player_grid: The player's grid.
        bot_grid: The bot's grid.
        block1: The bot's current block.
        block2: The bot's next block.

    Returns:
        A tuple (rotation, (y, x)): the wanted matrix and landing coordinates.
    """
    graph_possibilities,graph_grids = create_graph(bot_grid,block1,block2)
    rating_list=create_rating_list(graph_grids)
    i= choose_path(player_grid,bot_grid,rating_list)
    list_moves = get_possibles_positions(bot_grid,block1)
    return list_moves[i]