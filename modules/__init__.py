# from modules.mygames.handlers import router as game_router
from modules.main.handlers import router as main_router
from modules.newgame.handlers import router as newgame_router
from modules.profile.handlers import router as profile_router
from modules.support.handlers import router as support_router

ALL_ROUTERS = [
    main_router,
    # game_router,
    newgame_router,
    profile_router,
    support_router
]