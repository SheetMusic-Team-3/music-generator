import random

clefs = ('treble', 'soprano', 'mezzosoprano', 'alto', 'tenor', 'baritone', 'bass', 'subbass')

notes = ('a', 'b', 'c', 'd', 'e', 'f', 'g')

note_durations = (1, 2, 4, 8, 16, 32)

keys = ('C', 'G', 'D', 'A', 'E', 'B', 'Cb', 'F#', 'Gb', 'Db', 'C#', 'Ab', 'Eb', 'Bb', 'F')

octave_ranges = {
    'treble'       : ('4', '5', '6'),
    'soprano'      : ('3', '4', '5'),
    'mezzosoprano' : ('3', '4', '5'),
    'alto'         : ('3', '4', '5'),
    'tenor'        : ('3', '4', '5'),
    'tenor'        : ('2', '3', '4'),
    'baritone'     : ('2', '3', '4'),
    'bass'         : ('2', '3', '4'),
    'subbass'      : ('2', '3', '4')
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

    # Picks a random time signature; if 4/4 or 2/2, there is a 50-50 chance it will use common/cut time
    time_bar = random.choice(range(1, 11))
    time_beat = random.choice([2, 4, 8, 12])
    time_semantic = str(time_bar) + '/' + str(time_beat)
    time_lp = '\\numericTimeSignature \\time ' + time_semantic
    if time_semantic == '4/4' and random.choice([0, 1]) == 1:
        time_lp = '\\defaultTimeSignature \\time 4/4'
        time_semantic = 'C'
    elif time_semantic == '2/4' and random.choice([0, 1]) == 1:
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
            lilypond_file.write('\\version "2.20.0"\\score{{\n')

            lilypond_file.write('\\clef ' + clef + '\n')
            semantic_file.write('clef-' + clef_to_semantic[clef] + '\n')

            lilypond_file.write('\\key ' + key_lp + ' \\major\n')
            semantic_file.write('keySignature-' + key + '\n')

            lilypond_file.write(time_lp + '\n')
            semantic_file.write('timeSignature-' + time_semantic + '\n')

            # Writes notes by bar; currently, a note cannot span across a barline
            for bar in range(num_bars):
                beats_left = time_bar
                while beats_left >= 0:
                    # TODO
                semantic_file.write('barline\n')



def multi_generate(num_lines, output_name, num_bars):
    """Generates multiple random line of sheet music in LilyPond and semantic notation formats
       Calls generate_line() for each line to generate; each iteration generates 2 files 
       
       num_lines: an integer that dictates how many random lines will be generated
       output_name: a string that the export files will be saved to
       num_bars: an integer that dictates how many bars of music will be generated
    """

    for i in range(num_lines):
        generate_line(output_name + str(i + 1), num_bars)

#generate_line('test', 1)
#multi_generate(4, 'test', 4)