import easyocr
import io
import os, sys, inspect
from pathlib import Path
from common.bsmultimanager import BsMultiManager
from invalidstateerror import InvalidStateError
import difflib
import pyautogui
import cv2
import numpy as np
import time

g_reader = easyocr.Reader(['ko', 'en'], gpu=False)

accountList={
    "창천" : "BlueStacks",
    "초월" : "",
    "은선" : "",
    "백호" : "",
    "주작" : "",
    "진룡" : "",
    "봉무" : "",
    "정련" : "",
}

window_name = 'romancek'
state_instances = []
state_dict = {}
bsm= BsMultiManager()
log_text_view = None

def scan(bsimage):
    img_byte = io.BytesIO()
    bsimage.save(img_byte, format='PNG')
    img_byte = img_byte.getvalue()
    result = g_reader.readtext(img_byte, detail=1)

    return result

# 해당 keyword가 ocr_result에 존재하는지
# return : 찾은 단어의 ocr_result의 v값들을 리턴해주거나
# 찾고자 하는 단어와 가장 유사한 v값을 리턴해준다.
def search_word(ocr_result, keyword):    
    # found = [v for _, v in enumerate(ocr_result) if keyword in v[1]]
    found = []
    for _, v in enumerate(ocr_result):
        if keyword in v[1]:
            found.append(v)
    if len(found) == 0:
        max = 0
        for _, v in enumerate(ocr_result):
             t = difflib.SequenceMatcher(None, v[1], keyword).ratio()
             if t > max:
                 found.append(v)
    return found

def setup():
    # screen에 있는 모든 class들의 인스턴스를 생성하는 코드
    modules_folder_path = Path("screen")
    sys.path.insert(0, str(modules_folder_path.resolve()))

    exclude_list = ['featurebase.py', 'capbluestack.py']

    module_files = [f for f in os.listdir(modules_folder_path) if f.endswith('.py') and f not in exclude_list]

    for module_file in module_files:
        module_name = module_file[:-3]  # 확장자 (.py)를 제거합니다.
        module = __import__(module_name)

        # 모든 클래스의 객체를 생성
        for _, cls in inspect.getmembers(module, predicate=inspect.isclass):
            if cls.__module__ == module.__name__:
                state_instances.append(cls())

    for obj in state_instances:
        obj_name = obj.name
        state_dict[obj_name] = obj

    print('모든 state class의 객체들 생성완료')

def first_check():   

    for s in state_instances:
        if not s.check():
            print(f'{s.name} state class의 feature texts설정이 잘못 되었습니다. 다시 설정하세요')
        else:
            print(f'{s.name} state class의 feature texts설정 정상 확인')

    print('모든 state 객체들 self check완료')

    # cross-check는 일단 주석처리함, 현재 naming화면의경우 
    # feature text를 뽑기가 애매함(게임시작밖에...)
    # for i in range(len(state_instances)-1):
    #     for j in range(i + 1, len(state_instances)):
    #         if state_instances[i].check(state_instances[j].feature_texts):
    #             print(f'feature가 충돌 나는 state발견 {state_instances[i].name} 과 {state_instances[j].name}')
    #             raise RuntimeError("state , feautre설정 오류")

    print('검사완료')
    # 여기까지

    # 생성된 state_instance들은 각자 자신의 feature text와 img ocr결과를 비교하고 다른 


# 현재 화면의 state을 돌려주는 공용함수
def get_current_state():
    texts = get_current_text()
    for state in state_instances:
        if state.check(texts):
            return state
        
    raise RuntimeError("현재 화면의 대응되는 screen state가 정의되지 않았습니다.")

def get_current_text():
    bbox, img = bsm.get_CurrentBsImg()
    ocr_result = scan(img)
    recog_texts = [v[1] for _, v in enumerate(ocr_result)]
    return recog_texts


# 인자로 주어진 text영역을 터지하는 함수
# 동일한 text가 없다면 가장 유사한 문자의 첫번째 인자를 터치
def touch_on_text(text):
    bbox, result = bsm.get_screen_ocr()
    found = search_word(result, text)
    if len(found) == 0:
        print(f'{text} 단어를 찾지 못하였습니다.')
        return False
    
    pyautogui.click(bbox[0] + found[0][0][0][0], bbox[1] + found[0][0][0][1])
    
def press_on_text(text):
    bbox, result = bsm.get_screen_ocr()
    found = search_word(result, text)
    if len(found) == 0:
        print(f'{text} 단어를 찾지 못하였습니다.')
        return False
        
    pyautogui.mouseDown(bbox[0] + found[0][0][0][0], bbox[1] + found[0][0][0][1])
    time.sleep(0.5)
    pyautogui.mouseUp(bbox[0] + found[0][0][0][0], bbox[1] + found[0][0][0][1])
    
# small_image_path는 윈도우에서 
# 아래와 같은 형태로 변경해서 넣어줘야한다.
# small_image_path = '.\\rsrc\\target_img\\bokji.png'
def find_image_coord(large_image, small_image_path):
    np_img = np.array(large_image)
    large_image = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    # 이미지 파일을 읽어옵니다.    
    small_image_path = os.path.abspath(small_image_path)
    small_image = cv2.imread(small_image_path, cv2.IMREAD_COLOR)

    # 큰 이미지와 작은 이미지의 높이와 너비를 가져옵니다.
    large_height, large_width = large_image.shape[:2]
    small_height, small_width = small_image.shape[:2]

    # 템플릿 매칭 메소드를 사용해 이미지를 매칭합니다.
    result = cv2.matchTemplate(large_image, small_image, cv2.TM_CCOEFF_NORMED)

    # 최소 스코어와 최대 스코어 및 그 위치를 찾습니다.
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 임계값을 설정하고 매칭된 위치를 찾습니다 (역치에 맞는 경우).
    threshold = 0.8
    match_result = []

    if max_val > threshold:
        match_result.append(max_loc)

    return match_result

def touch_on_img(target_img_name):
    _, img = bsm.get_CurrentBsImg()
    tg_img_path = '.\\rsrc\\target_img\\' + target_img_name + '.png'
    coord = None

    coord = find_image_coord(img, tg_img_path)
    if len(coord) > 0:        
        pyautogui.click(coord[0])
    else:
        print(f'{target_img_name} 이미지를 현재 이미지에서 찾지 못했습니다.')

def print_log(log):
    if log_text_view:
        log_text_view.insert('end', log)
        log_text_view.insert('end', "'\n'")