
from common import commons, bsmultimanager
from screen import *
import time
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import threading

commons.setup()
# commons.first_check()

import control_manager

# 전역변수 설정
current_control_item = None
stop_event = threading.Event()
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

def get_selected_item_text(event=None):
    item = list_view.item(list_view.focus()) # 선택된 항목의 아이디 가져오기
    cur_item = item['text'] # 아이디를 사용해 항목의 텍스트 속성 가져오기
    return cur_item    

# 리스트뷰 생성
list_view = ttk.Treeview(left_frame, selectmode='browse')
list_view.bind('<<TreeviewSelect>>', get_selected_item_text)
list_view.pack(fill="both", expand=True)



# 여러 데이터 삽입
# for i in len(control_manager.control_item):
#     list_view.insert('', 'end', text="Item " + str(i))
for item in control_manager.control_item:
    list_view.insert('', 'end', text=item.con_name)


# 이미지뷰 생성
# image = Image.open("./rsrc/state_img/world.jpg")  # 여기에 로컬 이미지 파일 경로를 입력하세요.
_, cur_img = commons.bsm.get_CurrentBsImg()
photo = ImageTk.PhotoImage(cur_img)

def mouse_click_event(event):
    x, y = event.x, event.y
    print(f"Relative coordinates: ({x}, {y})")

image_label = ttk.Label(right_frame, image=photo)
image_label.pack()
image_label.bind('<Button-1>', mouse_click_event)

# 텍스트뷰와 스크롤바를 위한 프레임 생성
text_frame = ttk.Frame(left_frame)
text_frame.pack(fill="both", expand=True)

# 텍스트뷰 및 스크롤바 생성
text_view = tk.Text(text_frame, wrap="word")
text_view.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_view.yview)
scrollbar.pack(side="right", fill="y")

text_view.config(yscrollcommand=scrollbar.set)

commons.log_text_view = text_view

# 왼쪽 프레임의 하단에 버튼 추가
bottom_frame = ttk.Frame(left_frame)
bottom_frame.pack(side="bottom", padx=5, pady=10, fill="x")

def on_start_click():
    global current_control_item
    selected_item = get_selected_item_text()
    current_control_item = control_manager.control_dict[selected_item]

    current_control_item(stop_event).start()

def on_cancel_click():
    stop_event.set()

def on_scan_click():
    _, ocr_text = commons.get_current_text()
    bbox, img = commons.bsm.get_CurrentBsImg()
    update_image(img)
    text_view.insert('end', ocr_text)
    text_view.insert('end', "'\n'")

def on_save_click():
    bbox, img = commons.bsm.get_CurrentBsImg()
    file_name = filedialog.asksaveasfilename(defaultextension=".png", 
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_name:
        img.save(file_name)

def update_image(img):
    global photo
    # 이미지 업데이트    
    new_photo = ImageTk.PhotoImage(img)
    image_label.configure(image=new_photo)
    photo = new_photo

commons.bsm.fn_update_imageview = update_image

# 버튼 생성
start_btn = ttk.Button(bottom_frame, text="시작", command=on_start_click)
start_btn.pack(side="left", padx=5)
cancel_btn = ttk.Button(bottom_frame, text="중지", command=on_cancel_click)
cancel_btn.pack(side="left", padx=5)
scan_btn = ttk.Button(bottom_frame, text="스캔", command=on_scan_click)
scan_btn.pack(side="left", padx=5)
save_btn = ttk.Button(bottom_frame, text="저장", command=on_save_click)
save_btn.pack(side="left", padx=5)


# 메인 루프 실행
root.mainloop()

stop_event.set()
current_control_item.join()