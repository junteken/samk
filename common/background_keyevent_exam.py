import win32api
import win32con
import win32gui

# 애플리케이션 제목
app_title = 'your_app_title'

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
    post_key_event(window, ord('A'))

    # 예: 마우스 왼쪽 클릭을 x=100, y=100 좌표로 보냅니다.
    post_mouse_event(window, 100, 100)

    print("이벤트 전송 완료")
