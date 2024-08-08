from .population     import get_population, get_meta_url
from .infrastructure import get_amenity_official, get_amenity
from .connectivity   import get_tile_url
from .nat_disasters  import get_desinventar, get_emdat, get_desastres
#from .ecosystems     import 

__all__ = [
    'get_meta_url',
    'get_population',
    'get_amenity_official',
    'get_amenity',
    'get_tile_url',
    'get_desinventar',
    'get_emdat',
    'get_desastres'
]
            