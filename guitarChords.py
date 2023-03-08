from pathlib import Path
from typing import List, Tuple, Union
from pydub import AudioSegment
from pydub.generators import Square


# 0 = A, 1 = A#, 2 = B, 3 = C, 4 = C#, 5 = D, 6 = D#, 7 = E, 8 = F, 9 = F#, 10 = G, 11 = G#
GUITAR_NOTES = [        
    [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7], # E2
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0], # A2
    [5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5], # D3
    [10,11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], # G3
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2], # B3
    [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7]  # E4
]

OCTAVE_NOTES = [
    [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
    [2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4],
    [3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4],
    [3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
]

# Formula to calculate the frequency of a note : f = 2^(n/12) * 440
def calculateFrequency(note=0, octave=4):
    '''
    Get the frequency of a note
    :param note: 0 = A, 1 = A#, 2 = B, 3 = C, 4 = C#, 5 = D, 6 = D#, 7 = E, 8 = F, 9 = F#, 10 = G, 11 = G#
    :param octave: default is 4, which link to A4 = 440 Hz
    
    So, octave calculate differently:, it increment at C note, not A note:
    For example note, base_note, frequency:
    - B3 = 39 = 246 Hz
    - C4 = 40 = 261 Hz
    - C#4 = 41 = 277 Hz
    - D4 = 42 = 294 Hz
    - D#4 = 43 = 311 Hz
    - E4 = 44 = 330 Hz
    - F4 = 45 = 349 Hz
    - F#4 = 46 = 370 Hz
    - G4 = 47 = 392 Hz
    - G#4 = 48 = 415 Hz
    - A4 = 49 = 440 Hz
    - A#4 = 50 = 466 Hz
    - B4 = 51 = 494 Hz
    - C5 = 52 = 523 Hz

    We need an equation to calculate the order of each note, with respect to A4
    
    To calculate this note from base_note A4 = 49, we use this equation:
    n = 12[Tone] * (Octave - 1) + offset[C = 1, C# = 2, A = 9, B = 11, etc]
         + 3[Offset back to A note, because base_note is A4 started at A note = 0 in GUITAR_NOTES]

    :return: A3 = 220 Hz, A4 = 440 Hz, A5 = 880 Hz
    '''

    # Instead of 0=A, we offset it to 9=A, 10=A#, 11=B, 1=C, 2=C#, etc
    offset_to_c_note = (note+9)%12+1

    base_note = 49 # A4

    # n == B3 = 39, C4 = 40, G4 = 47, G#4 = 48, A4 = 49, B4 = 51, C5 = 52
    n = 12 * (octave - 1) + offset_to_c_note + 3
    return 2 ** ((n - base_note) / 12) * 440



# note to character
def noteToChar(note):
    '''
    Get the character of a note
    :param note: 0 = A, 1 = A#, 2 = B, 3 = C, 4 = C#, 5 = D, 6 = D#, 7 = E, 8 = F, 9 = F#, 10 = G, 11 = G#
    '''
    res = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"][note]
    return res





def print_guitar_fretboard(notes: List[Tuple[int, Union[int, None]]]
                            , fretboard_guitar_notes: List[List[int]]
                            , fretboard_notes_octave: List[List[int]]) -> str:
    '''
    :param notes: List of notes to print on the fretboard. Each note is a tuple of (note, octave)

    For example: to print a fretboard comtaining note A4, all A, C3, all C#
    print_guitar_fretboard([(0,None), (0,4), (4, None), (3, 3)])

    :return:
    1    2    3    4    5    6    7    8    9   10   11   12
   ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---
E |   ||   ||   ||   ||4A ||   ||   ||   || C#||   ||   ||   |
B |   || C#||   ||   ||   ||   ||   ||   ||   ||4A ||   ||   |
G |   || A ||   ||   ||   || C#||   ||   ||   ||   ||   ||   |
D |   ||   ||   ||   ||   ||   || A ||   ||   ||   || C#||   |
A |   ||   ||3C || C#||   ||   ||   ||   ||   ||   ||   || A |
E |   ||   ||   ||   || A ||   ||   ||3C || C#||   ||   ||   |
   ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---  ---
    '''
    result_str = ""

    # Define the number of frets on the guitar, remove the first element, as it doesnt need to press on the fret to play that note
    num_frets = len(fretboard_guitar_notes[0]) - 1
    # Define the ASCII art for each fretboard position
    position = "  " + " --- " * num_frets

    # Print the fret numbers
    for i in range(num_frets):
        result_str += f"{i+1:5}"

    # Print the top of the fretboard
    result_str += "\n" + position + "\n" 

    # Create a fretboard array and save all the note positions first, same dimensions as guitar_notes
    fretboard = [[None for _ in string] for string in fretboard_guitar_notes]

    for string_idx in range(len(fretboard_guitar_notes)):
        string = fretboard_guitar_notes[string_idx]

        for note_idx in range(len(string)):
            n = string[note_idx]
            for note, octave in notes:
                if n == note and octave and isinstance(octave, int) and octave == fretboard_notes_octave[string_idx][note_idx]:
                    fretboard[string_idx][note_idx] = f"{octave}{noteToChar(n)}"
                elif n == note and not octave:
                    fretboard[string_idx][note_idx] = f" {noteToChar(n)}"

    # Print each string in reverse order
    for fret_string_idx in range(len(fretboard)):
        # Print the beginning note of the string
        result_str += noteToChar(fretboard_guitar_notes[fret_string_idx][0])

        # Start printing the frets from index 1
        for note_idx in range(1, len(fretboard[fret_string_idx])):
            s = fretboard[fret_string_idx][note_idx]
            if s:
                result_str += f"|{s:3}|"
            else:
                result_str += "|   |"
        # Print the end of the string
        result_str += '\n'

    # Print the bottom of the fretboard
    return result_str + position + '\n'


# Convert note to sound frequency file
def convertToSound(notes: List[Tuple[int, int]], duration=750) -> str:
    '''
    Convert a list of notes to an audio file
    :param notes: List of notes to print on the fretboard. Each note is a tuple of (note, octave)
    :param duration: Duration of each note in milliseconds
    :return: None
    '''
    # Initialize an empty audio segment
    wave = AudioSegment.silent(duration=0)
    filename = ""

    # Get all the notes into sine waves
    for note, octave in notes:
        wave += Square(calculateFrequency(note, octave)).to_audio_segment(duration)
        filename += f"_{noteToChar(note)}{octave}"

    # Export the combined audio segment as an mp3 file
    Path('audio/').mkdir(parents=True, exist_ok=True)
    wave.export("audio/"+filename[1:]+".mp3", format="mp3")

    return filename[1:]+".mp3"


def getChords(note: int, chords: List[int], fretboard_guitar_notes: List[List[int]], fretboard_notes_octave: List[List[int]]) -> List[Tuple[int, int]]:
    '''
    Given a note, find all the chords that contain that note

    :param chords: E.g. A major chord => A, C#, E => [0, 4, 7]

    For example: to find all the A major chords, call 
    majorChords(0, [0,4,7], fretboard_guitar_notes, fretboard_notes_octave)
    '''
    # Find all the major chords ( 0, 4, 7) inside the fretboard_guitar_notes
    resultChords = set()
    for s_idx, stirng in enumerate(fretboard_guitar_notes):
        for n_idx, n in enumerate(stirng):
            if n in [note + c for c in chords]:
                resultChords.add((n, fretboard_notes_octave[s_idx][n_idx]))
    return [c for c in resultChords]


def getMajorChords(note: int) -> List[Tuple[int, int]]:
    '''
    Given a note, find all the major chords that contain that note
    For example: to find all the A major chords, call majorChords(0)
    '''
    majorChord = [0,4,7]
    return getChords(note, majorChord, GUITAR_NOTES, OCTAVE_NOTES)

def getMinorChords(note: int) -> List[Tuple[int, int]]:
    minorChord = [0,3,7]
    return getChords(note, minorChord, GUITAR_NOTES, OCTAVE_NOTES)

if __name__ == "__main__":
    # Reverse the order of the GUITAR_NOTES list, to print the thickest string at the bottom
    guitar_notes = [GUITAR_NOTES[i] for i in range(len(GUITAR_NOTES)-1, -1, -1)]
    octave_notes = [OCTAVE_NOTES[i] for i in range(len(OCTAVE_NOTES)-1, -1, -1)]


    aMajor = getMinorChords(0)
    print(print_guitar_fretboard(aMajor, guitar_notes, octave_notes))
