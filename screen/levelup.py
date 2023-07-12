from screen.featurebase import FeatureBase

class LevelUp(FeatureBase):
    # 승화성공 
    # 레텔: 38} {던전횟수: 125}

    def __init__(self):
        self.name = '레벨업'
        self.feature_texts=['승화성공', '던전횟수:']
        self.img_file_path = './rsrc/state_img/levelup.png'

