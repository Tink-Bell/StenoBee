from plover.system.english_stenotype import *

KEYS = (';-', 'K-', 'X-', 'C-', 'F-', 'D-', 'S-', 'H-', 'Q-', 'T-', 'P-', 'B-', 'J-', 'N-', 'G-', 'R-', '$-', 'L-', 'Z-', 'M-', 'V-', '-A', '-E', '-I', '-O')

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
	'X-'         : 'x',
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
	'Z-'         : 'z',
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
