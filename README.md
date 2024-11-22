# JOBifAI (that time I got the job interview at Grizley)

This is an experimental Visual Novel that uses AI to generate images and text.
The gameplay is something that could not exist without AI; you have to bullshit your way to win, and you need to do so based on the AI-generated images.

Each playthrough is unique thanks to these features, and the game is designed to be replayed multiple times.

You can play the game for free on [Steam](https://store.steampowered.com/app/3248650/JOBifAI/)!
You can also get a build directly on [itch.io](https://woolion.itch.io/jobifai).

[![Video trailer](https://img.youtube.com/vi/j1NsyamimcQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=j1NsyamimcQ)

## An AI augmented visual novel.

This is a work of fiction. 
Names, characters, businesses, places, events, locales, and incidents are either the products of the author’s imagination or used in a fictitious manner. Any resemblance to actual persons, living or dead, or actual events is purely coincidental.

## Roadmap

Version 1.0 is done :-)

Maybe?
- add more configuration options to be able to use comfyUI instead or Prodia
- distribute the function as ren'py libraries (?)

## Building the game

The makefile assumes that the Ren'Py SDK has been downloaded in the same folder as the parent directory of this file. If it is not, you can change the `RENPY` variable at the top of  the makefile to point to the correct location. Then you can build the game by running:

```bash
make
```

The makefile also ensure that the session images that are created in the `game/images/session*` folder are moved to a temporary directory before building the game.
Otherwise, the images would be included in the build, bloating it for no reason.
Images are moved back after the build is done, since otherwise that would break the corresponding save files.

## Transcripts

The interactive lines start with a "_   ", non-interactive lines with "    ".
To generate the transcripts, you can define the following command:

```bash
function transcript {
    grep '^_' $1 > "${1%.*}_strip.${1##*.}"
}
```
Which then only keeps the interactive lines.

## Credits

### Development tools
The game engine is [Ren'Py](https://www.renpy.org/).

Images are generated by SDXL using [Prodia](https://prodia.com/). 
It works super well, his very easy, and has a very generous free tier.

The LLM is provided by [Groq](https://groq.com/), which also has a generous free tier.
The calls are made using the standard REST OpeanAI API, so any other compatible service works, including local AI with [Ollama](https://github.com/ollama/ollama). 
You just need to go into advanced settings and change the URL and model.

The achievement system is [Ren'Py Achievements](https://github.com/shawna-p/RenPy-Achievements/).
The history has been pulled into this repository for ease of use.

The screen history has been copied from [tofurocks](https://tofurocks.itch.io/renpy-history).

Fonts are [Pixellari](https://www.dafont.com/pixellari.font) by Zacchary Dempsey-Plante, [VCR OSD Neue](https://www.dafont.com/vcrosdneue.font) by Elli Sho and [OpenDyslexic](https://opendyslexic.org/).

The TTS system is [Renpy Animalese](https://github.com/abrookst/Renpy8-Animalese), with a sound font from [DigiDuncan](https://github.com/DigiDuncan/animalese.py). It is based on [henryishuman' implementation](https://github.com/ztc0611/Ren-py-Animalese), published on a "Feel free to use and modify at your own discretion" license.

### Development team

Program, script: Woolion & Flora Lin.

Graphical assets, original idea: Woolion

Sound design: Flora Lin

Music is:
- Mr. Meowsickles, half of [Arbor Atlantic](https://arboratlantic.bandcamp.com)
- [George Alexander](https://georgealexander.bandcamp.com/)
- Mr. Meowsickles & Flora Lin, as [Recreational Noise](https://recreationalnoise.bandcamp.com/)
- [Cosmoose](https://cosmoose.bandcamp.com/)
- [Pixabay](https://pixabay.com/) (public domain)

We are very grateful to Mélanie for her help debugging non-free platforms and finding quite a number of bugs that inexplicably had found their way into the game. 
Other playtesters include the musicians above, who we can't thank enough for their support, as well as E. 

## License

The achievement system is licensed under the MIT license.
The game assets are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/) License.
The game code is licensed under the [GPL v3 license](https://www.gnu.org/licenses/gpl-3.0.html).
The music is under copyright of the respective artists.
