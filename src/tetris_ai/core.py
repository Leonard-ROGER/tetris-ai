import random


#Initialisation of all the textures and tetrominos shapes
#Moreover tetrominos will be named blocks after in the code

texture = " %x"
length,height=12,21
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

def create_grid(length,height):
    '''
    Create a size asked grid.
    '''
    grid = [[0 for _ in range(length)] for _ in range(height)]
    for i in range(height):
        for j in range(length):
            grid[i][0] = texture[1]
            grid[i][length-1]=texture[1]
            grid[height-1][j]=texture[1]
    return grid

def block_apparition():
    '''
    return all the varibles needed to a new block apparition
    '''
    new_block = random.choice(tetrominos)
    coord_of_apparition = (0,(length - len(new_block[0]))//2)
    return new_block,coord_of_apparition

def collision(grid,block,coord_block):
    """
    Check if there are collisions between the moving block, the grid and all the former block placed in the grid.
    """
    y,x=coord_block
    for i in range(len(block)):
        for j in range(len(block[0])):
            if block[i][j] != 0 and grid[y+i][x+j] != 0: #and x+j<len(grid[0])
                return True
    return False

def collision_for_bot(grid,block,coord_block):
    """
    Check if there are collisions between the moving block, the grid and all the former block placed in the grid.
    """
    y,x=coord_block
    for i in range(len(block)):
        for j in range(len(block[0])):
            if block[i][j] != 0 and x+j<len(grid[0]) and grid[y+i][x+j] != 0: 
                return True
    return False

def rotation(grid,block,coord_block):
    '''
    Rotate the moving block if there is no collision
    '''
    size=len(block)
    rotated = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            rotated[i][j] = block[size-j-1][i] #deduced from the expression for a rotation in the plane

    if collision(grid,rotated,coord_block):
        return block
    else:
        return rotated

def put_moving_block_in_grid(grid,block,coord_block):
    '''
    Place the moving block in the grid
    '''
    y,x=coord_block
    size=len(block)
    for i in range(size):
        for j in range(size):
            if block[i][j] == 1:
                grid[i+y][j+x] = texture[2]

def detect_and_delete_lines(grid):
    """
    Detect and delete complete lines from the grid. Count how many lines that have been deleted.
    """
    n=0
    end_check=True
    while end_check:
        end_check=False
        for i in range(height-1):
            bool=True
            for j in range(length):
                if grid[i][j] == 0:
                    bool = False
            if bool:
                end_check=True
                n+=1
                del grid[i]
                grid.insert(0,[texture[1]]+[0]*(length-2)+[texture[1]])
    return n

def add_score(score,nb_lines_deleted,speed):
    '''Modify the score of a player'''
    if nb_lines_deleted == 1:
        return score+100*(1/speed*2)
    elif nb_lines_deleted == 2:
        return score+300*(1/speed*2)
    elif nb_lines_deleted ==3:
        return score+500*(1/speed*2)
    elif nb_lines_deleted ==4:
        return score+800*(1/speed*2)
    else: return score