# -*- coding: utf-8 -*-
import copy, area, time, util, os

# TODO: detect the neighbourhoods, from the tails
def spiral_find_neighbours(Spirals):
    pass

Up    = ( 0,-1)
Down  = ( 0, 1)
Left  = (-1, 0)
Right = ( 1, 0)

def spiral_operators(): return  {"CounterClockwise": {
                                      "Down" : [Down, Right, Up, Left],
                                      "Right": [Right, Up, Left, Down],
                                      "Up"   : [Up, Left, Down, Right],
                                      "Left" : [Left, Down, Right, Up] },
                                 "Clockwise": {
                                     "Down" : [Down, Left, Up, Right],
                                     "Left" : [Left, Up, Right, Down],
                                     "Up"   : [Up, Right, Down, Left],
                                     "Right": [Right, Down, Left, Up] }}

def _operator_next(DirectionOperators, OperatorNextCounter):
    OperatorX, OperatorY = DirectionOperators[OperatorNextCounter % 4] # we always use 4 operators
    return OperatorX, OperatorY, OperatorNextCounter+1

_Ranges = dict() # cached ranges, I don't want to recreate them always

# Spiral search from point 1, Clockwise, Down start:
#                  5   56  567  567  567  567  567  567   567   567   567  g567
#    1  1   1  41  41  41  41   418  418  418  418  418   418   418  f418  f418
#       2  32  32  32  32  32   32   329  329  329  329   329  e329  e329  e329
#                                           a   ba  cba  dcba  dcba  dcba  dcba
def spiral_from_coord(MarkCoords, Coord, Direction="CounterClockwise", Start="Down"):
    OperatorNextCounter = 0
    DirectionOperators = spiral_operators()[Direction][Start]

    SpiralCoords = [(Coord)]
    X, Y = Coord
    Repetition = 1

    while True:
        if Repetition not in _Ranges:
            _Ranges[Repetition] = range(0, Repetition) # cached ranges to avoid nonstop range creation

        # I have to repeat twice this step to create the spiral
        for _ in ["TurnFirstOperator", "TurnSecondOperator"]:
            OperatorDeltaX, OperatorDeltaY, OperatorNextCounter = _operator_next(DirectionOperators, OperatorNextCounter)
            for _ in _Ranges[Repetition]: # to follow and understand
                X += OperatorDeltaX
                Y += OperatorDeltaY
                CoordNew = (X, Y)
                if CoordNew in MarkCoords:
                    SpiralCoords.append(CoordNew)
                else:
                    return SpiralCoords

        Repetition += 1

def spiral_max_from_coord(MarkCoords, Coord):
    CoordsLongest = []
    Variations = [  ("Clockwise", "Up"),
                    ("Clockwise", "Down"),
                    ("Clockwise", "Left"),
                    ("Clockwise", "Right"),

                    ("CounterClockwise", "Up"),
                    ("CounterClockwise", "Down"),
                    ("CounterClockwise", "Left"),
                    ("CounterClockwise", "Right") ]

    for Clock, Direction in Variations:
        Spiral = spiral_from_coord(MarkCoords, Coord, Clock, Direction)
        if len(Spiral) > len(CoordsLongest):
            CoordsLongest = Spiral

    return CoordsLongest

def spiral_nonoverlap_search_in_mark(Mark):
    SpiralsInMark = {}
    CoordsTry = dict(Mark["Coords"])

    while CoordsTry:

        SpiralBiggestCoordStart = (-1, -1)
        SpiralBiggestCoords = [] # the order of coords are important to represent the spiral

        for Coord in CoordsTry:
            SpiralMaxNow = spiral_max_from_coord(CoordsTry, Coord)
            if len(SpiralMaxNow) > len(SpiralBiggestCoords):
                SpiralBiggestCoords = SpiralMaxNow
                SpiralBiggestCoordStart = Coord

        SpiralsInMark[SpiralBiggestCoordStart] = SpiralBiggestCoords
        coords_delete(CoordsTry, SpiralBiggestCoords)

    return SpiralsInMark

def coords_delete(CoordsDict, CoordsDeletedList):
    for CoordDel in CoordsDeletedList:
        # print("  del:", CoordDel)
        del CoordsDict[CoordDel]

# these chars have colors in Linux terminal, I hope in windows there are colored chars, too
# https://apps.timwhitlock.info/emoji/tables/unicode

def spirals_display(Prg, Spirals, Width, Height, SleepTime=0, Prefix="", PauseAtEnd=0, PauseAtStart=0, SaveAsFilename=None):
    SaveAsTxt = []

    CharBg = "🔸" #small orange diamond
    CharsetColorful = [
        "😎", # smiling face with sunglasses
        "🔘", #radio button,
        "🌼",
        "🍀",
        "🐙",
        "🎃", # jack-o-lantern
        "🐸",  # frog face
        "🎅", # father christmas
        "🐨",  # koala
        "🎁",  # Wrapped present,
        "🌷",  # tulip
        "🏀",  # basketball and hoop
        "😈", # smiling face with horns
        "🕐",  # clock face, one o'clock
        "🔴", #large red circle
        "🔵", #large blue circle,
        "🔆", # high brightness symbol
        "💜", #purple heart
        "🔅",  # low brightness symbol
        "🌑", # new moon symbol
        "💡",  # electric light bulb

    ]

    Area = area.make_empty(Width, Height, CharBg)
    print(area.to_string(Area, Prefix=Prefix, AfterString="\n\n", BeforeString="\n" * 33))
    time.sleep(PauseAtStart)

    for Coords in Spirals.values():
        CharColorful = CharsetColorful.pop(0)
        CharsetColorful.append(CharColorful)  # shifting elements in Colorful chars

        for X, Y in Coords:
            Area[X][Y] = CharColorful
            AreaTxt = area.to_string(Area, Prefix=Prefix, AfterString="\n\n", BeforeString="\n"*33)
            SaveAsTxt.append(AreaTxt)
            print(AreaTxt)
            if SleepTime:
                time.sleep(SleepTime)

    if PauseAtEnd:
        time.sleep(PauseAtEnd)

    if SaveAsFilename:
        util.file_write(Prg, os.path.join(Prg["DirTmpPath"], SaveAsFilename), "".join(SaveAsTxt))



