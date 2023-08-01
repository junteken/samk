from typing import Any
from common import commons
from invalidstateerror import InvalidStateError
import threading
import pyautogui
import time
import pyperclip

def check_state_none(func):    
    def wrapper(*args, **kwargs):
        if args[0] is None:
            print(f'{args[0]} 가 None상태입니다.')
            return 
        result = func(*args, **kwargs)
        return result
    return wrapper

class ControlBase(threading.Thread):

    # con_name은 gui의 list view의 item이름으로 사용된다.
    con_name = None
    def __init__(self, stop_event):
        threading.Thread.__init__(self)
        self.start_screen_state = None
        # self.stop_event = threading.Event()
        self.stop_event = stop_event
        self.serverlist = None
        self.current_server = None
        self.current_server_coord = None        
        
    def check(self):
        # 현재 게임화면 상태가 start_screen_state와 동일한지 확인하기        
        # if self.start_screen_state.check(commons.get_current_text()):
        cur_state = commons.get_current_state()
        if self.start_screen_state.name == cur_state.name :
            return True
        else:
            raise InvalidStateError(cur_state, self.start_screen_state)
        

    # Bluestack엔진 시작후 게임실행직전 상태에서 Title까지상태전이
    @check_state_none
    def Bt_2_Title(self, cur_state):
        if cur_state.name != '블루스택':
            print(f'현재상태 = {cur_state}, 원하는 상태 = 블루스택')
            return
        
        commons.touch_on_text('삼국지K')        
        time.sleep(10)
        pyautogui.press('esc')
        time.sleep(1)

    # 게임시작 버튼 클릭 후 세계진입까지
    @check_state_none
    def start2world(self, cur_state):
        retry_cnt = 0
        while(cur_state.name != '세상'):
            if retry_cnt > 7:
                print(f'start2world함수에서 세계로 진입을 하지 못했습니다.')
                return False
            pyautogui.press('esc')
            time.sleep(3)
            cur_state = commons.get_current_state()
            retry_cnt += 1
        return True
    
    def world2event(self, cur_state):
        # 이벤트는 위치가 첫충전이 없어지는 경우를 제외하고는 바뀌지 않음
        event_coord = (391, 127)
        retry_cnt = 0
        while(cur_state.name != '이벤트'):
            if retry_cnt > 7:
                print(f'world2event함수에서 이벤트로 진입을 하지 못했습니다.')
                return False
            commons.mouseclick(event_coord)
            time.sleep(2)
            cur_state = commons.get_current_state()
            retry_cnt += 1
        return True
        
        
    def server_start(self, idx):        
        touch_texts = ['서버클리', '시즌서버', 'HB']
        for t in touch_texts:
            commons.touch_on_text(t)
            time.sleep(1)
        commons.selectserver(idx)
        time.sleep(1)
        commons.touch_on_text('게임시작')
        time.sleep(15)
            
    # 나라가입은 ocr인식이 잘 되지 않아 상대좌표에 click하는 형태로 구현함
    def join_country(self, country_name):
        print(f'{country_name} 나라의 가입을 시작합니다.')        
        country_list = {"한":(404, 222), "위":(638, 223), "마":(889, 214), '촉':(301, 434), '오':(538, 429), '원':(769, 423)}

        # click으로는 촉나라 아이콘의 가입화면으로 넘어가지 않아
        # mouse down으로 변경
        for i in range(3):            
            pyautogui.mouseDown(country_list[country_name])    
            time.sleep(0.5)
            pyautogui.mouseUp(country_list[country_name])
            
        # 컨펌화면
        commons.touch_on_text('가입')
        time.sleep(1)
        self.naming()
        

    # naming화면은 ocr결과가 좋지 않으므로 절대좌표로 박음
    def naming(self):
        # pyautogui.click(1051, 543, duration=0.5)
        commons.mouseclick((1051,543))
        time.sleep(1)

        # 이름 입력창뜨고
        for i in range(10):
            pyautogui.press('backspace')

        time.sleep(1)
        # 청운지지 서버의 경우 불법문자로 인식됨.
        if self.current_server in self.illegalstr:
            user_name = self.illegalstr[self.current_server]
        elif self.current_server[0] == 'S':
            user_name = self.current_server[2:] + self.postfix
        else:
            user_name = self.current_server + self.postfix
            
        pyperclip.copy(user_name)        
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        # commons.touch_on_text('게임시작')
        commons.mouseclick((1065, 644))
        time.sleep(10)










    

