from typing import Any
from control.controlbase import ControlBase
from common import commons
from invalidstateerror import InvalidStateError
import pyautogui
import time
import pyperclip

class TourAll(ControlBase):
    
    con_name = 'TourAll'

    def __init__(self, stop_event):
        super().__init__()
        # self.name='모든 서버 보상 얻기'
        # 모든 제어는 최초 화면 상태를 맞추고 시작해야하므로 최초 화면의 상태를 
        self.start_screen_state = commons.state_dict['타이틀화면']
        self.stop_event = stop_event

    def run(self):             

        # HB서버 리스트 화면까지 왔음
        serverlist = commons.getserverlist('hb')

        time.sleep(3)

        for i, server in enumerate(serverlist, start=48):
            if self.stop_event.is_set():
                return            

            print(f'{server} 를 선택하겠습니다.')
            commons.selectserver(i)
            time.sleep(1)
            touch_texts = ['서버클리', '시즌서버', 'HB']
            for t in touch_texts:
                commons.touch_on_text(t)
                time.sleep(1)
