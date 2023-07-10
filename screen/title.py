from screen.featurebase import FeatureBase

class Title(FeatureBase):

    def __init__(self):
        self.name = '타이틀화면'
        self.feature_texts=['게임시작', '과도한', '게임이용은']
        self.img_file_path = './rsrc/state_img/title.png'

   