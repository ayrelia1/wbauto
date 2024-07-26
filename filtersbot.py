from config import CallbackData, Filter
from function import databasework

class AdminCheck(Filter):
    async def __call__(self, message) -> bool:
        return await databasework.check_admin(message)


class CallbackDataFilter(CallbackData, prefix='get_cab_f'):
    cabinet: str
    action: str
    
class DeleteCabinet(CallbackData, prefix='del_cab_f'):
    cabinet: str
    action: str
    
    
class Templates(CallbackData, prefix='get_temp_f'):
    name: str
    action: str
    
    
class EditTemplate(CallbackData, prefix='ed_temp_f'):
    name_template: str
    have_text: str
    action: str
    
    
    

