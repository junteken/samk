from screen.featurebase import FeatureBase

class WeekEvent(FeatureBase):
    # 이벤트 출석 성장기금 출석체크
    def __init__(self):
        self.name = '이벤트'
        self.feature_texts=['이벤트', '출석', '성장기금']
        self.img_file_path = './rsrc/state_img/vip.png'

