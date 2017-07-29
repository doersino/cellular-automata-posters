#!/usr/bin/env python3

# Generate cellular automata posters as PDF files.
# https://github.com/doersino/cellular-automata-posters
#
# License info, setup instructions and usage examples can be found as part of
# the GitHub repository linked above.
#
# (Inspired by a Reddit post by /u/collatz_conjecture: https://redd.it/6bg60e --
# all credit goes to them, while any criticism (e.g. for taking their idea and
# running with it) is to be directed at me: https://github.com/doersino)

import math
from random import randint
import cairocffi as cairo


###########
# OPTIONS #
###########

rule = 30  # Between 0 and 255, see http://mathworld.wolfram.com/ElementaryCellularAutomaton.html

initialCondition = 'middle'  # 'middle' → '...0001000...'
                             # 'left'   → '1000...'
                             # 'right'  → '...0001'
                             # 'random' → '01101011100...' or similar.
                             # Or a bitstring like '000101010' (if the string
                             # length does not match the width specified below,
                             # it will be truncated or padded with zeros).

offset = 0  # From which generation on should the states be shown? Can also
            # be a (positive!) decimal number (e.g. 10.5) for minute
            # adjustments.

width  = 280     # ⎤ Dimensions (width in cells, height in generations) of grid.
height = 'auto'  # ⎦ Either one (but not both) can be set to 'auto' to fill the
                 #   page. Tested up to 1000×1416, which takes about 30s to
                 #   generate (but be aware that displaying 1.5M shapes tends to
                 #   choke PDF viewers).

colorScheme = 'blue'  # 'yellow', 'green', 'pink', 'salmon', 'red', 'blue',
                      # 'lime', 'orange', 'violet', 'gray' or a tuple of the
                      # form "('#ffe183', '#ffa24b')", with the first element
                      # being the living cell color and the second element being
                      # the dead cell color.

gridMode = 'dead'  # 'living' → Grid lines are same color as living cells.
                   # 'dead'   → Same for dead cells.
                   # 0.5      → Equal mix of both colors (other ratios between
                   #            0 and 1 are possible as well).
                   # None     → Hide grid. Makes the script run significantly
                   #            faster, especially if few living cells exist.

showLabel = True  # Whether to show the label.

font = 'Helvetica'  # Any font installed on your system. Helvetica, if you've
                    # got it, looks neat. For other fonts, you might need to dig
                    # into the code below and adjust the vertical spacing.

pageWidth  = 595  # ⎤ Page dimensions in PostScript points (i.e. ¹/₇₂ inch). The
pageHeight = 842  # ⎦ default values (595, 842) correspond to DIN A4. Unusual
                  #   aspect ratios should work just fine, though. Small values
                  #   (< 10) lead to distortions.

filename = 'rule{}.pdf'.format(rule)  # Output PDF filename.

debug = False   # Will output some rather verbose status info such as the initial
                # state (useful for reproducability when initialCondition =
                # 'random').


######################
# OPTIONS PROCESSING #
######################

# offset: split into decimal and integer part
generationOffset = int(offset)
displayOffset    = offset - generationOffset

# dimensions
if width == 'auto':
    width = math.floor((pageWidth / pageHeight) * height)
if height == 'auto':
    height = math.ceil((pageHeight / pageWidth) * width)
    if displayOffset > 0:
        height += 1

# color scheme
if colorScheme == 'yellow':
    colors = ('#ffe183', '#ffa24b')
elif colorScheme == 'green':
    colors = ('#bddba6', '#83b35e')
elif colorScheme == 'pink':
    colors = ('#000000', '#b84c8c')
elif colorScheme == 'salmon':
    colors = ('#ffb1b0', '#c24848')
elif colorScheme == 'red':
    colors = ('#fc5e5d', '#8e0033')
elif colorScheme == 'blue':
    colors = ('#4b669b', '#c0d6ff')
elif colorScheme == 'lime':
    colors = ('#cbe638', '#98ad20')
elif colorScheme == 'orange':
    colors = ('#ffe5db', '#f2936d')
elif colorScheme == 'violet':
    colors = ('#e9c3fe', '#6f5b7e')
elif colorScheme == 'gray':
    colors = ('#dddddd', '#333333')
else:
    colors = colorScheme

torgb = lambda hex: tuple(int((hex.lstrip('#'))[i:i+2], 16)/255 for i in (0, 2, 4))

livingColor = torgb(colors[0])
deadColor  = torgb(colors[1])

# grid
if gridMode == 'living':
    gridColor = livingColor
elif gridMode == 'dead':
    gridColor = deadColor
elif gridMode is None:
    gridColor = None
else:
    gridRatio = float(gridMode)
    gridColor = [gridRatio * lc + (1 - gridRatio) * dc for lc, dc in zip(livingColor, deadColor)]

# debug
log = lambda s: debug and print(s)


######################
# CELLULAR AUTOMATON #
######################

