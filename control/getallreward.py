from typing import Any
from control.controlbase import ControlBase
from common import commons
from invalidstateerror import InvalidStateError
import pyautogui
import time

class GetAllReward(ControlBase):

    def __init__(self):
        self.name='모든 서버 보상 얻기'
        # 모든 제어는 최초 화면 상태를 맞추고 시작해야하므로 최초 화면의 상태를 
        self.start_screen_state = commons.state_dict['공지']

    def execute(self, bsm):
        chk_state = super().execute(bsm)

        if chk_state is False:
            print('자동화를 시작하기위한 초기 상태가 아닙니다.')
            raise InvalidStateError("자동화를 시작하기위한 초기 상태가 아닙니다.")
        
        # 공지화면에서는 w키를 눌러야 title화면으로 이동한다.
        for i in range(3):
            pyautogui.press('w', interval= 1)

        time.sleep(1)

        


