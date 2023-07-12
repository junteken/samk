from screen.featurebase import FeatureBase

class Firstpaid(FeatureBase):
    # 첫충전 스페설 선물!} 
    # {[} {누적 55원보 패키지가치2 110원보)}

    def __init__(self):
        self.name = '첫충전'
        self.feature_texts=['충전', '누적']
        self.img_file_path = './rsrc/state_img/firstpaid.png'

