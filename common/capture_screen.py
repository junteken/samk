import ctypes
import pywinauto
import win32gui
import win32ui
from PIL import Image

def getWindowScreenshot(handle):
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    width, height = right - left, bottom - top

    hwnd_dc = win32gui.GetWindowDC(handle)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    ctypes.windll.user32.PrintWindow(handle, save_dc.GetSafeHdc(), 0)
    bmp_info = save_bitmap.GetInfo()
    bmp_str = save_bitmap.GetBitmapBits(True)

    img = Image.frombuffer(
        'RGB',
        (bmp_info['bmWidth'], bmp_info['bmHeight']),
        bmp_str, 'raw', 'BGRX', 0, 1)
    
    # 메모리를 해제합니다.
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(handle, hwnd_dc)

    return img

app_title = 'romancek'
handle = win32gui.FindWindow(None, app_title)

if handle == 0:
    print(f"'{app_title}' 애플리케이션을 찾을 수 없습니다.")
else:
    screenshot = getWindowScreenshot(handle)
    screenshot.save('screenshot.png')
    print(f'화면 캡처 완료, 저장된 파일명: screenshot.png')
