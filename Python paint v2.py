# Better console-based paint program
from copy import deepcopy
import simpleParsers
import keyboard
import os
import time

def down():  # Down command
    cursorPosition[1] += 1
    if cursorPosition[1] >= rowsPerPicture:
        cursorPosition[1] = rowsPerPicture - 1
    printPicture(rows, cursorPosition)
def up():  # Up command
    cursorPosition[1] -= 1
    if cursorPosition[1] < 0:
        cursorPosition[1] = 0
    printPicture(rows, cursorPosition)
def right():  # Right command
    cursorPosition[0] += 1
    if cursorPosition[0] >= itemsPerRow:
        cursorPosition[0] = itemsPerRow - 1
    printPicture(rows, cursorPosition)
def left():  # Left command
    cursorPosition[0] -= 1
    if cursorPosition[0] < 0:
        cursorPosition[0] = 0
    printPicture(rows, cursorPosition)
def assignBrush(i):  # Changes brush to brush choice
    global brushChoice, boxes
    try:
        brushChoice = boxes[i]
    except IndexError:
        return()
    printPicture(rows, cursorPosition)
def paint():  # Paint current box command
    rows[cursorPosition[1]][cursorPosition[0]] = brushChoice
    printPicture(rows, cursorPosition)

cursorChoice = 0  # Choice of cursor, global
def toggleCursor():  # Increment cursor choice on keypress
    global cursorChoice
    if cursorChoice < (len(cursorType) - 1):
        cursorChoice += 1
    else:
        cursorChoice = 0
    printPicture(rows, cursorPosition)
def refreshCursor():  # Refresh cursor math
    global cursorChoice, cursorType
    charUnderCursor = rows[cursorPosition[1]][cursorPosition[0]]
    indexInBoxes = boxes.index(charUnderCursor)
    cursorType = [
        '\u254b',  # Fixed cursor
        shadeSqrBoxes[charUnderCursor],  # Shaded box cursor
        boxes[indexInBoxes + 1] if charUnderCursor != boxes[-1] else boxes[indexInBoxes - 1],  # One shade lighter
        boxes[indexInBoxes - 1] if charUnderCursor != boxes[0] else boxes[indexInBoxes + 1],  # One shade darker
        None  # No cursor
    ]

def printPicture(picture, cursor=(-1,-1)):
    refreshCursor()
    cursorChar = cursorType[cursorChoice]


    rowIndexStrLen = len(f'{len(picture)}')
    columnStrLength = len(f'{len(picture[-1])}')
    os.system('cls' if os.name == 'nt' else 'clear')  # Uses correct clear console command
    print(f'\n[ BRUSH: ] [{brushChoice}]\t[ CURSOR: ] [{cursorChar}] ( {cursorPosition[0]}, {cursorPosition[1]} )')
    print(''.ljust(rowIndexStrLen + 1), end='')
    for i in range(rowIndexStrLen + 1, len(picture[0]) + 1 + rowIndexStrLen):  # Print top cursor pointer
        print('\u25bd\u25bd' if i - (rowIndexStrLen + 1) == cursor[0] else '  ', end='')
    print()
    # Top border:
    for i in range(0, len(picture[0]) + 2):
        if i == 0: print(f"""{''.rjust(rowIndexStrLen)}\u2554""", end='')  # Left corner
        elif i == len(picture[0]) + 1: print('\u2557')  # Right corner
        else: print('\u2550\u2550', end='')  # Middle section

    for rowIndex, row in enumerate(picture):  # Print picture itself
        rowIndexStr = f'{rowIndex}'.rjust(rowIndexStrLen)
        for itemIndex, item in enumerate(row):
            if itemIndex == 0: print(f'{rowIndexStr}\u2551', end='')  # Left border

            if itemIndex == cursor[0] and rowIndex == cursor[1] and cursorChar != None:  # If this item is cursor location
                print(cursorChar + cursorChar, end='')
            else:
                print(item + item, end='')

            if itemIndex == len(row) - 1: print('\u2551', '\u25c1' if rowIndex == cursor[1] else '', sep='', end='')  # Right border
        print()
    # Bottom border:
    for i in range(0, len(picture[-1]) + 2):
        if i == 0:  print(f"""{''.rjust(rowIndexStrLen)}\u255a""", end='')  # Left corner
        elif i == len(picture[-1]) + 1: print('\u255d')  # Right corner
        else:   print('\u2550\u2550', end='')  # Middle section
    # Bottom index number
    for i in range(0, columnStrLength):  # For each digit of the number of columns
        print(f"""{''.rjust(rowIndexStrLen + 1)}""", end='')
        for columnNum in range(0, 2*len(picture[-1])):  # For each column
            print(str(columnNum//2).ljust(columnStrLength)[i] if columnNum % (intervalXLabel * 2) == 0 else ' ', end='')  # print index
        print()
    print()
    # Print box options, then controls
    for index, item in enumerate(boxes):
        print(f'[{index + 1}] {item}\t', end='')
    print('\n[SPACE: PAINT] [WASD:MOVE] [H:TOGGLE CURSOR]\t\t', end='')


intervalXLabel = 2  # Customization


#  BEGIN PROGRAM
print('\n == Python Paint v1 ==')
boxes = [
    '\u2588',  # full
    '\u2593',  # dark
    '\u2592',  # medium
    '\u2591',  # light
    ' '        # none
]  # Box characters for drawing
shadeSqrBoxes = {
    boxes[0]: '\u25a0',  # full
    boxes[1]: '\u25a9',  # dark
    boxes[2]: '\u25a6',  # medium
    boxes[3]: '\u25a4',  # light
    boxes[4]: '\u25a1'   # none
}  # Shaded square characters for cursor

bufferRow, rows = [], []  # Matrix: A list of lists of row positions
# region Picture size prompt
print('Input picture size:')
while True:  # Prompt user picture width
    itemsPerRow = simpleParsers.parseInt(input('[ WIDTH ] > '), 200, 2) + 1
    if itemsPerRow != 'invalid': break
while True:
    rowsPerPicture = simpleParsers.parseInt(input('[ HEIGHT ] > '), 1000, 2) + 1
    if rowsPerPicture != 'invalid': break
# endregion

# region Fill picture with empty characters
for x in range(0, rowsPerPicture):  # For each row in the picture
    for y in range(0, itemsPerRow):  # For each item in row
        bufferRow.append(' ')
    rows.append(deepcopy(bufferRow))
    bufferRow.clear()
# rows now contains (rowsPerPicture) lists, each containing (itemsPerRow) items that will act as pixels
# endregion

cursorPosition, brushChoice = [itemsPerRow//2, rowsPerPicture//2], boxes[4]  # Defaults
commands = "U, D, L, R, C (CHOOSE), P (PAINT)"
printPicture(rows, cursorPosition)

# region Hotkey initialization
hotkeys = (  # Hotkeys for control buttons
    ('s', down),
    ('w', up),
    ('a', left),
    ('d', right),
    ('space', paint),
    ('h', toggleCursor)
)
for hotkey in hotkeys:  # Creates hotkeys from list hotkeys tuple above
    keyboard.add_hotkey(hotkey[0], hotkey[1])

for x in range(0, 9):  # Creates the number hotkeys
    keyboard.add_hotkey(f'{x+1}', lambda y=x : assignBrush(y))
# endregion

while True:  # Enter infinite loop, painting begins
    time.sleep(0.001)
    continue