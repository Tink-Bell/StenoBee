from plover.system.english_stenotype import *

KEYS = (';-', 'V-', 'Q-', 'C-', 'F-', 'H-', 'S-', 'D-', 'J-', 'T-', 'P-', 'B-', 'X-', 'N-', '$-', 'L-', 'G-', 'R-', 'Z-', 'M-', 'K-', '-A', '-E', '-I', '-O')

IMPLICIT_HYPHEN_KEYS = ()
SUFFIX_KEYS = ()
NUMBERS = {}
NUMBER_KEY = None
ORTHOGRAPHY_RULES = []
ORTHOGRAPHY_WORDLIST = None
FERAL_NUMBER_KEY = False
ORTHOGRAPHY_RULES_ALIASES = {}
UNDO_STROKE_STENO = ";-"

KEYMAPS = {
 'Keyboard': {
        ';-'         : 'u',
        'V-'         : 'v',
        'Q-'         : 'q',
        'C-'         : 'c',
        'F-'         : 'f',
        'H-'         : 'h',
	'S-'         : 's',
        'D-'         : 'd',
	'J-'         : 'j',
	'T-'         : 't',
	'P-'         : 'p',
	'B-'         : 'b',
	'X-'         : 'x',
	'N-'         : 'n',
	'$-'         : '4',
	'L-'         : 'l',
	'G-'         : 'g',
	'R-'         : 'r',
	'Z-'         : 'z',
	'M-'         : 'm',
	'K-'         : 'k',
	'-A'         : 'a',
	'-E'         : 'e',
	'-I'         : 'i',
	'-O'         : 'o',
        'arpeggiate': 'space',
        # Suppress adjacent keys to prevent miss-strokes.
        'no-op'     : ''
    }
}
