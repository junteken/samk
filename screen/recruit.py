from screen.featurebase import FeatureBase

class Recruit(FeatureBase):
    # 매일 지급 성장기금'

    def __init__(self):
        self.name = '무장모집'
        self.feature_texts=['무장모집', '일반모집', '중급모집']
        self.img_file_path = './rsrc/state_img/recruit.png'

