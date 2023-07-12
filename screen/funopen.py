from screen.featurebase import FeatureBase

class FunOpen(FeatureBase):
    #  확득가능보상 취소 이동

    def __init__(self):
        self.name = '기능오픈'
        self.feature_texts=['확득가능보상', '이동']
        self.img_file_path = './rsrc/state_img/func_open.png'

