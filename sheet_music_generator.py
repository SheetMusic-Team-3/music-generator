import random


# LILYPOND_VERSION = '2.20.0'
LILYPOND_VERSION = '2.18.2'
LILYPOND_ENDING = '\\layout{}\n\\midi{}'

COMMON_TIME_CHANCE = .50
CUT_TIME_CHANCE = .50
SHARP_CHANCE = .25
FLAT_CHANCE = .25
DOTTED_NOTE_CHANCE = .25
START_SLUR_CHANCE = .10
STOP_SLUR_CHANCE = .50

clefs = ('treble', 'soprano', 'mezzosoprano', 'alto', 'tenor', 'baritone', 'bass', 'subbass')

notes = ('a', 'b', 'c', 'd', 'e', 'f', 'g')

note_durations = (1, 2, 4, 8, 16, 32)
note_durations_semantic = ('whole', 'half', 'quarter', 'eighth', 'sixteenth', 'thirty_second')

keys = ('C', 'G', 'D', 'A', 'E', 'B', 'Cb', 'F#', 'Gb', 'Db', 'C#', 'Ab', 'Eb', 'Bb', 'F')

octave_ranges = {
    'treble'       : (4, 5, 6),
    'soprano'      : (3, 4, 5),
    'mezzosoprano' : (3, 4, 5),
    'alto'         : (3, 4, 5),
    'tenor'        : (3, 4, 5),
    'baritone'     : (3, 4),
    'bass'         : (2, 3, 4),
    'subbass'      : (2, 3, 4)
}

octave_to_lp = {
    1 : ',,',
    2 : ',,',
    3 : '',
    4 : '\'',
    5 : '\'\'',
    6 : '\'\'\''
}

clef_to_semantic = {
    'treble'       : 'G2',
    'soprano'      : 'C1',
    'mezzosoprano' : 'C2',
    'alto'         : 'C3',
    'tenor'        : 'C4',
    'baritone'     : 'C5',
    'bass'         : 'F4',
    'subbass'      : 'F5'
}

def generate_line(output_name, num_bars):
    """Generates a random line of sheet music in LilyPond and semantic notation formats
       
       output_name: a string that the export files will be saved to
       num_bars: an integer that dictates how many bars of music will be generated
    """

    # Picks a random clef
    clef = random.choice(clefs)

    # Picks a random time signature; if 4/4 or 2/2, it might use common or cut time
    value_per_beat = random.choice([2, 4, 8]) # inverse (e.g. 4 is a quarter note)
    beats_per_bar = random.choice(range(2, 11))
    time_semantic = str(beats_per_bar) + '/' + str(value_per_beat)
    time_lp = '\\numericTimeSignature \\time ' + time_semantic
    if time_semantic == '4/4' and random.uniform(0,1) < COMMON_TIME_CHANCE:
        time_lp = '\\defaultTimeSignature \\time 4/4'
        time_semantic = 'C'
    elif time_semantic == '2/4' and random.uniform(0,1) < CUT_TIME_CHANCE:
        time_lp = '\\defaultTimeSignature \\time 2/4'
        time_semantic = 'C/'
        
    # Picks a random key; all keys are written as major
    key = random.choice(keys)
    key_lp = key[0].lower()
    if key[1:] == '#':
        key_lp += 'is'
    elif key[1:] == 'b':
        key_lp += 'es'

    # Opens 2 output files (.ly and .txt)
    with open(output_name + '.ly', 'w') as lilypond_file:
        with open(output_name + '.txt', 'w') as semantic_file:

            # Writes intro material
            lilypond_file.write('\\version "'+ LILYPOND_VERSION + '"\\score{{\n')

            lilypond_file.write('\\clef ' + clef + '\n')
            semantic_file.write('clef-' + clef_to_semantic[clef] + '\n')

            lilypond_file.write('\\key ' + key_lp + ' \\major\n')
            semantic_file.write('keySignature-' + key + '\n')

            lilypond_file.write(time_lp + '\n')
            semantic_file.write('timeSignature-' + time_semantic + '\n')

            # Writes notes by bar; currently, a note cannot span across a barline
            in_slur = False
            for bar in range(num_bars):
                remaining_time = (1 / value_per_beat) * beats_per_bar
                while remaining_time > 0:
                    print('Remaining:', remaining_time)
                    note_lp = ''
                    note_semantic = 'note-'

                    # Determines pitch of note
                    note_pitch = random.choice(notes)
                    octave = random.choice(octave_ranges[clef])

                    # Adjusts note to be sharp or flat
                    accidental_lp = ''
                    accidental_semantic = ''
                    if random.uniform(0,1) < SHARP_CHANCE:
                        accidental_lp = 'is'
                        accidental_semantic = '#'
                    if random.uniform(0,1) < FLAT_CHANCE:
                        accidental_lp = 'es'
                        accidental_semantic = 'b'

                    # Adds pitch to strings
                    note_lp += note_pitch + accidental_lp + octave_to_lp[octave]
                    note_semantic += note_pitch.upper() + accidental_semantic + str(octave)

                    # Determines time value of note
                    note_durations_length = len(note_durations)
                    longest_note_index = 0
                    for i in range(note_durations_length):
                        if 1 / note_durations[i] <= remaining_time:
                            longest_note_index = i
                            break
                        if i == note_durations_length - 1:
                            raise Exception('Not enough space in bar; space remaining: ' + str(remaining_time))
                    note_index = random.choice(range(longest_note_index, note_durations_length))
                    note_duration = 1 / note_durations[note_index]

                    # Adds time value to strings
                    note_lp += str(note_durations[note_index])
                    note_semantic += '_' + str(note_durations_semantic[note_index])

                    # Determines if note is dotted & adds to strings
                    if note_index != note_durations_length - 1 and note_duration * 1.5 <= remaining_time and random.uniform(0,1) < DOTTED_NOTE_CHANCE:
                        note_duration *= 1.5
                        note_lp += '.'
                        note_semantic += '.'

                    # Determines whether to start/continue a slur; will end any slurs on the first note of the final bar
                    if bar == num_bars:
                        if in_slur:
                            in_slur = False
                            note_lp += ')'
                    elif in_slur:
                        if random.uniform(0,1) < STOP_SLUR_CHANCE:
                            in_slur = False
                            note_lp += ')'
                        else:
                            note_semantic += '\ntie'
                    else:
                        if random.uniform(0,1) < START_SLUR_CHANCE:
                            in_slur = True
                            note_lp += '('
                            note_semantic += '\ntie'
                    
                    # Writes strings to files
                    lilypond_file.write(note_lp + ' ')
                    semantic_file.write(note_semantic + '\n')

                    # Adjusts loop variable
                    remaining_time -= note_duration
                
                # Writes barline
                semantic_file.write('barline\n')
            
            # Finishes LilyPond file
            lilypond_file.write('\\bar "|."\n}\n' + LILYPOND_ENDING + '}')



def multi_generate(num_lines, output_name, num_bars):
    """Generates multiple random line of sheet music in LilyPond and semantic notation formats
       Calls generate_line() for each line to generate; each iteration generates 2 files 
       
       num_lines: an integer that dictates how many random lines will be generated
       output_name: a string that the export files will be saved to
       num_bars: an integer that dictates how many bars of music will be generated
    """

    for i in range(num_lines):
        generate_line(output_name + str(i + 1), num_bars)

generate_line('test', 4)
#multi_generate(4, 'test', 4)