from .emojis import Emojis
from .memes import Memes
from .words import Words
from .bqb import BQB
from .siteviewer import SiteViewer


# All models to instantiate on load
__beanie_models__ = [
    Emojis,
    Memes,
    Words,
    BQB,
    SiteViewer,
]
