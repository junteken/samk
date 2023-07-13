from screen.featurebase import FeatureBase

class Ranking(FeatureBase):

    # 유저 무장 공성 일동
    def __init__(self):
        self.name = '랭킹'
        self.feature_texts=['무장전', '유저']
        self.img_file_path = './rsrc/state_img/ranking.png'

