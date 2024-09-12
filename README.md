# JOBifAI (that time I got the job interview at Grizley)

## An AI augmented visual novel.

This is a work of fiction. 
Names, characters, businesses, places, events, locales, and incidents are either the products of the author’s imagination or used in a fictitious manner. Any resemblance to actual persons, living or dead, or actual events is purely coincidental.

## Roadmap

TODO:
- let the user respond first to the interviewer; if confidence is low, make the AD explain that `portfolio_idea` should be explained to fit with `series_idea`
- make the text input scrollable? (or bigger?)
- Add music
- easter eggs: able to find the earring in the couch, give it back to the secretary (or keep it?)
- improve interview experience
- have demo_key for the steam export, which is used if the real keys are not set (or set to demo)
- achievements
- advanced configuration options (url, model) for the LLM
- add PRODIA_DEMO_KEY and LLM_DEMO_KEY to be used as default if no key has been set
- add explanation page for the advanced settings "To simplify things, the AI calls are made using a demo key.
If this key is abused, it will cease working for all players.
In that case you can set up your own keys, for free, in the settings. If you run your own AI, this is also supported! 
"
- add a persistent user id that is passed to the LLM calls

Maybe?
- add more configuration options to be able to use comfyUI instead or Prodia
- distribute the function as ren'py libraries (?)

## Bulding the game

Final build script, once demo keys have been set:

```bash
source .keys.rc
sed -i "s/PRODIA_DEMO_KEY/$prodia_api_key/" game/scripts/init_python.rpy
sed -i "s/LLM_DEMO_KEY/$llm_api_key/" game/scripts/init_python.rpy
dir_tmp=$(mktemp -d "tmp/dirXXXX")
mkdir -p $dir_tmp
mv game/images/session* $dir_tmp
./renpy.sh launcher distribute JOBifAI
mv $dir_tmp/* game/images/
```

Otherwise, all these images will get packaged with it.
