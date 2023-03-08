import math
from typing import List, Tuple, Union
from pydub import AudioSegment
from pydub.generators import Sine

# Set the duration of the audio in milliseconds
duration = 2000

# 0 = A, 1 = A#, 2 = B, 3 = C, 4 = C#, 5 = D, 6 = D#, 7 = E, 8 = F, 9 = F#, 10 = G, 11 = G#
guitar_notes = [        
    [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7], # E2
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0], # A2
    [5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5], # D3
    [10,11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], # G3
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2], # B3
    [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7]  # E4
]

octave_notes = [
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
    
    :return: A3 = 220 Hz, A4 = 440 Hz, A5 = 880 Hz
    '''

    # Instead of 0=A, we offset it to 9=A, 10=A#, 11=B, 1=C, 2=C#, etc
    offset_to_c_note = (note+9)%12+1

    base_note = 49 # A4

    # n == B3 = 39, C4 = 40, G4 = 47, G#4 = 48, A4 = 49, B4 = 51, C5 = 52
    n = 12 * (octave - 1) + offset_to_c_note + 3
    return 2 ** ((n - base_note) / 12) * 440



# Calulate all the notes in the guitar
def get_frequency_notes() -> List[List[float]]:

    frequency_notes = []
    for string_idx in range(len(guitar_notes)):
        string = guitar_notes[string_idx]
        frequency_string = []

        # Start printing the frets from index 1
        for note_idx in range(len(string)):
            n = string[note_idx]
            # print(f"|{octave_notes[string_idx][note_idx]}{noteToChar(n)}|")
            frequency_string.append(calculateFrequency(n, octave_notes[string_idx][note_idx]))
        frequency_notes.append(frequency_string)
    return frequency_notes



# note to character
def noteToChar(note):
    '''
    Get the character of a note
    :param note: 0 = A, 1 = A#, 2 = B, 3 = C, 4 = C#, 5 = D, 6 = D#, 7 = E, 8 = F, 9 = F#, 10 = G, 11 = G#
    '''
    res = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"][note]
    return f"{res:2}"





def print_guitar_fretboard(notes: List[Tuple[int, Union[int, None]]]) -> str:
    '''
    :param notes: List of notes to print on the fretboard. Each note is a tuple of (note, octave)

    For example: to print a fretboard comtaining note A4, all A, C3, all C#

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

    # Reverse the order of the guitar_notes list, to print the thickest string at the bottom
    guitar_notes.reverse()
    octave_notes.reverse()
    # Define the number of frets on the guitar
    num_frets = 12
    # Define the ASCII art for each fretboard position
    position = "  " + " --- " * num_frets

    # Print the fret numbers
    for i in range(num_frets):
        result_str += f"{i+1:5}"

    # Print the top of the fretboard
    result_str += "\n" + position + "\n" 

    # Create a fretboard array and save all the note positions first, same dimensions as guitar_notes
    fretboard = [[None for _ in string] for string in guitar_notes]

    for string_idx in range(len(guitar_notes)):
        string = guitar_notes[string_idx]

        for note_idx in range(len(string)):
            n = string[note_idx]
            for newNote in notes:
                note, octave = newNote
                if n == note and octave and isinstance(octave, int) and octave == octave_notes[string_idx][note_idx]:
                    fretboard[string_idx][note_idx] = f"{octave}{noteToChar(n)}"
                elif n == note and not octave:
                    fretboard[string_idx][note_idx] = f" {noteToChar(n)}"

    # Print each string in reverse order
    for fret_string_idx in range(len(fretboard)):
        # Print the beginning note of the string
        result_str += noteToChar(guitar_notes[fret_string_idx][0])

        # Start printing the frets from index 1
        for note_idx in range(1, len(fretboard[fret_string_idx])):
            s = fretboard[fret_string_idx][note_idx]
            if s:
                result_str += f"|{s}|"
            else:
                result_str += "|   |"
        # Print the end of the string
        result_str += '\n'

    # Print the bottom of the fretboard
    return result_str + position + '\n'


fb = print_guitar_fretboard([(0,None), (0,4), (4, None), (3, 3)])
print(fb)
# notes = get_frequency_notes()

# # Get all the notes into sine waves
# sine_waves = [Sine(n).to_audio_segment(duration) for string in notes for n in string ]

# # Concatenate all the audio segments
# combined = sine_waves[0]
# for i in range(1, len(sine_waves)):
#   combined += sine_waves[i]

# # Export the combined audio segment as an mp3 file
# combined.export("out.mp3", format="mp3")
