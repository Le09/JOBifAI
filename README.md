# JOBifAI (that time I got the job interview at Grizley)

## An AI augmented visual novel.

This is a work of fiction. 
Names, characters, businesses, places, events, locales, and incidents are either the products of the author’s imagination or used in a fictitious manner. Any resemblance to actual persons, living or dead, or actual events is purely coincidental.

## Roadmap

TODO:
- add black border behind navigation
- improve scrollable screen
- Add music and sfx (band scene)
- with music changes, in the loop, change the AD sprite depending on confidence (angry: <=.33, happy >=.66, neutral in between)
- advanced configuration options (url, model) for the LLM
- improve title screen
- add explanation page for the advanced settings "To simplify things, the AI calls are made using a demo key.
  If this key is abused, it will cease working for all players.
In that case you can set up your own keys, for free, in the settings. If you run your own AI, this is also supported!"

Maybe?
- add more configuration options to be able to use comfyUI instead or Prodia
- distribute the function as ren'py libraries (?)

## Building the game

The game use "demo keys" variable to make builds directly usable without the need to create new accounts or keys.
To make this work, the build script replaces the demo keys placeholders by the actual values in the file `.keys.rc`, expecting to give a value to `groq_api_key` and `prodia_api_key`.
The build script reverts this change after the build is done.

To avoid the risk of committing the keys, the `.keys.rc` file is ignored by git, and you should install the commit hook to ensure that the project is not commited while the keys have been changed.

To set up the Git hooks in your local environment, run the following command after cloning the repository:

```bash
./setup-hooks.sh
```
This will ensure that if you use

The makefile assumes that the Ren'Py SDK has been downloaded in the same folder as the parent directory of this file. If it is not, you can change the `RENPY` variable at the top of  the makefile to point to the correct location. Then you can build the game by running:

```bash
make
```

If you want to build the game without bundling it with demo keys, you can simply run:

```bash
make no_demo
```

If you intend to distribute the game, make sure to update the disclaimer.

The makefile also ensure that the session images that are created in the `game/images/session*` folder are moved to a temporary directory before building the game.
Otherwise, the images would be included in the build, which bloating it for no reason.
Images are moved back after the build is done, since otherwise that would break the corresponding save files.

## Credits

- [Ren'Py](https://www.renpy.org/)
- [Prodia](https://prodia.ai/)
- [Groq](https://groq.com/)

### Achievement system [Ren'Py Achievements](https://github.com/shawna-p/RenPy-Achievements/)

The history has been pulled into this repository for ease of use.
