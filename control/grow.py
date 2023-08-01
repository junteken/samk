from typing import Any
from control.controlbase import ControlBase
from common import commons
from invalidstateerror import InvalidStateError
import pyautogui
import time
import pyperclip

class Grow(ControlBase):
    
    con_name = '일일미션'

    def __init__(self, stop_event):
        super().__init__(stop_event)        
        # grow는 기본적으로 국가선택, 네이밍까지 완료된 상태의 서버만 실행
        self.start_screen_state = commons.state_dict['타이틀화면']
        self.target_server_name = '입춘대길'

    def run(self):
        # 처음에는 해당 state가 맞는지 검사해야함        
        chk_state = self.check()
        if chk_state is False:
            print(f'{Grow.con_name} 자동화를 시작하기위한 초기 상태가 아닙니다.')
            return
        
        print('초기상태 일치 확인완료')
        # 탐색할 서버의 txt파일이름을 아래에 넣어준다.
        self.serverlist = commons.getserverlist('hb')
        start = self.serverlist[self.start_server_name]

        for idx, sv in enumerate(self.serverlist):
            if self.stop_event.is_set():
                return            
            if idx < start:
                continue
            self.current_server = sv
            # 초기상태는 타이틀화면 이다.                        
            self.server_start(idx)
            #시작버튼을 누르면 여러가지 화면으로 바뀐다.
            cur_state = commons.get_current_state()
            self.start2world(cur_state)
    
        
        
