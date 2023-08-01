
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

import threading
import time
import tkinter as tk

class MainWindow(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.current_control_item = None
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        # 창 크기 설정 (원하는 창 크기로 변경)
        self.window_width = 1000
        self.window_height = 1000
        # 창 위치 계산 (우측 상단)
        x = screen_width - self.window_width
        y = 0
        # 창 크기 및 위치 설정
        parent.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')
        s = ttk.Style()
        s.configure('Treeview', rowheight=30) # repace 40 with whatever you need
        self.create_widgets()
        for item in control_manager.control_item:
            self.list_view.insert('', 'end', text=item.con_name)
        commons.bsm.fn_update_imageview = self.update_image
        self.stop_event = None
        
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.parent.title('삼국지k 자동화툴')

        # 프레임 생성
        left_frame = ttk.Frame(self.parent)
        left_frame.pack(side="left", padx=5, pady=10)

        right_frame = ttk.Frame(self.parent)      
        right_frame.pack(side="right", padx=5, pady=10)

        bottom_frame = ttk.Frame(self.parent)
        bottom_frame.pack(side="bottom", padx=5, pady=10, fill="x")

        # 리스트뷰 생성
        self.list_view = ttk.Treeview(left_frame,
                                    #   height=self.window_height*.2,                                       
                                         selectmode='browse')
        self.list_view.bind('<<TreeviewSelect>>', self.get_selected_item_text)
        self.list_view.pack(fill="both", expand=True)

        # 이미지뷰 생성
        _, cur_img = commons.bsm.get_CurrentBsImg()
        photo = ImageTk.PhotoImage(cur_img)

        self.image_label = ttk.Label(right_frame, image=photo)
        self.image_label.pack()
        # 왼쪽 클릭시 이벤트 발생 cb 등록
        self.image_label.bind('<Button-1>', self.img_click_event)

        # 텍스트뷰와 스크롤바를 위한 프레임 생성
        text_frame = ttk.Frame(left_frame)
        text_frame.pack(fill="both", expand=True)

        # 텍스트뷰 및 스크롤바 생성
        self.text_view = tk.Text(text_frame, wrap="word")
        self.text_view.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_view.yview)
        scrollbar.pack(side="right", fill="y")

        self.text_view.config(yscrollcommand=scrollbar.set)

        commons.log_text_view = self.text_view

        # 왼쪽 프레임의 하단에 버튼 추가
        bottom_frame = ttk.Frame(left_frame)
        bottom_frame.pack(side="bottom", padx=5, pady=10, fill="x")

        # 버튼 생성
        self.start_btn = ttk.Button(bottom_frame, text="시작", command=self.on_start_click)
        self.start_btn.pack(side="left", padx=5)
        self.cancel_btn = ttk.Button(bottom_frame, text="중지", command=self.on_cancel_click)
        self.cancel_btn.pack(side="left", padx=5)
        self.scan_btn = ttk.Button(bottom_frame, text="스캔", command=self.on_scan_click)
        self.scan_btn.pack(side="left", padx=5)
        self.save_btn = ttk.Button(bottom_frame, text="저장", command=self.on_save_click)
        self.save_btn.pack(side="left", padx=5)

    def on_start_click(self):
        self.start_btn.config(state='disabled')
        selected_item = self.get_selected_item_text()
        self.current_control_item = control_manager.control_dict[selected_item]
        self.stop_event = threading.Event()
        self.current_control_item(self.stop_event).start()

    def on_cancel_click(self):
        if self.stop_event is not None:
            self.stop_event.set()
        self.start_btn.config(state='enabled')

    def on_scan_click(self):
        _, ocr_text = commons.get_current_text()
        _, img = commons.bsm.get_CurrentBsImg()
        self.update_image(img)
        self.text_view.insert('end', ocr_text)
        self.text_view.insert('end', "'\n'")

    def on_save_click(self):
        bbox, img = commons.bsm.get_CurrentBsImg()
        file_name = filedialog.asksaveasfilename(defaultextension=".png", 
                                                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_name:
            img.save(file_name)

    def update_image(self, img):
        global photo
        # 이미지 업데이트    
        new_photo = ImageTk.PhotoImage(img)
        self.image_label.configure(image=new_photo)
        photo = new_photo

    def get_selected_item_text(self, event=None):
        item = self.list_view.item(self.list_view.focus()) # 선택된 항목의 아이디 가져오기
        cur_item = item['text'] # 아이디를 사용해 항목의 텍스트 속성 가져오기
        return cur_item    
    
    def img_click_event(self, event):
        x, y = event.x, event.y
        print(f"Relative coordinates: ({x}, {y})")

    def on_closing(self):
        if self.stop_event is not None:
            self.stop_event.set()
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    m_win = MainWindow(root)    
    
    root.mainloop()
