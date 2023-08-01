import os
import sys
import importlib
from control.getallreward import GetAllReward
from control.coupon import Coupon


# directory = './control'

# # 디렉토리를 시스템 경로에 추가
# sys.path.insert(0, directory)

# for filename in os.listdir(directory):
#     if filename.endswith('.py') and not filename.startswith('__init__'):
#         # 파일 확장자 삭제
#         module_name = filename[:-3]
        
#         # 모듈 import
#         module = importlib.import_module(module_name)


control_item=[
    GetAllReward,
    Coupon,
]

control_dict={}

for con in control_item:
    control_dict[con.con_name] = con

