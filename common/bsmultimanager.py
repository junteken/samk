from screen import capbluestack
from common import commons
import time
import pyautogui

class BsMultiManager(object):

    def __init__(self):
        self.window_name= "BlueStacks Multi-Instance Manager"
        self.ref_image_name = "./rsrc/state_img/bluestack_manager.PNG"
        self.sample_text_file = "./rsrc/state_img/블루스택매니저.txt"
        self.bs= capbluestack.CapBlueStack()
        self.current_bsIdx=0 #현재 bluestack instance number



    #idx에 해당하는 bluestack을 새로 시작하는 함수
    def do_restart(self, idx=0):
        #bbox의 x좌표를 기준으로 x를 눌러 종료
        print('bluestack 재시작!!! %d', idx)

        #esc키를 0.1초 단위로 5회 까지 날린다

        bbox, img = self.get_CurrentBsImg()

        pyautogui.click(bbox[0], bbox[1]);

        for i in range(3):
            pyautogui.press('esc', interval= 0.5)

        self.is_GameQuit()
        time.sleep(1)
        self.do_executeSamK()

        for i in range(5):
            pyautogui.press('space', interval= 1)

        self.is_notice()

        time.sleep(1)

        pyautogui.press('space', interval= 1)


    # 현재 화면의 screen을 캡처하고 ocr결과를 돌려준다.
    def get_screen_ocr(self):
        bbox, img = self.get_CurrentBsImg()
        ocr_result = commons.scan(img)

        return bbox, ocr_result

    def is_notice(self):
        bbox, ocr_result= self.get_screen_ocr()
        found = commons.search_word(ocr_result, '공지')
        found = commons.search_word(ocr_result, '확인')
        pyautogui.click(bbox[0] + found[0][0][0][0], bbox[1] + found[0][0][0][1])


    def do_executeSamK(self):
        bbox, ocr_result= self.get_screen_ocr()
        found=commons.search_word(ocr_result, '삼국지K')
        pyautogui.click(bbox[0] + (found[0][0][0][0]+found[0][0][1][0])/2, bbox[1] + (found[0][0][0][1]+found[0][0][2][1])/2)


    #현재 게임 화면이 "게임을 종료하시겠습니까?"
    def is_GameQuit(self):
        bbox, ocr_result= self.get_screen_ocr()
        found= commons.search_word(ocr_result, '게임을 나가시겠습니까', True)
        found= commons.search_word(ocr_result, '확인')
        if len(found) > 0:
            pyautogui.click(bbox[0] + found[1][0][0][0], bbox[1] + found[1][0][0][1])



    def get_CurrentBsImg(self):
        return self.bs.select_bluestack(self.current_bsIdx)

    def get_CurrentBsXY(self):
        return self.bs.get_window_rect(self.current_bsIdx)











    #bluestack multi-instance manager의 화면을 보고 해당 name을 가진 instance를 실행하는 기능
    #def ExecBS(self, name):




