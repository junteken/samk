import pyautogui
import CapBlueStack
from screen.notice import Notice
import commons
#from pytesseract import *
import cv2

screenWidth, screenHeight = pyautogui.size()
bluestackimg= CapBlueStack.CapBlueStack()


nt= Notice()
img= bluestackimg.select_bluestack(0)
bluestackimg.printBS();

#commons.gcv.detect_text(img)
#text = pytesseract.image_to_string(img,lang='Hangul+eng')
