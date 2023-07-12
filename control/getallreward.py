from typing import Any
from control.controlbase import ControlBase
from common import commons
from invalidstateerror import InvalidStateError
import pyautogui
import time
import pyperclip

class GetAllReward(ControlBase):

    # [S 0O1] <-- 요렇게 인식됨
    con_name = '모든 서버 보상 얻기'

    def __init__(self):
        super().__init__()
        # self.name='모든 서버 보상 얻기'
        # 모든 제어는 최초 화면 상태를 맞추고 시작해야하므로 최초 화면의 상태를 
        self.start_screen_state = commons.state_dict['타이틀화면']
        self.serverlist = []
        self.current_server = None
        self.thread_control = False

    def run(self):
        # 처음에는 해당 state가 맞는지 검사해야함
        self.thread_control = True
        chk_state = self.check()
        if chk_state is False:
            print('자동화를 시작하기위한 초기 상태가 아닙니다.')
            raise InvalidStateError("자동화를 시작하기위한 초기 상태가 아닙니다.")
        
        print('초기상태 일치 확인완료')

        # 탐색할 서버의 txt파일이름을 아래에 넣어준다.
        sv_list = self.getserverlist('hb')

        for sv in sv_list:
            # sv = '입초대길'
            self.current_server = sv
            # 초기상태는 타이틀화면 이다.                        
            touch_texts = ['서버클리', '시즌서버', 'HB']
            for t in touch_texts:
                commons.touch_on_text(t)
                time.sleep(1)

            commons.touch_on_text(sv)
            time.sleep(1)
            if self.receive_bokji():
                # 여기 파일로 로깅하는 함수 하나 만들어야됨
                # 일단은 text view에 출력
                commons.print_log(f'{sv}서버 복지 수령 완료')
            else:
                commons.print_log(f'{sv}서버에는 복지가 없었네요')

            time.sleep(1)
            pyautogui.press('esc')
            time.sleep(1)
            cur_state = commons.get_current_state()

            while cur_state.name != '게임종료':
                pyautogui.press('esc')
                time.sleep(1)
                cur_state = commons.get_current_state()

            if cur_state.name == '게임종료':
                print('게임 종료 확인 질문 상태')
                # commons.press_on_text('확인')
                pyautogui.press('enter')
                time.sleep(2)
                cur_state = commons.get_current_state()
                while(cur_state.name == '게임종료'):
                    pyautogui.press('enter')
                    time.sleep(2)

            cur_state = commons.get_current_state()
            if cur_state.name == '블루스택':
                print('게임종료 확인')
                # commons.touch_on_text('삼국지k')
                pyautogui.click(1080, 176)
                time.sleep(10)
                pyautogui.press('esc')
                time.sleep(1)

    def receive_bokji(self):
        print(f'{self.current_server} 서버의 복지 받기가 시작되었습니다.')
        # 현재 복지를 받아야할 서버의 타이틀 화면이다.
        commons.touch_on_text('게임시작')
        time.sleep(15)

        #시작버튼을 누르면 여러가지 화면으로 바뀐다.
        cur_state = commons.get_current_state()

        if cur_state.name == '국가선택': 
            # 한번도 플레이한적이 없어서 나라부터 고르는 경우
            print('나라선택화면')
            self.join_country('촉')                        
        elif cur_state.name == '첫충전':
            print('첫충전 화면')
            pass 
        else:
            print('재돌입 후 이름설정화면')
            self.naming(self.current_server+'빈즈')

        pyautogui.press('esc')
        time.sleep(0.5)

        # 여기까지 오면 세계로 진입했는지 확인하면 된다.
        cur_state = commons.get_current_state()
        if cur_state.name != '세상':
            raise InvalidStateError(cur_state, commons.state_dict['세상'])
        
        commons.touch_on_img('bokji')
        time.sleep(1)
        cur_state = commons.get_current_state()
        if cur_state.name != '보상':
            print(f'{self.current_server} 서버의 복지는 없네요')
            return False

        while(cur_state.name == '보상'):
            print('보상이 존재합니다.')
            commons.touch_on_text('모두수령')
            time.sleep(1)
            cur_state = commons.get_current_state()

        print(f'{self.current_server} 서버의 복지 수령완료')
        return True


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

        self.naming(self.current_server+'빈즈')

    def naming(self, user_name):
        pyautogui.click(987, 532)
        time.sleep(1)

        # 이름 입력창뜨고
        for i in range(10):
            pyautogui.press('backspace')

        time.sleep(1)
        pyperclip.copy(user_name)        
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        commons.touch_on_text('게임시작')
        time.sleep(3)

    def getserverlist(self, filename):
        filepath = './rsrc/' + filename
        sv_list = []
        with open(filepath, "r", encoding="utf-8") as file:
            sv_list = [line.strip() for line in file]

        return sv_list

            

        



        


       

        

        

