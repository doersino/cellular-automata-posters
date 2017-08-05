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

import os
import math
from random import randint
import cairocffi as cairo


###########
# OPTIONS #
###########

rule = 30  # See http://mathworld.wolfram.com/ElementaryCellularAutomaton.html
           # but note that "higher" rules beyond 255 (e.g. rule 31415926, see
           # http://www.wolframalpha.com/input/?i=rule+31415926) are also
           # supported (for legibility reasons sans rule icons on the label).

initialCondition = 'middle'  # 'middle' → '...0001000...'
                             # 'left'   → '1000...'
                             # 'right'  → '...0001'
                             # 'random' → '01101011100...' or similar.
                             # Or a bitstring like '000101010' (if the string
                             # length does not match the width specified below,
                             # it will be truncated or padded with zeros).

cellShape = 'square'  # 'square'  → □
                      # 'circle'  → ◯ (Note that this hides the grid, see
                      #                gridMode option below.)

width  = 280     # ⎤ Dimensions (width in cells, height in generations) of grid.
height = 'auto'  # ⎦ Either one (but not both) can be set to 'auto' to fill the
                 #   page. Tested up to 1000×1416, which takes about 30s to
                 #   generate (but be aware that displaying 1.5M shapes tends to
                 #   choke PDF viewers).

offset = 0  # From which generation on should the states be shown? Handy for
            # rules that take a few generations to converge to a nice repeating
            # pattern. Can also be a decimal number (e.g. 10.5) or negative to
            # adjust the vertical display offset.

angle = 0  # Rotation angle in degrees (tested between -45° and 45°). To fill
           # the resulting blank spots in the corners, the dimensions of the
           # grid are increased to keep the displayed cell size constant (as
           # opposed to scaling up the grid).

colorScheme = 'blue'  # 'yellow', 'green', 'pink', 'salmon', 'red', 'blue',
                      # 'lime', 'orange', 'darkblue', 'violet', 'gray' or a tuple
                      # of the form "('#ffe183', '#ffa24b')", with the first
                      # element being the living cell color and the second
                      # element being the dead cell color.

gridMode = 'dead'  # 'living' → Grid lines are same color as living cells.
                   # 'dead'   → Same for dead cells.
                   # 0.5      → Equal mix of both colors (other ratios between
                   #            0 and 1 are possible as well).
                   # None     → Hide grid. Makes the script run significantly
                   #            faster, especially if few living cells exist.
                   #            Implied when cellShape is set to 'circle'.

showLabel = True  # Whether to show the label containing rule number & icons.

font = 'Helvetica'  # Any font installed on your system. Helvetica, if you've
                    # got it, looks neat. For other fonts, you might need to dig
                    # into the code below and adjust the vertical spacing.

wolframAlphaAppID = ''  # A non-empty string enables display of Wolfram|Alpha-
                        # sourced "fun facts" as part of the label. To get an
                        # AppID, register for a developer account at
                        # https://developer.wolframalpha.com/portal/apisignup.html
                        # and click the "Get an AppID" button.

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

log = lambda s: debug and print(s)

colorSchemes = {'yellow':   ('#ffe183', '#ffa24b'),
                'green':    ('#bddba6', '#83b35e'),
                'pink':     ('#000000', '#b84c8c'),
                'salmon':   ('#ffb1b0', '#c24848'),
                'red':      ('#fc5e5d', '#8e0033'),
                'blue':     ('#4b669b', '#c0d6ff'),
                'lime':     ('#cbe638', '#98ad20'),
                'orange':   ('#ffe5db', '#f2936d'),
                'darkblue': ('#1baaef', '#0d6ca5'),
                'violet':   ('#e9c3fe', '#6f5b7e'),
                'gray':     ('#dddddd', '#333333')}

# option overrides
if 'CAP_RULE' in os.environ:
    rule = int(os.environ['CAP_RULE'])
if 'CAP_INITIALCONDITION' in os.environ:
    initialCondition = os.environ['CAP_INITIALCONDITION']
