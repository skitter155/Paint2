# Better console-based paint program
from copy import deepcopy
import simpleParsers
import keyboard
import os
import time

def multiChar(length, char = ' ', first = None, last = None):
    workString = ''
    for x in range(0, length):
        if x == 0 and first != None: workString += first
        elif x == length - 1 and last != None: workString += last
        else: workString += char
    return workString

def down():  # Down command
    cursorPos[1] += 1
    if cursorPos[1] >= rowsPerPicture:
        cursorPos[1] = rowsPerPicture - 1
    pictureUpdatedFlag = True
def up():  # Up command
    cursorPos[1] -= 1
    if cursorPos[1] < 0:
        cursorPos[1] = 0
    pictureUpdatedFlag = True
def right():  # Right command
    cursorPos[0] += 1
    if cursorPos[0] >= itemsPerRow:
        cursorPos[0] = itemsPerRow - 1
    pictureUpdatedFlag = True
def left():  # Left command
    cursorPos[0] -= 1
    if cursorPos[0] < 0:
        cursorPos[0] = 0
    pictureUpdatedFlag = True
def assignBrush(i):  # Changes brush to brush choice
    global brushChoice, boxes
    try:
        brushChoice = boxes[i]
    except IndexError:
        return()
    pictureUpdatedFlag = True
def paint():  # Paint current box command
    picture[cursorPos[1]][cursorPos[0]] = brushChoice
    pictureUpdatedFlag = True

cursorChoice = 0  # Choice of cursor, global
def toggleCursor():  # Increment cursor choice on keypress
    global cursorChoice
    if cursorChoice < (len(cursorType) - 1):
        cursorChoice += 1
    else:
        cursorChoice = 0
    pictureUpdatedFlag = True
def refreshCursor():  # Refresh cursor math
    global cursorChoice, cursorType
    charUnderCursor = picture[cursorPos[1]][cursorPos[0]]
    indexInBoxes = boxes.index(charUnderCursor)
    cursorType = [
        '\u254b',  # Fixed cursor
        shadeSqrBoxes[charUnderCursor],  # Shaded box cursor
        boxes[indexInBoxes + 1] if charUnderCursor != boxes[-1] else boxes[indexInBoxes - 1],  # One shade lighter
        boxes[indexInBoxes - 1] if charUnderCursor != boxes[0] else boxes[indexInBoxes + 1],  # One shade darker
        None  # No cursor
    ]

imageBuffer = []
def buildImageBuffer(picture):
    global imageBuffer, cursorPos, cursorChoice, cursorType, brushChoice
    refreshCursor()

    imageBuffer = deepcopy(picture)  # Start with image buffer as a copy of the picture

    imageBufferHeight = len(imageBuffer)  # Find height of image for later use
    imageBufferHeightStrL = len(str(imageBufferHeight))  # Length of height string
    imageBufferWidth = len(imageBuffer[0])  # Find width of image for later use
    imageBufferWidthStrL = len(str(imageBufferWidth))  # Length of width string

    if cursorChoice != None:  # If cursor choice is not None, set that place to the cursor char
        imageBuffer[cursorPos[1]][cursorPos[0]] = cursorType[cursorChoice]

    # Draw left and right borders
    for rowIndex, row in enumerate(imageBuffer):
        leftBorderLabel = str(rowIndex).rjust(imageBufferHeightStrL)
        row.insert(0, leftBorderLabel + '\u2551')  # Insert left border with label
        row.append('\u2551' + ('\u25c1' if rowIndex == cursorPos[1] else ' '))  # Right border plus arrow
    pictureLocation = [len(leftBorderLabel) + 1, 0]  # Top left corner of the picture

    # Draw top border
    topBorder = multiChar(pictureLocation[0] - 1)  # Add spaces for left border
    topBorder += multiChar(imageBufferWidth + 2, '\u2550', '\u2554', '\u2557')  # Middle, left, right chars
    imageBuffer.insert(0, [*topBorder])
    pictureLocation[1] += 1  # Picture is one row down now

    # Draw top arrow
    topArrowLine = multiChar(pictureLocation[0] - 1)  # Spaces for left border
    topArrowLine = multiChar(pictureLocation[0] + cursorPos[0])
    topArrowLine += '\u25bd'  # Place arrow
    topArrowLine.ljust(pictureLocation[0] + imageBufferWidth)
    imageBuffer.insert(0, [*topArrowLine])
    pictureLocation[1] += 1  # Picture is one row down now

    # Draw top text
    topText = f'\n[ BRUSH: ] [{brushChoice}]\t' \
              f'[ CURSOR: ] [{cursorType[cursorChoice]}] ( {cursorPos[0]}, {cursorPos[1]} )'
    imageBuffer.insert(0, [*topText])
    pictureLocation[1] += 1  # Picture is one row down now


    # Draw bottom border
    bottomBorder = multiChar(pictureLocation[0] - 1)
    bottomBorder += multiChar(imageBufferWidth + 2, '\u2550', first='\u255a', last='\u255d')  # Mid, L, R chars
    imageBuffer.append([*bottomBorder])

    # Draw bottom numbers
    bottomLabelsLs = []
    for x in range(0, imageBufferWidth):
        xLabel = str(x) if x % intervalXLabel == 0 else ''  # Only label if on interval
        bottomLabelsLs.append(xLabel.ljust(imageBufferWidthStrL))  # Append with max string length justification
    for x in range(0, imageBufferWidthStrL):  # For each character of the labels
        imageBuffer.append([*multiChar(imageBufferWidthStrL + 1)])  # Add empty list at bottom
        for item in bottomLabelsLs:  # Add character for this row
            imageBuffer[-1].append(item[x])
    imageBuffer.append([])

    # Draw controls/etc
    bottomText = ''
    for index, item in enumerate(boxes):
        bottomText += f'[{index + 1}] {item}\t'  # Box options
    bottomText += '\n[SPACE: PAINT] [WASD:MOVE] [H:TOGGLE CURSOR]' # Controls
    imageBuffer.append([*bottomText])

    return imageBuffer

def printPicture(picture):
    global imageBuffer
    buildImageBuffer(picture)
    os.system('cls' if os.name == 'nt' else 'clear')  # Uses correct clear console command

    for row in imageBuffer:
        print(''.join(row))  # Join elements of row and print



intervalXLabel = 5  # Customization


#  BEGIN PROGRAM
print('\n == Python Paint v1 ==')
pictureUpdatedFlag = True
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

bufferRow, picture = [], []  # Matrix: A list of lists of row positions
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
    picture.append([*multiChar(itemsPerRow)])  # Append a list of spaces

# picture now contains (rowsPerPicture) lists, each containing (itemsPerRow) items that will act as pixels
# endregion

cursorPos, brushChoice = [itemsPerRow//2, rowsPerPicture//2], boxes[0]  # Defaults
printPicture(picture)

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
    if pictureUpdatedFlag == True:
        printPicture(picture)
        pictureUpdatedFlag == False
    continue