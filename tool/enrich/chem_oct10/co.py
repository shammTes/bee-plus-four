"""Card helpers: chem_models' Unit with "-co-" ids (so this tool owns and re-creates only its own cards)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'chem_models'))
from common import Unit as _Unit  # noqa: E402
from chemtex import ce, eq, ie  # noqa: E402,F401


class Unit(_Unit):
    def id(self, i):
        return f'{self.U}-co-{i}'
