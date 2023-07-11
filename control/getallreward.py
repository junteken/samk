from typing import Any
from control.controlbase import ControlBase
from common import commons
from invalidstateerror import InvalidStateError
import pyautogui
import time

class GetAllReward(ControlBase):

    # [S 0O1] <-- 요렇게 인식됨

    def __init__(self):
        super().__init__()
        self.name='모든 서버 보상 얻기'
        # 모든 제어는 최초 화면 상태를 맞추고 시작해야하므로 최초 화면의 상태를 
        self.start_screen_state = commons.state_dict['타이틀화면']
        self.serverlist = []
        self.current_server = None

    def run(self):
        # 처음에는 해당 state가 맞는지 검사해야함
        chk_state = self.check()
        if chk_state is False:
            print('자동화를 시작하기위한 초기 상태가 아닙니다.')
            raise InvalidStateError("자동화를 시작하기위한 초기 상태가 아닙니다.")
        
        print('초기상태 일치 확인완료')

        # 탐색할 서버의 txt파일이름을 아래에 넣어준다.
        sv_list = self.getserverlist('hb')

        for sv in sv_list:
            self.current_server = sv
            # 초기상태는 타이틀화면 이다.                        
            touch_texts = ['서버클리', '시즌서버', 'HB']
            for t in touch_texts:
                commons.touch_on_text(t)
                time.sleep(1)

            commons.touch_on_text(sv)
            self.receive_bokji()
            break        

    def receive_bokji(self):
        print(f'{self.current_server} 서버의 복지 받기가 시작되었습니다.')
        # 현재 복지를 받아야할 서버의 타이틀 화면이다.
        pyautogui.press('w', interval= 1)
        time.sleep(1)

        #시작버튼을 누르면 여러가지 화면으로 바뀐다.
        cur_state = commons.get_current_state()

        if cur_state.name == '국가선택':
            # touch_texts = ['괜담가입', ]
            self.join_country('촉')


    # 나라가입은 ocr인식이 잘 되지 않아 상대좌표에 click하는 형태로 구현함
    def join_country(self, country_name):
        country_list = {"한":(404, 222), "위":(638, 223), "마":(889, 214), '촉':(301, 434), '오':(538, 429), '원':(769, 423)}

        pyautogui.click(country_list[country_name][0], country_list[country_name][1])
        time.sleep(1)
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
        pyautogui.write(user_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        commons.touch_on_text('게임시작')








    


        


    def getserverlist(self, filename):
        filepath = './rsrc/' + filename
        sv_list = []
        with open(filepath, "r", encoding="utf-8") as file:
            sv_list = [line.strip() for line in file]

        return sv_list

            

        



        


       

        

        


