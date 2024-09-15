# JOBifAI (that time I got the job interview at Grizley)

## An AI augmented visual novel.

This is a work of fiction. 
Names, characters, businesses, places, events, locales, and incidents are either the products of the author’s imagination or used in a fictitious manner. Any resemblance to actual persons, living or dead, or actual events is purely coincidental.

## Roadmap

TODO:
- add black border behind navigation
- worst ending: band blocking the path, what do you do? they put a hat waiting for tip (give or leave). If give they sing (play song)
- make the text input scrollable? (or bigger?)
- Add music
- achievements
- advanced configuration options (url, model) for the LLM
- add explanation page for the advanced settings "To simplify things, the AI calls are made using a demo key.
If this key is abused, it will cease working for all players.
In that case you can set up your own keys, for free, in the settings. If you run your own AI, this is also supported!"

Maybe?
- add more configuration options to be able to use comfyUI instead or Prodia
- distribute the function as ren'py libraries (?)

## Building the game

Final build script, once demo keys have been set:

```bash
source .keys.rc
sed -i "s/PRODIA_DEMO_KEY/$prodia_api_key/" game/config.rpy
sed -i "s/LLM_DEMO_KEY/$groq_api_key/" game/config.rpy
dir_tmp=$(mktemp -d "tmp/dirXXXX")
mkdir -p $dir_tmp
mv game/images/session* $dir_tmp
./renpy.sh launcher distribute JOBifAI
mv $dir_tmp/* game/images/
```

Otherwise, all these images will get packaged with it.
