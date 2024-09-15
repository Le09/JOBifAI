
# Declare characters used by this game.
define s = Character(_("Secretary"), color="#c8ffc8")
define m = Character(_("Me"), color="#c8c8ff")
define b = Character(_("Boss"), color="#ffc8ff")
define g = Character(_("Guard"), color="#ffffaa")
define h = Character(_("Henk"), color="#c8c8")
define j = Character(_("JOBifAI"), color="#ccc8c8")

default persistent.user_id = None
default persistent.game_first_time = True
default persistent.config = {"groq_api_key": persistent.groq_api_key}

default dir_session = None

default portfolio_idea = None
default portfolio_prompt = None
default portfolio_0 = None
default portfolio_0_job = None

default series_idea = None
default series_prompt = None
default series_cover = None
default series_cover_job = None

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

default ad_mood = None
default ad_mood_string = None
default confidence = 0.34
default ad_answer = None

default earring_got = False
default earring_given = False
default secretary_happy = False
