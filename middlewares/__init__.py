from config import *

from .check_ban import BannedMiddleware

def setup(dp: Dispatcher):


    banned_middleware = BannedMiddleware()
    dp.message.outer_middleware.register(banned_middleware)
    dp.callback_query.outer_middleware.register(banned_middleware)
    
    