from typing import Any
from common import commons

class ControlBase(object):
    def __init__(self):
        self.name = None
        self.start_screen_state = None
        
    def execute(self, bsm):
        # 현재 게임화면 상태가 start_screen_state와 동일한지 확인하기
        bbox, img = bsm.get_CurrentBsImg()
        if self.start_screen_state.check(img):
            return True
        else:
            return False




    

