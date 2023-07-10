from typing import Any
from control.controlbase import ControlBase
from common import commons
from invalidstateerror import InvalidStateError
import pyautogui
import time

class GetAllReward(ControlBase):

    # [S 0O1] <-- 요렇게 인식됨

    def __init__(self):
        self.name='모든 서버 보상 얻기'
        # 모든 제어는 최초 화면 상태를 맞추고 시작해야하므로 최초 화면의 상태를 
        self.start_screen_state = commons.state_dict['공지']
        self.serverlist = []

    def execute(self, bsm):
        chk_state = super().execute(bsm)

        if chk_state is False:
            print('자동화를 시작하기위한 초기 상태가 아닙니다.')
            raise InvalidStateError("자동화를 시작하기위한 초기 상태가 아닙니다.")
        
        print('초기상태 일치 확인완료')

        # 탐색할 서버의 txt파일이름을 아래에 넣어준다.
        sv_list = self.getserverlist('hb')

        for sv in sv_list:
            # 초기상태는 공지이다.
            pyautogui.press('w', interval= 1)
            time.sleep(1)
            #타이틀
            touch_texts = ['서버클리', '시즌서버', 'HB']
            for t in touch_texts:
                commons.touch_on_text(t)
                time.sleep(1)
            


        
        # 공지화면에서는 w키를 눌러야 title화면으로 이동한다.
        # for i in range(10):
        #     pyautogui.press('w', interval= 1)
        #     time.sleep(1)
        #     current = commons.get_current_state()
        #     if current.name == '타이틀화면':
        #         print('타이틀화면으로 이동 완료')
        #         break
        #     if i == 9:
        #         raise InvalidStateError("공지화면에서 타이틀화면으로 넘어가기실패")
        
        

        

    def receive_bokji():
        pass


    def getserverlist(self, filename):
        filepath = './rsrc/' + filename
        sv_list = []
        with open(filepath, "r", encoding="utf-8") as file:
            sv_list = [line.strip() for line in file]

        return sv_list

            

        



        


       

        

        


