from screen.featurebase import FeatureBase

class ChulMujang(FeatureBase):

    # 우편 시스템 전투보고 유저  전체 읽음표기'
    def __init__(self):
        self.name = '출전무장'
        self.feature_texts=['출전무장', '무장']
        self.img_file_path = './rsrc/state_img/chulmujang.png'

