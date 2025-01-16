from .emoji import Emoji
from .memes import Memes
from .siteviewer import SiteViewer


# All models to instantiate on load
__beanie_models__ = [
    Emoji,
    Memes,
    SiteViewer,
]
