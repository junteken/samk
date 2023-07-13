from screen.featurebase import FeatureBase

class Growth(FeatureBase):
    #  
    def __init__(self):
        self.name = '레벨업'
        self.feature_texts=['성장하기', '추천성급']
        self.img_file_path = './rsrc/state_img/grow.png'

