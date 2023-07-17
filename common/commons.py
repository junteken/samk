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

g_reader = easyocr.Reader(['ko', 'en'], gpu=True)

window_name = 'romancek'
window_bbox = None
state_instances = []
state_dict = {}
bsm= BsMultiManager()
log_text_view = None
page_scroll_unit = 62
server_name_font_height = 61
left_server_point = (540, 213)
right_server_point = (920, 213)



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
    found = [v for _, v in enumerate(ocr_result) if keyword in v[1]]
    # debugging용 풀어쓰기
    # found = []
    # for _, v in enumerate(ocr_result):
    #     if keyword in v[1]:
    #         found.append(v)
    if len(found) == 0:
        max = 0
        for _, v in enumerate(ocr_result):
             t = difflib.SequenceMatcher(None, v[1], keyword).ratio()
             if t > 0.2 and t > max:
                 found.append(v)
    return found

def setup():
    # screen에 있는 모든 class들의 인스턴스를 생성하는 코드
    window_bbox = bsm.get_CurrentBsImg()
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
    loop = 0
    while(True and loop < 5):
        _, texts = get_current_text()
        for state in state_instances:
            if state.check(texts):
                return state
        loop = loop + 1
            
        time.sleep(0.5)
        
    return state_dict['알수없음']

def get_current_text():
    bbox, img = bsm.get_CurrentBsImg()
    ocr_result = scan(img)
    recog_texts = [v[1] for _, v in enumerate(ocr_result)]
    return ocr_result, recog_texts

def moveTo_mouse(coord):
    pyautogui.moveTo(bsm.current_bsBbox[0]+coord[0], 
                     bsm.current_bsBbox[1]+coord[1])
    
def mouseclick(coord):
    pyautogui.click(bsm.current_bsBbox[0]+coord[0], 
                     bsm.current_bsBbox[1]+coord[1])
# 인자로 주어진 text영역을 터지하는 함수
# 동일한 text가 없다면 가장 유사한 문자의 첫번째 인자를 터치
def touch_on_text(text, coord=None):
    if coord is not None:
        pyautogui.click(bsm.current_bsBbox[0] + coord[0][0],
                        bsm.current_bsBbox[0] + coord[0][1])
        return True

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
    
    result = find_image_in_another(small_image, large_image)

    if result is not None:
        return result
    else:
        return None

def find_image_in_another(image1, image2):

    img1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # ORB 검출기 생성
    orb = cv2.ORB_create()

    # 이미지 1 (template)에서 ORB 특징점 검출
    keypoints1, descriptors1 = orb.detectAndCompute(img1_gray, None)

    # 이미지 2 (target)에서 ORB 특징점 검출
    keypoints2, descriptors2 = orb.detectAndCompute(img2_gray, None)

    # Brute Force 매칭기 초기화 및 매칭시작
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)

    # 매칭된 결과를 거리에 따라 정렬
    matches = sorted(matches, key = lambda x:x.distance)

    # 일정 비율 이상의 좋은 매칭점만 추출
    good_matches = []
    for m in matches:
        if m.distance < 60:
            good_matches.append(m)

    # 매칭된 특징점이 일정 개수 이상일 경우 이미지 1 (template)이 이미지 2 (target)에 포함되어 있는 것으로 판단
    if len(good_matches) > 5:

        # 매칭 결과로부터 이미지 1 (template)과 이미지 2 (target)에서 매칭된 좌표를 추출
        src_pts = np.float32([ keypoints1[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ keypoints2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)

        # 이미지 1 (template)과 이미지 2 (target)에서 매칭된 특징점을 이용하여 perspective transform 계산
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

        h,w,_ = image1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        x_min, y_min = dst.min(axis=0)
        x_max, y_max = dst.max(axis=0)

        if x_min >= 0 and y_min >= 0 and x_max <= image2.shape[1] and y_max <= image2.shape[0]:
            return [(x[0], y[0]) for (x,y) in dst]
        else:
            return None

    else:
        return None
    
def touch_on_img(target_img_name):
    _, img = bsm.get_CurrentBsImg()
    tg_img_path = '.\\rsrc\\target_img\\' + target_img_name + '.png'
    coord = None

    coord = find_image_coord(img, tg_img_path)
    if coord is not None:        
        pyautogui.click(coord[0])
        print(f'발견한 이미지 좌표는{coord[0]}')
        time.sleep(1)
        return True
    else:
        print(f'{target_img_name} 이미지를 현재 이미지에서 찾지 못했습니다.')
        return False

def print_log(log):
    if log_text_view:
        log_text_view.insert('end', log)
        log_text_view.insert('end', "'\n'")

def getserverlist(filename):
        filepath = './rsrc/' + filename
        
        with open(filepath, "r", encoding="utf-8") as file:
            sv_list = {line.strip():idx for idx, line in enumerate(file) }

        return sv_list



def scroll_pgdwn(count):
    for i in range(count):
        pyautogui.moveTo(715, 685)
        # pyautogui.drag(0, -520, 10, button='left')
        pyautogui.dragTo(715, 164, 5, pyautogui.easeOutQuad, button='left')
        # pyautogui.drag(10, 0, 2, button='left')
        # time.sleep(1)

def selectserver(index):
    # 8로 나누어 몫과 나머지를 구한다.
    quotient = index // 16
    remainder = index % 16
    scroll_pgdwn(quotient)

    if remainder % 2 == 0:
        #짝수인경우 왼쪽에 있는 서버리스트이다.
        pyautogui.click((left_server_point[0], left_server_point[1] + 
                         server_name_font_height *(remainder//2)))
    else:
        pyautogui.click((right_server_point[0], right_server_point[1] + 
                         server_name_font_height*(remainder//2)))

    time.sleep(1)


    