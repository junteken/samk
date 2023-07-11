from screen.featurebase import FeatureBase

class JoinCountry(FeatureBase):

    # 한 위  
    # 속 원 표 표 769 253 1 괜담가입
    def __init__(self):
        self.name = '국가선택'
        self.feature_texts=['괜덤가입', '보상']
        self.img_file_path = './rsrc/state_img/joincountry.png'

