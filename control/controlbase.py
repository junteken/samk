from typing import Any
from common import commons
from invalidstateerror import InvalidStateError
import threading

class ControlBase(threading.Thread):
    def __init__(self):
        # name은 gui의 list view의 item이름으로 사용된다.
        super().__init__()        
        self.name = None
        self.start_screen_state = None
        
    def check(self):
        # 현재 게임화면 상태가 start_screen_state와 동일한지 확인하기        
        # if self.start_screen_state.check(commons.get_current_text()):
        if self.start_screen_state.name == commons.get_current_state().name :
            return True
        else:
            raise InvalidStateError(self.state, self.start_screen_state)




    

