
# Declare characters used by this game.
define s = Character(_("Secretary"), color="#c8ffc8", callback=make_voice("anh"))
define m = Character(_("Me"), color="#c8c8ff", callback=make_voice("an"))
define b = Character(_("Boss"), color="#ffc8ff", callback=make_voice("normal"))
define g = Character(_("Guard"), color="#ffffaa", callback=make_voice("normal"))
define h = Character(_("Henk"), color="#c8c8", callback=make_voice("normal"))
define j = Character(_("JOBifAI"), color="#ccc8c8", callback=make_voice("anh"))
define r = Character(_("Random Man"), color="#99c888", callback=make_voice("normal"))
define bb = Character(_("Boss"), color="#ffc8ff", what_style="say_transcript", callback=make_voice("normal"))
define mm = Character(_("Me"), color="#c8c8ff", what_style="say_transcript", callback=make_voice("an"))

default persistent.touch = "dynamic"
default persistent.user_id = None
default persistent.game_first_time = True

default persistent.ticket = None
default persistent.steam_id = None

default dir_session = None

default portfolio_idea = None
default portfolio_prompt = None
default portfolio_0 = None

default series_idea = None
default series_prompt = None
default series_cover = None

default prompt = None
default schema = None
default result = None
default im_portfolio_0 = None
default im_series_cover = None
default answer = None
default choice = None
default jump_state = None
default count_first_move = 0
default count_ask_interview = 0
default count_secretary_angry_boss = 0
default count_warning = 0
default count_boss_presentation = 0
default count_waiting_time = 0

default ad_mood = None
default ad_mood_string = None
default confidence = 0.34
default ad_answer = None

default earring_got = False
default earring_given = False
default secretary_happy = False
