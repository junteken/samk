from screen.featurebase import FeatureBase

class Mujangsel(FeatureBase):

    # 우편 시스템 전투보고 유저  전체 읽음표기'
    def __init__(self):
        self.name = '무장선택'
        self.feature_texts=['무장선택', '조합']
        self.img_file_path = './rsrc/state_img/mujangselect.png'

