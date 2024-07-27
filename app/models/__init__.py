from .emojis import Emojis
from .memes import Memes
from .words import Words
from .bqb import BQB


# All models to instantiate on load
__beanie_models__ = [
    Emojis,
    Memes,
    Words,
    BQB,
]
