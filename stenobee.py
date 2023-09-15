from plover.system.english_stenotype import *

KEYS = (';-', 'K-', 'Z-', 'C-', 'F-', 'D-', 'S-', 'H-', 'Q-', 'T-', 'P-', 'B-', 'J-', 'N-', 'G-', 'R-', '$-', 'L-', 'X-', 'M-', 'V-', '-A', '-E', '-I', '-O')

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
	'K-'         : 'k',
	'Z-'         : 'z',
	'C-'         : 'c',
	'F-'         : 'f',
	'D-'         : 'd',
	'S-'         : 's',
	'H-'         : 'h',
	'Q-'         : 'q',
	'T-'         : 't',
	'P-'         : 'p',
	'B-'         : 'b',
	'J-'         : 'j',
	'N-'         : 'n',
	'G-'         : 'g',
	'R-'         : 'r',
	'$-'         : '4',
	'L-'         : 'l',
	'X-'         : 'x',
	'M-'         : 'm',
	'V-'         : 'v',
	'-A'         : 'a',
	'-E'         : 'e',
	'-I'         : 'i',
	'-O'         : 'o',
        'arpeggiate': 'space',
        # Suppress adjacent keys to prevent miss-strokes.
        'no-op'     : ''
    }
}
