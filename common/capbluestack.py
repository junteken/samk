from ctypes import windll, wintypes, byref, sizeof

from PIL import ImageGrab
import win32gui
import win32con
from common import commons

'''
window api를 이용해 bluestack process정보를 기반으로 window정보를 가져오는 역할 수행
'''

class CapBlueStack(object):

    def __init__(self):
        self.winlist=[]
        self.toplist=[]
        win32gui.EnumWindows(self.enum_cb, self.toplist)
        self.bslist=[(hwnd, title) for hwnd, title in self.winlist if commons.window_name in title.lower()]
        print(f"검출된 {commons.window_name} 갯수는 + {len(self.bslist)})")

    def printBS(self):
        for b in self.bslist:
            print("bs="+ b[1])

    def set_window_size_default(self, idx=0):
        # window_handle = win32gui.FindWindow(None, commons.window_name)
        window_handle = self.bslist[idx][0]

        if window_handle == 0:
            print(f"'{commons.window_name}' 애플리케이션을 찾을 수 없습니다.")
            return
        
        # win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 0, 0, 1280, 720,  win32con.SWP_SHOWWINDOW)

        rect = win32gui.GetWindowRect(window_handle)        
        x, y = rect[0], rect[1]
        print(f'{commons.window_name}의 시작좌표는 {x}, {y}, width={rect[2]}, height={rect[3]}')
        
        
    def get_window_rect(self, idx):
        """ 핸들에 대응하는 윈도우의 좌표정보를 반환한다
        param:
            <int> hwnd: 윈도우 핸들
        return:
            <tuple> x1, y1, x2, y2
        """
        f = windll.dwmapi.DwmGetWindowAttribute
        rect = wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(wintypes.HWND(self.bslist[idx][0]),
          wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          byref(rect),
          sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom


    def enum_cb(self, hwnd, results):
        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    def select_bluestack(self, idx, debug=False):
        try:
            win32gui.SetForegroundWindow(self.bslist[idx][0])
        except:
            print('win32gui.SetForegroundWindow exception occured!!!')

        bbox = self.get_window_rect(idx)
        img = ImageGrab.grab(bbox)
        if(debug):
            img.show()
        return bbox, img