if 'CAP_CELLSHAPE' in os.environ:
    cellShape = os.environ['CAP_CELLSHAPE']
if 'CAP_WIDTH' in os.environ:
    if os.environ['CAP_WIDTH'] == 'auto':
        width = 'auto'
    else:
        width = int(os.environ['CAP_WIDTH'])
if 'CAP_HEIGHT' in os.environ:
    if os.environ['CAP_HEIGHT'] == 'auto':
        height = 'auto'
    else:
        height = int(os.environ['CAP_HEIGHT'])
if 'CAP_OFFSET' in os.environ:
    offset = float(os.environ['CAP_OFFSET'])
if 'CAP_ANGLE' in os.environ:
    angle = float(os.environ['CAP_ANGLE'])
if 'CAP_COLORSCHEME' in os.environ:
    if os.environ['CAP_COLORSCHEME'] in colorSchemes.keys():
        colorScheme = os.environ['CAP_COLORSCHEME']
    else:
        colorScheme = eval(os.environ['CAP_COLORSCHEME'])
if 'CAP_GRIDMODE' in os.environ:
    if os.environ['CAP_GRIDMODE'] in ['living', 'dead']:
        gridMode = os.environ['CAP_GRIDMODE']
    elif os.environ['CAP_GRIDMODE'] == 'None':
        gridMode = None
    else:
        gridMode = float(os.environ['CAP_GRIDMODE'])
if 'CAP_SHOWLABEL' in os.environ:
    showLabel = os.environ['CAP_SHOWLABEL'] == 'True'
if 'CAP_FONT' in os.environ:
    font = os.environ['CAP_FONT']
if 'CAP_WOLFRAMALPHAAPPID' in os.environ:
    wolframAlphaAppID = os.environ['CAP_WOLFRAMALPHAAPPID']
if 'CAP_PAGEWIDTH' in os.environ:
    pageWidth = int(os.environ['CAP_PAGEWIDTH'])
if 'CAP_PAGEHEIGHT' in os.environ:
    pageHeight = int(os.environ['CAP_PAGEHEIGHT'])
if 'CAP_FILENAME' in os.environ:
    filename = os.environ['CAP_FILENAME']
else:
    filename = 'rule{}.pdf'.format(rule)
if 'CAP_DEBUG' in os.environ:
    debug = os.environ['CAP_DEBUG'] == 'True'

# offset: split into decimal and integer part
generationOffset = max(0, int(offset))
displayOffset    = offset - generationOffset

# dimensions
if width == 'auto':
    width = math.floor((pageWidth / pageHeight) * height)
if height == 'auto':
    height = math.ceil((pageHeight / pageWidth) * width)
    if displayOffset > 0:
        height += 1

# rotation
angle = math.radians(angle)
requiredPageWidth  = math.sin(abs(angle)) * pageHeight + math.cos(abs(angle)) * pageWidth
requiredPageHeight = math.sin(abs(angle)) * pageWidth  + math.cos(abs(angle)) * pageHeight

translation = ((requiredPageWidth - pageWidth) / 2,
               (requiredPageHeight - pageHeight) / 2)

originalWidth = width
width  = math.ceil(width * requiredPageWidth / pageWidth)
height = math.ceil(height * requiredPageHeight / pageHeight)

# color scheme selection
if isinstance(colorScheme, str):
    colors = colorSchemes[colorScheme]
else:
    colors = colorScheme

torgb = lambda hex: tuple(int((hex.lstrip('#'))[i:i+2], 16)/255 for i in (0, 2, 4))
livingColor, deadColor = map(torgb, colors)

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

