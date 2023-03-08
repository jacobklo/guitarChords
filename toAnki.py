from __future__ import annotations
from pathlib import Path
from typing import List
import hashlib
import genanki

from guitarChords import GUITAR_NOTES, OCTAVE_NOTES, calculateFrequency, noteToChar, print_guitar_fretboard, convertToSound


def convertguitarNotes2Anki(notes_chars: List[str], notes_fretboard: List[str], notes_sound: List[str]):
  my_model = MyModel('GuitarChordsModel', fields=[{'name': 'Question'}, {'name': 'Answer'}, {'name': 'Sound'}],
  front_html=QUESTION, back_html=ANSWER, css=STYLE)

  deckName = 'GuitarChords::Notes'
  my_deck = genanki.Deck(deck_id=abs(hash(deckName)) % (10 ** 10), name=deckName)

  for i,n in enumerate(notes_chars):
    newNotes = genanki.Note(model=my_model, fields=[n, notes_fretboard[i], "[sound:"+notes_sound[i]+"]"], tags=[deckName])
    my_deck.add_note(newNotes)

  audio_path = Path(r'audio').glob('**/*')
  audios = ['audio/'+x.name for x in audio_path if x.is_file()]

  anki_output = genanki.Package(my_deck)
  anki_output.media_files = audios
  anki_output.write_to_file('GuitarNotes.apkg')



class MyModel(genanki.Model):

  def __init__(self, name: str, fields: List, front_html: str, back_html: str, css: str):
    hash_object = hashlib.sha1(name.encode('utf-8'))
    hex_dig = int(hash_object.hexdigest(), 16) % (10 ** 10)
    
    templates = [
      {
        'name': 'GuitarChordsCard',
        'qfmt': front_html,
        'afmt': back_html,
      }
    ]
    super(MyModel, self).__init__(model_id=hex_dig, name=name, fields=fields, templates=templates, css=css)



QUESTION = '''
<div class="front">{{Question}}</div>
'''


ANSWER = '''
<div class="back">
{{Answer}}

{{Sound}}
</div>


'''


STYLE = '''
.card {
 font-family: 'DejaVu Sans Mono';
 text-align: left;
 color: white;
 background-color: rgba(42, 129, 151,1);
 text-shadow: 0px 4px 3px rgba(0,0,0,0.4),
             0px 8px 13px rgba(0,0,0,0.1),
             0px 18px 23px rgba(0,0,0,0.1);
}

.front {
	font-size: 14px;
}

.back {
	font-size: 14px;

}

div.o9Q4V2vd {
  margin-bottom: 50px;
}


@font-face { font-family: DejaVu Sans Mono; src: url('_DejaVuSansMono.ttf'); }
'''

if __name__ == "__main__":
  # Get list of notes, thickest string to thinnest
  notes = [(GUITAR_NOTES[s_idx][o_idx], OCTAVE_NOTES[s_idx][o_idx]) \
    for s_idx in range(len(GUITAR_NOTES)-1,-1,-1) for o_idx in range(len(GUITAR_NOTES[s_idx]))]
  
  # Reverse the order of the GUITAR_NOTES list, to print the thickest string at the bottom
  guitar_notes = [GUITAR_NOTES[i] for i in range(len(GUITAR_NOTES)-1, -1, -1)]
  octave_notes = [OCTAVE_NOTES[i] for i in range(len(OCTAVE_NOTES)-1, -1, -1)]

  # Print each note into each fretboard
  notes_fretboard = ['<pre>'+print_guitar_fretboard([(note, octave)], guitar_notes, octave_notes)+'</pre>' for note, octave in notes]

  # Convert notes into chars
  notes_chars = [noteToChar(note)+str(octave) for note, octave in notes]

  # Convert notes to sound
  notes_sound = [convertToSound(notes=[(note, octave)], duration=2000) for note, octave in notes]
  
  convertguitarNotes2Anki(notes_chars, notes_fretboard, notes_sound)
