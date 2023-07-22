import win32api
import win32con
import win32gui
import pywintypes

# 애플리케이션 제목
app_title = 'romancek'

def enum_child_proc(wnd, param):
    print("    Handling child 0x{:08X} - [{:}] - 0x{:08X}".format(wnd, win32gui.GetWindowText(wnd), win32gui.GetParent(wnd)))
    if param[0] >= 0:
        if param[1] == param[0]:
            win32gui.SendMessage(wnd, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
            return 0
        param[1] += 1


def handle_window(wnd, child_index=-1):
    print("Handling 0x{:08X} - [{:}]".format(wnd, win32gui.GetWindowText(wnd)))
    cur_child = 0
    param = [child_index, cur_child]
    try:
        win32gui.EnumChildWindows(wnd, enum_child_proc, param)
    except pywintypes.error as e:
        if child_index < 0 or e.args[0]:
            raise e
        

def post_key_event(handle, key_code):
    win32api.SendMessage(handle, win32con.WM_KEYDOWN, key_code, 0)
    win32api.SendMessage(handle, win32con.WM_KEYUP, key_code, 0)

def post_mouse_event(handle, x, y):
    l_param = win32api.MAKELONG(x, y)
    win32gui.PostMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.PostMessage(handle, win32con.WM_LBUTTONUP, 0, l_param)

window = win32gui.FindWindow(None, app_title)

if window == 0:
    print("존재하지 않거나 찾을 수 없는 창입니다.")
else:
    # 예: 키보드 A를 보냅니다.
    # post_key_event(window, ord('w'))

    # # 예: 마우스 왼쪽 클릭을 x=100, y=100 좌표로 보냅니다.
    # post_mouse_event(window, 100, 100)

    print("이벤트 전송 완료")

    handle_window(window)

    # post_key_event(0x000C0762, 'w')
    win32gui.SetWindowPos(window, win32con.HWND_TOP, 0, 0, 1280, 720,  win32con.SWP_SHOWWINDOW)

    rect = win32gui.GetWindowRect(window)        
    x, y = rect[0], rect[1]
    print(f'{app_title}의 시작좌표는 {x}, {y}, width={rect[2]}, height={rect[3]}')

