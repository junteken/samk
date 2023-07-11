import easyocr
import io
import os, sys, inspect
from pathlib import Path
from common.bsmultimanager import BsMultiManager
from invalidstateerror import InvalidStateError
import time
import pyautogui

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

def scan(bsimage):
    img_byte = io.BytesIO()
    bsimage.save(img_byte, format='PNG')
    img_byte = img_byte.getvalue()

    result = g_reader.readtext(img_byte, detail=1)

    print(result)

    return result

def search_word(ocr_result, keyword, debug=False):
    found = [v for _, v in enumerate(ocr_result) if keyword in v[1]]

    if debug:
        if found is None:
            print('단어를 찾지 못했습니다.')
        else:
            for w in found:
                print('단어를 찾았습니다.')

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


    for i in range(len(state_instances)):
        for j in range(i + 1, len(state_instances)):
            if state_instances[i].check(state_instances[j].img):
                print(f'feature가 충돌 나는 state발견 {state_instances[i].name} 과 {state_instances[j].name}')
                raise RuntimeError("state , feautre설정 오류")

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
def touch_on_text(text):
    bbox, result = bsm.get_screen_ocr()
    found = search_word(result, text)
    if len(found) == 0:
        print('단어를 찾지 못하였습니다.')
        return False
    
    pyautogui.click(bbox[0] + found[0][0][0][0], bbox[1] + found[0][0][0][1])
    
    
    