from typing import Any
from common import commons
from invalidstateerror import InvalidStateError
import threading

class ControlBase(threading.Thread):

    # con_name은 gui의 list view의 item이름으로 사용된다.
    con_name = None
    def __init__(self, stop_event):
        threading.Thread.__init__(self)
        self.start_screen_state = None
        # self.stop_event = threading.Event()
        self.stop_event = stop_event
        
    def check(self):
        # 현재 게임화면 상태가 start_screen_state와 동일한지 확인하기        
        # if self.start_screen_state.check(commons.get_current_text()):
        cur_state = commons.get_current_state()
        if self.start_screen_state.name == cur_state.name :
            return True
        else:
            raise InvalidStateError(cur_state, self.start_screen_state)




    

