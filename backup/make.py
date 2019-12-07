import sys

from dataIO import js

# Bot Utilities
from tools import GetWords

sys.path.append("..")

avlos = GetWords.List.dict_to_json("https://www.sprakradet.no/sprakhjelp/Skriverad/Avloeysarord/")
js.dump(avlos, "avlos.json", overwrite=True, indent_format=True, enable_verbose=False)

forkort = GetWords.List.dict_to_json("https://www.sprakradet.no/sprakhjelp/Skriveregler/Forkortinger/")
js.dump(forkort, "forkort.json", overwrite=True, indent_format=True, enable_verbose=False)
