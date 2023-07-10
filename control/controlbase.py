from typing import Any
from common import commons
from invalidstateerror import InvalidStateError
import time

class ControlBase(object):
    def __init__(self):
        # name은 gui의 list view의 item이름으로 사용된다.
        self.name = None
        self.start_screen_state = None
        
    def execute(self, bsm):
        # 현재 게임화면 상태가 start_screen_state와 동일한지 확인하기
        bbox, img = bsm.get_CurrentBsImg()
        if self.start_screen_state.check(img):
            return True
        else:
            raise InvalidStateError(self.state, self.start_screen_state)




    

