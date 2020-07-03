from ctypes import windll, wintypes, byref, sizeof

from PIL import ImageGrab
import win32gui

class CapBlueStack(object):

    def __init__(self):
        self.winlist=[]
        self.toplist=[]
        win32gui.EnumWindows(self.enum_cb, self.toplist)
        self.bslist=[(hwnd, title) for hwnd, title in self.winlist if 'bluestacks' in title.lower()]
        print("검출된 bluestack 갯수는 "+ str(len(self.bslist)))

    def printBS(self):
        for b in self.bslist:
            print("bs="+ b[1])



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

    def select_bluestack(self, idx):
        win32gui.SetForegroundWindow(self.bslist[idx][0])
        bbox = self.get_window_rect(idx)
        img = ImageGrab.grab(bbox)
        img.show()
        return img
