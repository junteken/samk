from screen.featurebase import FeatureBase

class Vip(FeatureBase):
    # 귀족때키지 오리 퍽 귀족때키지 일일복지
    # 매주때키지 귀족0선물 총가치 귀족
    # 선물 수령 재충전시
    def __init__(self):
        self.name = '귀족패키지'
        self.feature_texts=['귀족', '선물', '수령']
        self.img_file_path = './rsrc/state_img/vip.png'

