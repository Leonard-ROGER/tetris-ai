import os

#Get the terminal dimensions
terminal_length, terminal_height = os.get_terminal_size()

#Create the blanck img
image = [[' ' for _ in range(terminal_length)] for _ in range(terminal_height)]

#Adjust the terminal because the first line is otherwise not visible
terminal_height -=1


def placerPixel(x, y, char):
    '''
    Place a specific type of character on the image at a position (x,y)
    '''
    x1 = int(x)
    y1 = int(y)
    
    if 0 <= x1 <= terminal_length - 1 and 0 <= y1 <= terminal_height - 1:
        image[y1][x1] = char



def afficher():
    '''
    Print the image on the terminal
    '''
    strImage = ''
    for y in range(terminal_height):
        for x in range(terminal_length):
            strImage += image[y][x]
    print(strImage, end='') #The " end='' " avoids a line break


def supprimer():
    '''
    Clear the terminal
    '''
    for y in range(terminal_height):
        for x in range(terminal_length):
            image[y][x] = ' '