# fetch and format fun facts
funFacts = []
if showLabel and wolframAlphaAppID:
    import wolframalpha

    log('Fetching fun facts from Wolfram|Alpha...')
    try:
        client = wolframalpha.Client(wolframAlphaAppID)
        res = client.query('rule {}'.format(rule))
        for pod in res.pods:
            if pod['@id'] == 'RuleEquivalences':
                for sub in pod.subpods:
                    tableRows = sub.plaintext.split('\n')
                    tableHead = tableRows[0].split(' | ')
                    tableData = tableRows[1].split(' | ')
                    tableData = [int(''.join(c for c in r if c.isdigit())) for r in tableData]
                    ruleEquivalences = dict(zip(tableHead, tableData))
                    if ruleEquivalences.get('left-right', rule) != rule:
                            funFacts.append("Rule {} is this rule's mirror image.".format(ruleEquivalences['left-right']))
                    if ruleEquivalences.get('color', rule) != rule:
                        funFacts.append("Rule {} is this rule's color-inverted equivalent.".format(ruleEquivalences['color']))
                    if ruleEquivalences.get('both', rule) != rule:
                        funFacts.append("Rule {} is this rule's color-inverted mirror image.".format(ruleEquivalences['both']))
            if pod['@id'] == 'BooleanForm':
                for sub in pod.subpods:
                    booleanForm = ' '.join(sub.plaintext.split()).replace('|->', '~>')
                    funFacts.append("The boolean form of rule {} is {}.".format(rule, booleanForm))
            if pod['@id'] == 'Properties':
                for sub in pod.subpods:
                    funFacts.append(sub.plaintext)
    except Exception as e:
        if debug:
            raise
        else:
            print('Skipping fun facts: An exception occurred while trying to fetch them from Wolfram|Alpha. Try again or enable the debugging flag at the bottom of the options and rerun to view the exception.')
    if len(funFacts) == 1:
        funFacts.insert(0, 'Fun fact:')
    elif len(funFacts) > 1:
        funFacts.insert(0, 'Fun facts:')


######################
# CELLULAR AUTOMATON #
######################

# compute width (i.e. number of cells) of current state to consider
currentStateWidth = max(3, math.ceil(math.log2(math.log2(rule+1))))

# convert rule to binary and pad to required length
ruleBinary = format(rule, 'b').zfill(int(math.pow(2,currentStateWidth)))

# compute transistions, i.e. set up mapping from each possible current
# configuration to the rule-defined next state
transistions = {bin(currentState)[2:].zfill(currentStateWidth): resultingState for currentState, resultingState in enumerate(reversed(ruleBinary))}

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
    currentStatePadded = currentState[-math.floor(currentStateWidth/2):width] + currentState + currentState[0:currentStateWidth-math.floor(currentStateWidth/2)-1]

    nextState = ''
    for x in range(0, width):
        pattern = currentStatePadded[x:x+currentStateWidth]
        nextState += transistions[pattern]
    grid.append(nextState)


###########
# DRAWING #
###########

grid = grid[generationOffset:]  # discard any unwanted generations

cellSize = pageWidth / originalWidth
xPositions = [x * cellSize - translation[0] for x in range(0,width)]
yPositions = [(y - displayOffset) * cellSize - translation[1] for y in range(0,height+1)]

log('Drawing to "{}"...'.format(filename))

surface = cairo.PDFSurface(filename, pageWidth, pageHeight)
context = cairo.Context(surface)

# fill with background color
with context:
    context.set_source_rgb(deadColor[0], deadColor[1], deadColor[2])
    context.paint()

# draw cells and grid
context.set_line_width(cellSize / 16)
context.translate(pageWidth / 2, pageHeight / 2)
context.rotate(angle)
context.translate(-pageWidth / 2, -pageHeight / 2)
for y, row in enumerate(grid):
    log('Drawing row {}/{}...'.format(y, height))
    for x, cell in enumerate(row):
        xP = xPositions[x]
        yP = yPositions[y]
        if cell == '1':
            context.set_source_rgb(livingColor[0], livingColor[1], livingColor[2])
            if cellShape == 'square':
                context.rectangle(xP, yP, cellSize, cellSize)
            else:
                context.arc(xP + cellSize / 2, yP + cellSize / 2, cellSize / 2, 0, 2*math.pi)
            context.fill()
        if gridColor is not None and cellShape == 'square':
            context.set_source_rgb(gridColor[0], gridColor[1], gridColor[2])
            context.rectangle(xP, yP, cellSize, cellSize)
            context.stroke()
