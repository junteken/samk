from screen.featurebase import FeatureBase

class Notice(FeatureBase):

    def __init__(self):
        self.name = '공지'
        self.feature_texts=['공지', '문의사항:', '공식카페']
        self.img_file_path = './rsrc/state_img/notice.png'

