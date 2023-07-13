from screen.featurebase import FeatureBase

class Shop(FeatureBase):

    # 보석 자원 장비
    def __init__(self):
        self.name = '상점'
        self.feature_texts=['보석', '자원', '장비']
        self.img_file_path = './rsrc/state_img/shop.png'

