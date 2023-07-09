import os, sys, inspect
from pathlib import Path
from common import commons, bsmultimanager
from screen import *
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

state_instances = []

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

for i in range(len(state_instances)):
    for j in range(i + 1, len(state_instances)):
        if state_instances[i].cross_check(state_instances[j].img):
            print(f'feature가 충돌 나는 state발견 {state_instances[i].name} 과 {state_instances[j].name}')

print('검사완료')

# 여기까지

# 생성된 state_instance들은 각자 자신의 feature text와 img ocr결과를 비교하고 다른 

# bsm= bsmultimanager.BsMultiManager()
# bsm.do_restart()

# 윈도우 생성
root = tk.Tk()
root.title("GUI Example")

# 프레임 생성
left_frame = ttk.Frame(root)
left_frame.pack(side="left", padx=5, pady=10)

right_frame = ttk.Frame(root)
right_frame.pack(side="right", padx=5, pady=10)

bottom_frame = ttk.Frame(root)
bottom_frame.pack(side="bottom", padx=5, pady=10, fill="x")

# 리스트뷰 생성
list_view = ttk.Treeview(left_frame)
list_view.pack(fill="both", expand=True)

# 여러 데이터 삽입
for i in range(5):
    list_view.insert('', 'end', text="Item " + str(i))

# 이미지뷰 생성
image = Image.open("./rsrc/state_img/world.jpg")  # 여기에 로컬 이미지 파일 경로를 입력하세요.
photo = ImageTk.PhotoImage(image)

image_label = ttk.Label(right_frame, image=photo)
image_label.pack()

# 텍스트뷰와 스크롤바를 위한 프레임 생성
text_frame = ttk.Frame(left_frame)
text_frame.pack(fill="both", expand=True)

# 텍스트뷰 및 스크롤바 생성
text_view = tk.Text(text_frame, wrap="word")
text_view.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_view.yview)
scrollbar.pack(side="right", fill="y")

text_view.config(yscrollcommand=scrollbar.set)

# 왼쪽 프레임의 하단에 버튼 추가
bottom_frame = ttk.Frame(left_frame)
bottom_frame.pack(side="bottom", padx=5, pady=10, fill="x")

def on_start_click():
    print("Button clicked!")

def on_cancel_click():
    print("Button clicked!")

# 버튼 생성
start_btn = ttk.Button(bottom_frame, text="시작", command=on_start_click)
start_btn.pack(side="left", padx=5)
cancel_btn = ttk.Button(bottom_frame, text="중지", command=on_cancel_click)
cancel_btn.pack(side="left", padx=5)


# 메인 루프 실행
root.mainloop()