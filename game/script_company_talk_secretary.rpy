# Part 3: talking with Grizley secretary.
label talk_secretary:
    stop music fadeout 1.0
    scene bg desk
    show secretary at truecenter

    $ reply = renpy.input(["Secretary","Is there any way I can help?"], screen="viewport_llm")
    $ reply = reply.strip() or "babble incoherently"
    $ narrator.add_history(kind="adv", who=narrator.name, what=reply)

    while count_ask_interview < 3:
        $ earring_can_give = earring_got and not earring_given
        $ earring_choice = "6) talk about the earring" if earring_can_give else ""
        $ earring_instruction = "- Choose **6** if the character mentions the earrings in any way" if earring_can_give else ""
        $ count_ask_interview+= 1
        $ prompt = """
        Context: The main character is in front of the secretary, a woman, of Grizley, an entertainment company.
Here are the possible actions:
1) Say nothing or a confusing blurb
2) Explicitly mention being there for a job interview (at 10 am), with the art director
3) Leave the building
4) Act in a very suspicious or rude manner
5) Something else (if the character does anything else that doesn’t fit into 1, 2, 3, or 4)
%s

Here is a description of what the character did:

%s

Based on the description, follow these strict rules to determine the outcome:
- Choose **5** if the character doesn't mention the interview, says nothing, provides a confusing response, or acts shy/awkward.
- Choose **2** only if the character clearly references the job interview with specific details (time and art director).
- Choose **1** for complete silence or vague, meaningless statements.
- Choose **4** if the character’s behavior is rude, suspicious, or highly inappropriate.
- Choose **3** only if the character leaves the building explicitly.
%s

Moreover, describe what happens as a result of this action. Focus strictly on the direct result of the action without assumptions about future events.
Return the result in JSON format as follows:  {"choice": c, "result": s}
        """ % (earring_choice, reply, earring_instruction)

        $ schema = {"choice":  "integer:1<=i<=6" if earring_can_give else "integer:1<=i<=5", "result":  "string"}

        $ answer = askllm("talk_secretary", prompt, schema)
        $ choice = answer["choice"]
        $ result = answer["result"]
        $ jump_state = ["secretary_nervous", "ready_interview", "bad_ending", "security", "secretary_nervous", "earring_give"][choice - 1]

        if choice == 6:  # this way we skip the reply that may not make sense with our dialogue
            jump earring_give
        $ renpy.say(narrator, result)
        $ renpy.jump(jump_state)

    jump secretary_angry_boss

label secretary_nervous:

    "It's a stressful situation... Maybe next time tell her about the interview."

    jump talk_secretary

label earring_give:
    "I found this earring between the couch's cushions."
    s "Oh, thank you! I was looking for it everywhere."
    s "It's an earring with the logo of my favourite band, OKF."
    "Maybe her smile was worth this earring weight in gold."
    $ achievement_earring_given.grant()
    $ earring_given = True
    $ secretary_happy = True

    jump talk_secretary

label ready_interview:
    s "The art director's office is this way."
    if secretary_happy:
        jump boss_happy

    jump boss_neutral
