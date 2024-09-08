# Part 1: The game begins here.
label start:

    if persistent.game_first_time:
        call screen config_menu
        $ persistent.game_first_time = False

    scene bg room
    with fade


    m "Gin...ious... I'm a gin...ious..."
    show henk
    with dissolve
    h "Ahem... If you're so... rhum...markeable... Hohoho... Why aren't you working for Grizley?"
    m "Grizley... When I apply, I'll be there in no time. Watch me!"
    h "Watching... With my Eyes... Wide...  OZzzzZZZzzzzz"
    hide henk
    with dissolve
    m "Henk, you never handled alcohol too well."

    scene bg cyber

    m "JOBifAI, how do I become concept designer for Grizley?"

    show j intro
    with dissolve

    j "Complete these 4 steps to become concept designer for Grizley:"
    j "Step 1: Send this CV I made for you. It says you have a degree in Industrial Design from RISD."


    j "Add the link of your SinkedIN page I just made. I connected you to some notable concept designers."
    m "What is RISD? And who are these SinkedIN \'friends\' you connected me to? Their faces are weird."
    j "Step 2: Attach this portfolio I am generating for you, with the following description:"

    show j cv

    j "I grew up in Videville, a small town known for its vertical lake..."
    j "At 10, while helping my grandfather build the town's cycle superhighway, a cyclist stopped by." 
    j "It was no other than Syd Meat. Listening to his encouraging words, my vocation became clear."
    m "You know what, if I don't apply, I have a 100\% chance of being rejected. So I'll apply."
    j " Step 3: Read this 587 page document detailing the work environment at Grizley."
    j "With these three steps, you're guaranteed to get hired!"
    j "Remember, this version of JOBifAI is experimental. It is not advised to use it in a real-life setting."
    m "Awesome. Now I just need to submit the CV and portfolio, and hope for the best. Let's wait a bit..."

    jump init_series
