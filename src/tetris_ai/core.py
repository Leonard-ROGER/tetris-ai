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
    """
    Create an empty grid surrounded by walls (left, right and bottom).

    Args:
        length: Number of columns, walls included.
        height: Number of rows, floor included.

    Returns:
        A list of `height` rows of `length` cells: 0 for an empty cell,
        texture[1] for a wall.
    """
    grid = [[0 for _ in range(length)] for _ in range(height)]
    for i in range(height):
        for j in range(length):
            grid[i][0] = texture[1]
            grid[i][length-1]=texture[1]
            grid[height-1][j]=texture[1]
    return grid

def block_apparition():
    """
    Pick a random tetromino and its spawn position.

    Returns:
        A tuple (block, (y, x)): the tetromino matrix and the coordinates of
        its top-left corner, on the first row and horizontally centered.
    """
    new_block = random.choice(tetrominos)
    coord_of_apparition = (0,(length - len(new_block[0]))//2)
    return new_block,coord_of_apparition

def collision(grid,block,coord_block):
    """
    Check if the block overlaps a wall or a block already placed in the grid.

    Args:
        grid: The game grid.
        block: The tetromino matrix.
        coord_block: (y, x) coordinates of the block's top-left corner.

    Returns:
        True if at least one filled cell of the block is on a non-empty cell
        of the grid, False otherwise.
    """
    y,x=coord_block
    for i in range(len(block)):
        for j in range(len(block[0])):
            if block[i][j] != 0 and grid[y+i][x+j] != 0: #and x+j<len(grid[0])
                return True
    return False

def collision_for_bot(grid,block,coord_block):
    """
    Same as collision, but cells beyond the right edge of the grid are ignored
    instead of being read (used by the bot to test every column).

    Args:
        grid: The game grid.
        block: The tetromino matrix.
        coord_block: (y, x) coordinates of the block's top-left corner.

    Returns:
        True if a filled cell of the block is on a non-empty cell inside the
        grid, False otherwise.
    """
    y,x=coord_block
    for i in range(len(block)):
        for j in range(len(block[0])):
            if block[i][j] != 0 and x+j<len(grid[0]) and grid[y+i][x+j] != 0: 
                return True
    return False

def rotation(grid,block,coord_block):
    """
    Rotate the block by 90 degrees if the result does not collide.

    Args:
        grid: The game grid.
        block: The tetromino matrix to rotate.
        coord_block: (y, x) coordinates of the block's top-left corner.

    Returns:
        The rotated matrix, or the original block if the rotation collides.
    """
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
    """
    Write the block into the grid, modifying the grid in place.

    Args:
        grid: The game grid (modified in place).
        block: The tetromino matrix.
        coord_block: (y, x) coordinates of the block's top-left corner.
    """
    y,x=coord_block
    size=len(block)
    for i in range(size):
        for j in range(size):
            if block[i][j] == 1:
                grid[i+y][j+x] = texture[2]

def detect_and_delete_lines(grid):
    """
    Delete every complete line and insert an empty line at the top for each.

    Args:
        grid: The game grid (modified in place).

    Returns:
        The number of lines deleted.
    """
    deleted_lines_count=0
    line_found=True
    while line_found:
        line_found=False
        for i in range(height-1):
            is_full_line=True
            for j in range(length):
                if grid[i][j] == 0:
                    is_full_line = False
            if is_full_line:
                line_found=True
                deleted_lines_count+=1
                del grid[i]
                grid.insert(0,[texture[1]]+[0]*(length-2)+[texture[1]])
    return deleted_lines_count

def add_score(score,nb_lines_deleted,speed):
    """
    Compute a player's new score after a block is placed.

    Args:
        score: The current score.
        nb_lines_deleted: Number of lines cleared by the block (0 to 4).
        speed: Current delay between two descents, in seconds. The faster
            the game, the more points a line is worth.

    Returns:
        The updated score (unchanged if no line was cleared).
    """
    if nb_lines_deleted == 1:
        return score+100*(1/speed*2)
    elif nb_lines_deleted == 2:
        return score+300*(1/speed*2)
    elif nb_lines_deleted ==3:
        return score+500*(1/speed*2)
    elif nb_lines_deleted ==4:
        return score+800*(1/speed*2)
    else: return score