from typing import Any
from control.controlbase import ControlBase
from common import commons
from invalidstateerror import InvalidStateError
import pyautogui
import time
import pyperclip

class Mujang(ControlBase):
    
    con_name = '무장배치'

    def __init__(self, stop_event):
        super().__init__(stop_event)        
        # grow는 기본적으로 국가선택, 네이밍까지 완료된 상태의 서버만 실행
        self.start_screen_state = commons.state_dict['타이틀화면']
        self.target_server_name = '입춘대길'

    def run(self):
        # HB서버 리스트 화면까지 왔음
        self.serverlist = commons.getserverlist('hb')
        start = self.serverlist[self.start_server_name]

        for idx, sv in enumerate(self.serverlist):                       
            if self.stop_event.is_set():
                return                        
            if self.stop_event.is_set():
                return            
            if idx < start:
                continue
            self.current_server = sv

            self.server_start(idx)
            cur_state = commons.get_current_state()
            cur_state = self.start2world(cur_state)
            
            cur_state = self.world2chulmujang(cur_state)






            # 항상 게임재시작해줘야함
            self.restart_game()

    
        
        
