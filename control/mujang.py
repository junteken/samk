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
        self.target_server_name = '권토중래'
        self.mujang_order = ['축융부인', '육손']

    def run(self):
        # HB서버 리스트 화면까지 왔음
        self.serverlist = commons.getserverlist('hb')
        start = self.serverlist[self.target_server_name]

        for idx, sv in enumerate(self.serverlist):                       
            if self.stop_event.is_set():
                return                        
            if self.stop_event.is_set():
                return            
            if idx < start:
                continue
            self.current_server = sv

            print(f'{self.current_server} 서버의 무장셋팅 시작합니다.')            

            self.server_start(idx)
            cur_state = commons.get_current_state()
            cur_state = self.start2world(cur_state)

            # 일단 무장모집부터시작
            if cur_state.name == '세상':
                cur_state = self.high_gacha(cur_state)

            while cur_state.name != '세상':
                pyautogui.press('esc')
                time.sleep(1)
                pyautogui.press('space')
                time.sleep(1)

            cur_state = self.world2chulmujang(cur_state)
            if not self.mujang_chuljin(cur_state):
                print(f'{self.current_server} 출전무장 실패')

            if not self.levelup(cur_state):
                print(f'{self.current_server} 렙업 실패')

            
            # 항상 게임재시작해줘야함
            self.restart_game()

    def levelup(self, cur_state):
        if cur_state.name != '출전무장':
            print(f'레벨업 할수 없음, 원인 = {cur_state}')
            return False
        
        # 30 pixel씩 아래로 내려가면된다.
        coord = [(385, 267), (835, 267)]

        for i in range(8):
            x = coord[i%2][0]
            y = coord[i%2][1] - i*30
            commons.mouseclick((x, y))
            time.sleep(1)
            # 즉시레벨업
            pyautogui.press('e')
            time.sleep(1)

            # # 진급
            pyautogui.press('d')
            time.sleep(1)
            pyautogui.press('w')
            time.sleep(1)

            cur_state = commons.get_current_state()
            while cur_state.name == '진급성공':
                pyautogui.press('esc')
                time.sleep(1)
                pyautogui.press('w')
                time.sleep(1)
                cur_state = commons.get_current_state()

            while cur_state.name != '출전무장':
                pyautogui.press('esc')
                time.sleep(1)
                cur_state = commons.get_current_state()
                  
            pyautogui.press('esc')
            time.sleep(1)

        return True
            
        
    
    def mujang_chuljin(self, cur_state):        
        if cur_state.name != '출전무장':
            print(f'무장을 출전할수 없음, 원인 = {cur_state}')
            return False
        chuljin_list = commons.search_all_similar_texts_on_cur_screen('출진기능')

        if len(chuljin_list) == 0:
            print('빈슬롯이 없습니다.')
            return True

        for chuljin in chuljin_list:
            commons.mouseclick((chuljin[0][0][0], chuljin[0][0][1]))
            time.sleep(2)
            # 이부분을 원하는 무장으로 선택하게 변경하면된다.
            commons.mouseclick((351, 232))
            time.sleep(2)

        print('출전무장 완료')
        return True
        

            



    
        
        
