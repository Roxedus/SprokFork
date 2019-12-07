import sys
sys.path.append("..")
from tools import GetWords
from dataIO import js

avlos = GetWords.List.dict_to_json("https://www.sprakradet.no/sprakhjelp/Skriverad/Avloeysarord/")
js.dump(avlos, "avlos.json", overwrite=True, indent_format=True, enable_verbose=False)

forkort = GetWords.List.dict_to_json("https://www.sprakradet.no/sprakhjelp/Skriveregler/Forkortinger/")
js.dump(forkort, "forkort.json", overwrite=True, indent_format=True, enable_verbose=False)
