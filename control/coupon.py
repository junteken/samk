from typing import Any
from control.controlbase import ControlBase
from common import commons
from invalidstateerror import InvalidStateError
import pyautogui
import time
import pyperclip

class Coupon(ControlBase):
    
    con_name = '쿠폰적용하기'

    def __init__(self, stop_event):
        super().__init__(stop_event)
        # self.name='모든 서버 보상 얻기'
        # 모든 제어는 최초 화면 상태를 맞추고 시작해야하므로 최초 화면의 상태를 
        self.start_screen_state = commons.state_dict['타이틀화면']
        self.coupon_list = ['81b8d8ada343484e',
                            '7844b2d651c8e31c',
                            '4aa4913117c956b8',
                            '266f997f6ad53932',
                            '644ff0517177d086']
        self.start_server_name = 'S 109'

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
            print(f'{self.current_server} 서버의 쿠폰 받기가 시작되었습니다.') 
            cur_state = commons.get_current_state()
            self.start2world(cur_state)
            self.world2event(cur_state)

            scroll_start = (231, 667)
            scroll_to = (231, 188)

            for i in range(5):
                commons.scroll(scroll_start, scroll_to)

            time.sleep(3)
            commons.mouseclick((226,648))
            time.sleep(1)

            for cp in self.coupon_list:
                commons.mouseclick((585, 369))
                for i in range(20):
                    pyautogui.press('backspace')
                pyperclip.copy(cp)        
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(2)
                pyautogui.press('r')
                time.sleep(1)

            cur_state = self.gamequit()
            cur_state = commons.get_current_state()
            cur_state = self.Bt_2_Title(cur_state)

            


        






            
            

            
            
