# Revision 1: MJA Initial Release
# Revision 2: MJA 3/28/20: Corrected user prompts to ask for mode.
#   Improved error checking on user input, forcing user to enter a valid note.


# noteMap is a simple dictionary of lists of strings, intended to create \
# a reference that later functions can use for constructing scales chords, etc.
# The values of this dictionary are lists because some notes have two names,
# such as Gsharp and Aflat, or Csharp and Dflat, etc.
# noteMap creates key-value pairs, where the values are notes, and the keys
# are integers from 0 to 11. Each integer represents a half-step, musically
# speaking. The values start at A and ends at G sharp/ A flat.
numToNoteMap = {0:['A','A'],1:['As','Bf'],2:['B','B'],3:['C','C'],4:['Cs','Df'],5:['D','D'], \
6:['Ds','Ef'],7:['E','E'],8:['F','F'],9:['Fs','Gf'],10:['G','G'],11:['Gs','Af']}

noteToNumMap = {'A':0,'As':1,'Bf':1,'B':2,'C':3,'Cs':4,'Df':4,'D':5, \
'Ds':6,'Ef':6,'E':7,'F':8,'Fs':9,'Gf':9,'G':10,'Gs':11}

def numToNote(num,sharps=1) :
    noteList = numToNoteMap[num]
    if sharps == 1 :
        return noteList[0]
    else :
        return noteList[1]
# end def
def noteToNum(noteName) :
    return noteToNumMap[noteName]
# end def

noteMapTup = ([0,'A','A'],[1,'As','Bf'],[2,'B','B'],[3,'C','C'], \
[4,'Cs','Df'],[5,'D','D'],[6,'Ds','Ef'],[7,'E','E'],[8,'F','F'], \
[9,'Fs','Gf'],[10,'G','G'],[11,'Gs','Af'])

# intervalMap is another tuple that operates similarly to noteMap, except it
# maps the modes to their intervals relative to the major scale. This tuple
# is used to programmatically fill in text when outputting results to the user,
# and the value at position 3 in the sublists are used to determine whether the
# next step in the current scale is a half step or a whole step away.
intervalMapTup = (  \
    [1, "Ionian",       "major",        "I",    2,  1], \
    [2, "Dorian",       "minor",        "ii",   2,  2], \
    [3, "Phrygian",     "minor",        "iii",  1,  2], \
    [4, "Lydian",       "major",        "IV",   2,  1], \
    [5, "Mixolydian",   "major",        "V",    2,  2], \
    [6, "Aeolian",      "minor",        "vi",   2,  2], \
    [7, "Locrian",      "diminished",   "vii",  1,  2]  \
)

romanMap = {1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI',7:'VII'}

# nextStep handles the transition between integers. If a proposed step exceeds
# the bounds of our noteMap, it 'starts over' at the correct value
def nextStep(currentInteger,stepSize,map) :
    lowerBound = 0
    upperBound = len(map)-1
    if currentInteger < lowerBound or currentInteger > upperBound :
        print("Error: noteMap range exceeded")
    elif currentInteger + stepSize > upperBound :
        return currentInteger + stepSize - upperBound - 1
    elif currentInteger + stepSize < lowerBound :
        return currentInteger + stepSize + upperBound + 1
    else :
        return currentInteger + stepSize
    # end else
# end def

def toRoman(number, upperCase = True) :
    if number in romanMap :
        if upperCase :
            return romanMap[number]
        else :
            return romanMap[number].lower()
        # end else
    else :
        print("toRoman: Value not in romanMap")
        return -1
    # end else
# end def

# scaleBuilder builds a scale based on an inputted root note, and other optional
# parameters, such as sharps, mode, etc. Mode defaults to 1 for the major scale
# (Ionian). Enter an integer corresponding to that modes interval in the major
# scale (2 for Dorian, 3 for Phrygian, etc.).
def scaleBuilder(rootNote, mode=1, sharps=True, octaves=1, \
        detailedPrint = False) :

    notePos = noteToNum(rootNote)
    if notePos == -1 :
        print("Error: Inputted rootNote is not a valid note name")
    # end if
    modePos = mode
    newScale = []
    for num in range(1,8) :
        newScale.append([numToNote(notePos),intervalMapTup[modePos - 1][3],intervalMapTup[modePos-1][2]])
        # intervalMapTup at modePos -1 because of counting by one in
        # intervalMap. Consider fixing this.
        notePos = nextStep(notePos,intervalMapTup[modePos - 1][4],noteMapTup)
        modePos = nextStep(modePos,1,intervalMapTup)
    # end for
    if detailedPrint == True :
        print("\tNote\tInterval\tChord Type")
        for note in newScale :
            print("\t  {}\t  {}\t\t   {}".format(note[0],note[1],note[2]))
    else :
        print("{} {}: {}".format(rootNote,intervalMapTup[mode-1][1],newScale))
    # end else
#end def

# generic function for getting input from user
def getUserInput(message = "Please enter a value (Press 'x' to escape): ") :
    userInput = input(message)
    if userInput == 'X' or userInput =='x' :
        print("Exiting program")
        exit()
    else :
        return userInput
    # end else
# end def

#formats the root input from the user
def formatRoot(userInput):
    root = ''
    if len(userInput) == 1:
        root = userInput.upper()
    elif len(userInput) == 2:
        root = '{}{}'.format(userInput[0].upper(),userInput[1].lower())
    else:
        root = -1
    return root
    # end else
# end def

# gets the root from the user, formats it, and returns the properly formatted root
def getRootFromUser():
    rootErrorMessage = "**Invalid input! Please enter a valid root name.**"
    message = "Please enter a root note A-G (Press 'x' to escape): "
    acceptableInput = False
    root = ''
    while acceptableInput != True:
        userInput = getUserInput(message)
        root = formatRoot(userInput)
        if root in noteToNumMap:
            return root
        elif root.upper() == 'X':
            break
        else:
            acceptableInput = False
            continue
        # end else
    # end while
# end def

def scaleLooper() :
    for count in range(100) :
        root = getRootFromUser()
        mode = int(getUserInput(message = "Please enter a mode using 1-7 (1 for Ionian, 6 for Aeolian, etc.) (Press 'x' to escape): "))
        scaleBuilder(root, mode, detailedPrint = True)
    # end for
# end for

#getRootFromUser()
scaleLooper()
