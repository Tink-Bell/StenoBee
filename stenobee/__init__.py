from plover.system.english_stenotype import *

KEYS = ('^-', 'X-', 'K-', 'P-', 'M-', 'S-', 'H-', 'L-', 'T-', 'J-', 'Q-', 'C-', 'N-', 'R-', 'D-', 'G-', 'F-', 'V-', 'B-', 'Z-', '-O', '-A', '-*', '-E', '-I')

IMPLICIT_HYPHEN_KEYS = ()
SUFFIX_KEYS = ()
NUMBERS = {}
NUMBER_KEY = None
ORTHOGRAPHY_RULES = []
ORTHOGRAPHY_WORDLIST = None
FERAL_NUMBER_KEY = False
ORTHOGRAPHY_RULES_ALIASES = {}
UNDO_STROKE_STENO = "-*"

KEYMAPS = {
 'Keyboard': {
	'^-'         : '6',
	'X-'         : 'x',
	'K-'         : 'k',
	'P-'         : 'p',
	'M-'         : 'm',
	'S-'         : 's',
	'H-'         : 'h',
	'L-'         : 'l',
	'T-'         : 't',
	'J-'         : 'j',
	'Q-'         : 'q',
	'C-'         : 'c',
	'N-'         : 'n',
	'R-'         : 'r',
	'D-'         : 'd',
	'G-'         : 'g',
	'F-'         : 'f',
	'V-'         : 'v',
	'B-'         : 'b',
	'Z-'         : 'z',
	'-O'         : 'o',
	'-A'         : 'a',
	'-*'         : 'u',
	'-E'         : 'e',
	'-I'         : 'i',
        'arpeggiate': 'space',
        # Suppress adjacent keys to prevent miss-strokes.
        'no-op'     : ''
    }
}

DICTIONARIES_ROOT = 'asset:stenobee:assets'

DEFAULT_DICTIONARIES = (
    'StenoBee-Core.json',
    'StenoBee-Common.json',
    'StenoBee-Proper-Nouns.json',
    'StenoBee-Numbers.py',
    'StenoBee-Alt_Ergo_Numbers.json',
    'StenoBee-Symbols&Spelling.json',
    'StenoBee-Modifiers.json',
    'StenoBeeNiche-Pokemon-[KPMN].json',
    'StenoBeeNiche-Emoji-[MJ].json',
    'StenoBeeNiche-Minecraft-[MTCNRF].json',
    'StenoBeeNiche-Mineral-[MLNR].json',
    'StenoBeeNiche-Chemistry-[MSHTCR].json',
    'StenoBeeNiche-Music&Instruments-[MSTCNRD].json',
    'StenoBeeNiche-ModeSetSpace-[PMSTCD].json',
)









