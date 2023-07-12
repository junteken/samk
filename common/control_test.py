import cv2
import os

def image_matching(large_image_path, small_image_path):
    # 이미지 파일을 읽어옵니다.
    large_image = cv2.imread(large_image_path, cv2.IMREAD_COLOR)
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


# 이미지 파일 경로
large_image_path = '.\\rsrc\\state_img\\world.png'
small_image_path = '.\\rsrc\\target_img\\bokji.png'

large_image_path = os.path.abspath(large_image_path)
small_image_path = os.path.abspath(small_image_path)

result = image_matching(large_image_path, small_image_path)

if len(result) > 0:
    print("작은 이미지가 큰 이미지 안에 있습니다.")
    print("좌표:", result[0])
else:
    print("작은 이미지가 큰 이미지 안에 없습니다.")
