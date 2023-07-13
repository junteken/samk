from screen.featurebase import FeatureBase

class Mail(FeatureBase):

    # 우편 시스템 전투보고 유저  전체 읽음표기'
    def __init__(self):
        self.name = '우편'
        self.feature_texts=['우편', '전체']
        self.img_file_path = './rsrc/state_img/mail.png'

