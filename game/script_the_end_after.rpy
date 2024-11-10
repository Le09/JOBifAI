# After the end.

label band_starts:
    # play music "meow-lilac.mp3"
    play music "meow-bassguitar.mp3" noloop

    scene bg street
    hide henk
    with dissolve
    show meow
    with dissolve
    show flora
    with dissolve

    h "Hey, these people are blocking the road."
    h "What do they think, playing music in the street? Can't they be normal NEETs?"
    h "They even put a hat for donations... as if we have any money."
    h "There's no way around them... what do we do?"

    stop music fadeout 1.0
    $ reply = renpy.input(["","Describe what you do."], screen="viewport_llm")
    $ reply = reply.strip() or "Walk away."
    $ mm.add_history(kind="adv", who=narrator.name, what=reply)
    $ prompt = """
    Context: the main character is in the street, where some musicians are setting up their gear to play.
    They have put down a hat for donations.
    Here are the possible actions:
    1) give coins to the musicians
    2) leave the scene

    Here is a description of what the character did:

    %s

    Evaluate what the answer may be among the previous options as a choice c.
    Be strict on the fact that for option **1**, the answer must take decisive action to get this result, or show a strong interest to listen to the music; if the main character does not, the result should be **2**.
    Moreover, describe what happens as a result of this action as a sentence s.
    Describe only the direct result of the action.
    Give your answer as a json of the form {"choice": c, "result": s}.
    """ % reply

    $ schema = {"choice": "integer:1<=i<=2", "result":  "string"}
    $ answer = askllm("lobby_first", prompt, schema)
    $ choice = answer["choice"]
    $ result = answer["result"]
    $ jump_state = ["band_plays", "band_escape"][choice - 1]

    $ renpy.say(narrator, result, what_style="say_transcript")
    $ renpy.jump(jump_state)


label band_plays:
    play music "meow-gardenia.mp3"
    m "I got a few coins that I... found in the lobby's couch, I guess."
    h "You guess?"
    m "Right? So anyway, let's listen to them. They look like they need some support."


    $ achievement_flora.grant()

    "{b}Stop the song and return to main screen?{/b}"

    $ save_transcript("band_plays")
    return

label band_escape:
    hide flora
    hide meow
    show henk
    h "Look, they moved their amplifier, let's run for it!"

    $ save_transcript("band_escape")
    return
