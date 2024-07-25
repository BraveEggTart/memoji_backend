from .emojis import Emojis
from .memes import Memes


# All models to instantiate on load
__beanie_models__ = [
    Emojis,
    Memes,
]