context.translate(pageWidth / 2, pageHeight / 2)
context.rotate(-angle)
context.translate(-pageWidth / 2, -pageHeight / 2)

if showLabel:
    log('Drawing label...')

    pageSize = min(pageWidth, pageHeight)  # enables a kind of responsive design

    # format fun facts and compute height of label based on number of lines
    funFactsLines = []
    labelHeight = 0.14*pageSize
    if funFacts:
        context.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        context.set_font_size(0.015*pageSize)
        context.set_source_rgb(0, 0, 0)
        funFacts =  ' '.join(funFacts).split(' ')

        # split long string into lines depending on page width
        i = 0
        while funFacts:
            rest = []
            lineWidth = context.text_extents(' '.join(funFacts))[2]
            while lineWidth > pageWidth - 0.2 * pageSize:
                rest.insert(0, funFacts[-1])
                funFacts = funFacts[:-1]
                lineWidth = context.text_extents(' '.join(funFacts))[2]
            funFactsLines.append(' '.join(funFacts))
            funFacts = rest
            i += 1
        funFactLineHeight = context.text_extents(funFactsLines[0])[3]  # via http://blog.mathieu-leplatre.info/text-extents-with-python-cairo.html
        labelHeight += i*funFactLineHeight*1.5 + 0.035*pageSize

    # draw white box for label
    context.set_source_rgb(1, 1, 1)
    context.rectangle(0, 0.9*pageHeight-labelHeight, pageWidth, labelHeight)
    context.fill()

    # draw drop shadows, top one slightly smaller than bottom one to simulate
    # soft light from just above
    gradient = cairo.LinearGradient(0, 0.9*pageHeight-labelHeight, 0, 0.9*pageHeight-labelHeight-0.004*pageSize)
    gradient.add_color_stop_rgba(0, 0, 0, 0, 0.13)
    gradient.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    context.rectangle(0, 0.9*pageHeight-labelHeight-0.004*pageSize, pageWidth, 0.004*pageSize)
    context.set_source(gradient)
    context.fill()

    gradient = cairo.LinearGradient(0, 0.9*pageHeight, 0, 0.9*pageHeight+0.006*pageSize)
    gradient.add_color_stop_rgba(0, 0, 0, 0, 0.21)
    gradient.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    context.rectangle(0, 0.9*pageHeight, pageWidth, 0.006*pageSize)
    context.set_source(gradient)
    context.fill()

    # draw text
    context.move_to(0.1*pageSize, 0.9*pageHeight-labelHeight+0.0895*pageSize)
    context.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(0.054*pageSize)
    context.set_source_rgb(0, 0, 0)
    context.show_text(u'RULE {}'.format(rule))

    # draw fun facts
    if funFactsLines:
        context.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        context.set_font_size(0.015*pageSize)
        context.set_source_rgb(0, 0, 0)
        for i, l in enumerate(funFactsLines):
            context.move_to(0.1*pageSize, 0.9*pageHeight - labelHeight + 0.14*pageSize + i*funFactLineHeight*1.5)
            context.show_text(l)

    # draw rule icons (only for simple rules, would not be not legible for
    # "higher" rules)
    if currentStateWidth == 3:
        xOffset = pageWidth-0.115*pageSize
        yOffset = 0.9*pageHeight-labelHeight+0.056*pageSize
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
            if transistions[neighbors] == '1':
                context.rectangle(xOffset+cellSize*2.5, yOffset+cellSize*1.25, cellSize, cellSize)
                context.fill()
            context.rectangle(xOffset+cellSize*2.5, yOffset+cellSize*1.25, cellSize, cellSize)
            context.stroke()

            xOffset -= cellSize * 0.7

log('Almost there, writing to disk...')
