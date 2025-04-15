from .game import MESSAGES_GAME
from .roles import MESSAGES_ROLES
from .night import MESSAGES_NIGHT

MESSAGES = {
    **MESSAGES_GAME,
    **MESSAGES_ROLES,
    **MESSAGES_NIGHT,
}