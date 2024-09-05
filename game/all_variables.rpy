
# Declare characters used by this game.
define s = Character(_("Secretary"), color="#c8ffc8")
define m = Character(_("Me"), color="#c8c8ff")
define b = Character(_("Boss"), color="#ffc8ff")
define g = Character(_("Guard"), color="#ffffaa")
define f = Character(_("Friend"), color="#c8c8")
define j = Character(_("JOBifAI"), color="#ccc8c8")

default persistent.game_first_time = True
default persistent.config = {"groq_api_key": persistent.groq_api_key}

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
default answer = None
default choice = None
default jump_state = None
