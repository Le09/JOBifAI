# Final part.

label ok_ending:
    scene bg street
    show henk
    with dissolve

    h "Hey!!!! How did it go?"

    m "It went pretty well! They said they would call me back."
    m "Though I'm afraid the number on my AI-generated CV is not accurate at all..."
    h "Send them an email saying you just changed your number. It will be fine."
    m "Definitely. It's a shame AIs can't be trusted yet."

    "{b} OK Ending {/b}"

    return

label worst_ending:
    scene bg street
    show henk
    with dissolve
    h "Hey!!!! How did it go?"

    m "They... they are not ready to hire, apparently."
    h "They really don't know what they're missing. Let's go, you'll find a better job."
    m "A better job than Grizley?"
    h "Yeah I know. Was looking for something nice to say... Wanna try to beat me at Dario Dart?"
    m "Definitely. I probably won't find a job for the next 5 years anyways."

    "{b}Worst Ending{/b}"
    
    return

label bad_ending:
    scene bg street
    "\'You'll never know if you don't even try.\' - Orson Vanderbear, co-founder of Grizley Inc."
    "\'Next time, try harder and stay chill.\' - Henk Lamarre, shareholder of Red Gull GmbH"
    "{b}Bad Ending{/b}"

    return

label ending:
    scene bg street
    m "Hello? Henk, can you hear me? I got the job!!!! They loved my portfolio and said my CV was impressive!!!"
    h "I knew it!!! You're always the best at making up stories."
    m "Thank you for believing in me! See you at 2!"
    "They gave me a brochure to read before I start..."
    "\'There is no such thing as too much hard work, no matter what people say.\' - Orson Vanderbear, co-founder of Grizley Inc."
    "Nice. I can't wait."
    "{b}Good Ending{/b}."

    return