# set up ca rules based on rule number
ruleBinary = format(rule, 'b').zfill(8)
transistions = {
    '111': ruleBinary[0],
    '110': ruleBinary[1],
    '101': ruleBinary[2],
    '100': ruleBinary[3],
    '011': ruleBinary[4],
    '010': ruleBinary[5],
    '001': ruleBinary[6],
    '000': ruleBinary[7]
}

# generate initial state
if initialCondition == 'middle':
    initialState = list('0' * width)
    initialState[int(width/2)] = '1'
elif initialCondition == 'left':
    initialState = '1' + '0' * (width-1)
elif initialCondition == 'right':
    initialState = '0' * (width-1) + '1'
elif initialCondition == 'random':
    initialState = [str(randint(0,1)) for b in range(0,width)]
else:
    initialState = (initialCondition[0:width])[::-1].zfill(width)[::-1]

log('Initial state: ' + ''.join(initialState))
grid = [''.join(initialState)]  # list of sucessive states

# run ca to generate grid
log('Running rule {} cellular automaton...'.format(rule))
for y in range(0, height + generationOffset):
    currentState = grid[y]
    log(currentState)

    nextState = ''
    for x in range(0, width):
        currentStatePadded = currentState[-1] + currentState + currentState[0]
        pattern = currentStatePadded[x:x+3]
        nextState += transistions[pattern]
    grid.append(nextState)


###########
# DRAWING #
###########

grid = grid[generationOffset:]  # discard any unwanted generations

cellSize = pageWidth / width
xPositions = [x * cellSize for x in range(0,width)]
yPositions = [(y - displayOffset) * cellSize for y in range(0,height+1)]

log('Drawing to "{}"...'.format(filename))

surface = cairo.PDFSurface(filename, pageWidth, pageHeight)
context = cairo.Context(surface)

# fill with background color
with context:
    context.set_source_rgb(deadColor[0], deadColor[1], deadColor[2])
    context.paint()

# draw cells and grid
context.set_line_width(cellSize / 16)
for y, row in enumerate(grid):
    log('Drawing row {}/{}...'.format(y, height))
    for x, cell in enumerate(row):
        xP = xPositions[x]
        yP = yPositions[y]
        if cell == '1':
            context.set_source_rgb(livingColor[0], livingColor[1], livingColor[2])
            context.rectangle(xP, yP, cellSize, cellSize)
            context.fill()
        if gridColor is not None:
            context.set_source_rgb(gridColor[0], gridColor[1], gridColor[2])
            context.rectangle(xP, yP, cellSize, cellSize)
            context.stroke()

if showLabel:
    log('Drawing label...')

    pageSize = min(pageWidth, pageHeight)  # enables a kind of responsive design

    # draw white box for label
    context.set_source_rgb(1, 1, 1)
    context.rectangle(0, 0.9*pageHeight-0.14*pageSize, pageWidth, 0.14*pageSize)
    context.fill()

    # draw drop shadows, top one slightly smaller than bottom one to simulate soft light from just above
    gradient = cairo.LinearGradient(0, 0.9*pageHeight-0.14*pageSize, 0, 0.9*pageHeight-0.14*pageSize-0.004*pageSize)
    gradient.add_color_stop_rgba(0, 0, 0, 0, 0.1)
    gradient.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    context.rectangle(0, 0.9*pageHeight-0.14*pageSize-0.004*pageSize, pageWidth, 0.004*pageSize)
    context.set_source(gradient)
    context.fill()

    gradient = cairo.LinearGradient(0, 0.9*pageHeight, 0, 0.9*pageHeight+0.006*pageSize)
    gradient.add_color_stop_rgba(0, 0, 0, 0, 0.20)
    gradient.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    context.rectangle(0, 0.9*pageHeight, pageWidth, 0.006*pageSize)
    context.set_source(gradient)
    context.fill()

    # draw text
    context.move_to(0.1*pageSize, 0.9*pageHeight-0.0505*pageSize)
    context.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(0.054*pageSize)
    context.set_source_rgb(0, 0, 0)
    context.show_text(u'RULE {}'.format(rule))

    # draw rules explainer
    xOffset = pageWidth-0.115*pageSize
    yOffset = 0.9*pageHeight-0.084*pageSize
    cellSize = pageSize/78

    context.set_line_width(cellSize / 10)
    context.set_source_rgb(0, 0, 0)
    for neighbors in sorted(transistions.keys()):
        for cell in neighbors[::-1]:
            if cell == '1':
                context.rectangle(xOffset, yOffset, cellSize, cellSize)
                context.fill()
            context.rectangle(xOffset, yOffset, cellSize, cellSize)
            context.stroke()
            xOffset -= cellSize * 1.25
        #print(transistions[thing])  # 1.1 below and -2.2 in x
        if transistions[neighbors] == '1':
            context.rectangle(xOffset+cellSize*2.5, yOffset+cellSize*1.25, cellSize, cellSize)
            context.fill()
        context.rectangle(xOffset+cellSize*2.5, yOffset+cellSize*1.25, cellSize, cellSize)
        context.stroke()

        xOffset -= cellSize * 0.7

log('Almost there, writing to disk...')
