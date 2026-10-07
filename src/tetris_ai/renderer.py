import os

#Get the terminal dimensions
terminal_length, terminal_height = os.get_terminal_size()

#Create the blanck img
image = [[' ' for _ in range(terminal_length)] for _ in range(terminal_height)]

#Adjust the terminal because the first line is otherwise not visible
terminal_height -=1


def place_pixel(x, y, char):
    """
    Place a character on the image at position (x, y).
    Positions outside the terminal are ignored.

    Args:
        x: Column (converted to int).
        y: Row (converted to int).
        char: The character to draw.
    """
    x1 = int(x)
    y1 = int(y)
    
    if 0 <= x1 <= terminal_length - 1 and 0 <= y1 <= terminal_height - 1:
        image[y1][x1] = char



def display():
    """
    Print the whole image in the terminal, without a final line break.
    """
    image_str = ''
    for y in range(terminal_height):
        for x in range(terminal_length):
            image_str += image[y][x]
    print(image_str, end='') #The " end='' " avoids a line break


def clear():
    """
    Reset every pixel of the image to a space.
    """
    for y in range(terminal_height):
        for x in range(terminal_length):
            image[y][x] = ' '