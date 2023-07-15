from screen import capbluestack
from common import commons
import time
import pyautogui

class BsMultiManager(object):

    def __init__(self):
        self.bs= capbluestack.CapBlueStack()
        self.bs.set_window_size_default()
        self.current_bsIdx=0 #현재 bluestack instance number
        self.current_bsBbox=None
        self.fn_update_imageview = None
    
    # 현재 화면의 screen을 캡처하고 ocr결과를 돌려준다.
    def get_screen_ocr(self):
        self.current_bsBbox, img = self.get_CurrentBsImg()
        ocr_result = commons.scan(img)

        return self.current_bsBbox, ocr_result

    def get_CurrentBsImg(self):
        self.current_bsBbox, img = self.bs.select_bluestack(self.current_bsIdx)
        if self.fn_update_imageview:
            self.fn_update_imageview(img)

        return self.current_bsBbox, img        

    def get_CurrentBsXY(self):
        return self.bs.get_window_rect(self.current_bsIdx)
