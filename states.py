from config import State, StatesGroup


class add_cabinet_state(StatesGroup):
    one = State()
    two = State()
    three = State()
    four = State()
    five = State()
    
    
class add_template_state(StatesGroup):
    one = State()
    two = State()
    three = State()
    four = State()
    five = State()
    six = State()
    seven = State()
    
class edit_time_pars_state(StatesGroup):
    one = State()
    
class load_reviews_state(StatesGroup):
    one = State()
    
class duplicate_template_state(StatesGroup):
    one = State()
    two = State()
    
    
class edit_template_state(StatesGroup):
    one = State()
    two = State()
    three = State()
    four = State()
    
class give_admin(StatesGroup):
    one = State()