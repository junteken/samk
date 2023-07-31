from typing import Any
from common import commons
from invalidstateerror import InvalidStateError
import threading
import pyautogui
import time

def check_state_none(func):
    @wraps(func)
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
    def Bt_2_Title(cur_state):
        if cur_state != '블루스택':
            print(f'현재상태 = {cur_state}, 원하는 상태 = 블루스택')
            return
        
        commons.touch_on_text('삼국지K')        
        time.sleep(10)
        pyautogui.press('esc')
        time.sleep(1)

    # 게임시작 버튼 클릭 후 세계진입까지
    @check_state_none
    def start2world(cur_state):
        if cur_state == '기능오픈':
            pyautogui.press('esc')
            time.sleep(3)
            cur_state = commons.get_current_state()

            while(cur_state != '세계'):
                pyautogui.press('esc')
                time.sleep(3)
                cur_state = commons.get_current_state()

            return True
        elif cur_state == '첫충전':
            









    

