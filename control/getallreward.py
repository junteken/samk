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
        self.serverlist = None
        self.current_server = None
        self.current_server_coord = None
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
        self.serverlist = self.getserverlist('hb')

        for sv in self.serverlist:
            if self.thread_control is False:
                return
            # sv = '입초대길'
            self.current_server = sv
            # 초기상태는 타이틀화면 이다.                        
            touch_texts = ['서버클리', '시즌서버', 'HB']
            for t in touch_texts:
                commons.touch_on_text(t)
                time.sleep(1)

            # 서버가 없다면 scroll해야함
            if self.scroll_until_find_server(self.current_server) is False:
                continue            
            commons.touch_on_text(self.current_server)

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

            cur_state = commons.get_current_state()
            if cur_state.name == '블루스택':
                print('게임종료 확인')
                commons.touch_on_text('삼국지K')
                # pyautogui.click(1080, 176)
                time.sleep(10)
                pyautogui.press('esc')
                time.sleep(1)

    # ocr인식 문제로 아래와 같은 알고리즘으로 변경
    # 입춘대길 = 입초대길 로 인식하는 경우 순서와 글자 2개만
    # 맞으면 해당 서버가 있는걸로 판단하고 해당좌표와 존재유무를 리턴
    def scroll_until_find_server(self, server_name):
        while True :
            ocr_result, _ = commons.get_current_text()
            for _, v in enumerate(ocr_result):
                if self.is_included(server_name, v[1]):
                    self.current_server_coord = v[0]
                    return True
                elif self.is_included(self.serverlist[-1], v[1]):
                    print(f'{server_name} 서버를 찾지 못했습니다.')
                    return False
            
            pyautogui.moveTo(730, 312)
            pyautogui.scroll(-10)
            time.sleep(3)

            # 서버를 못찾으면 scroll해야함
    def is_included(self, str1, str2):
        count = 0
        for ch in str1:
            if ch in str2:
                count += 1
                str2 = str2.split(ch, 1)[1]

        matching_percent = (count / len(str1)) * 100

        return matching_percent >= 50

    def receive_bokji(self):
        print(f'{self.current_server} 서버의 복지 받기가 시작되었습니다.')
        # 현재 복지를 받아야할 서버의 타이틀 화면이다.
        commons.touch_on_text('게임시작')
        time.sleep(15)

        #시작버튼을 누르면 여러가지 화면으로 바뀐다.
        cur_state = commons.get_current_state()

        if cur_state is None:
            print('재돌입 후 이름설정화면')
            self.naming(self.current_server+'빈즈')
        
        # naming state가 없는 이유는 title과 겹치기때문
        # elif cur_state.name == '유저이름':
        #     print('재돌입 후 이름설정화면')
            # self.naming(self.current_server+'빈즈')
        elif cur_state.name == '국가선택': 
            # 한번도 플레이한적이 없어서 나라부터 고르는 경우
            print('나라선택화면')
            self.join_country('촉')                        
        elif cur_state.name == '첫충전':
            print('첫충전 화면')
            pass 

        cur_state = commons.get_current_state()

        if cur_state.name == '첫충전':
            pyautogui.press('esc')
            time.sleep(5) # 첫충전화면을 끄면 기능오픈이 뜰수도 있으므로

        # 여기까지 오면 세계로 진입했는지 확인하면 된다.
        cur_state = commons.get_current_state()
        while(cur_state is None or cur_state.name != '세상'):
            # 세상이 아니라 기능오픈인경우 나간다
            pyautogui.press('esc')
            time.sleep(5)
            cur_state = commons.get_current_state()
        
        # 일단 image matching은 잘 동작하지 않아 절대좌표로
        # success = commons.touch_on_img('bokji')        
        success = self.search_bokji()
        if success:
            cur_state = commons.get_current_state()
            if cur_state is not None and cur_state.name != '보상':
                success = False                

            else:
                while(success):
                    time.sleep(1)
                    print('보상이 존재합니다.')
                    commons.touch_on_text('모두수령')
                    # 모두수령의 경우 lv점핑이 들어있는경우 시간이 오래걸리므로
                    time.sleep(10)
                    cur_state = commons.get_current_state()
                    if cur_state.name != '보상':
                        success = False
                    
                    if cur_state.name == '레벨업':
                        pyautogui.press('esc')
                        time.sleep(1)

        else:
            print(f'{self.current_server} 서버의 복지는 없네요')
            return False

        print(f'{self.current_server} 서버의 복지 수령완료')
        return True
    
    def search_bokji(self):
        # 복지가 있을수 있는 좌표 (244, 213), (319, 212), (751, 130)

        bokji_coord = [(611, 129), (679, 128), (756, 131)]
        for coord in bokji_coord:
            pyautogui.click(coord)
            time.sleep(3)
            cur_state = commons.get_current_state()
            if cur_state.name == '보상':
                return True
            else:
                pyautogui.press('esc')
                time.sleep(3)
            
        return False



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

    # naming화면은 ocr결과가 좋지 않으므로 절대좌표로 박음
    def naming(self, user_name):
        pyautogui.click(1051, 543, duration=0.5)
        time.sleep(1)

        # 이름 입력창뜨고
        for i in range(10):
            pyautogui.press('backspace')

        time.sleep(1)
        pyperclip.copy(user_name)        
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        # commons.touch_on_text('게임시작')
        pyautogui.click(1065, 644)
        time.sleep(10)

    def getserverlist(self, filename):
        filepath = './rsrc/' + filename
        sv_list = []
        with open(filepath, "r", encoding="utf-8") as file:
            sv_list = [line.strip() for line in file]

        return sv_list

            

        



        


       

        

        


