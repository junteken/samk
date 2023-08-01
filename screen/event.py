from screen.featurebase import FeatureBase

class Event(FeatureBase):
    # 매일 지급 성장기금'

    def __init__(self):
        self.name = '이벤트'
        self.feature_texts=['매일', '성장기금']
        self.img_file_path = './rsrc/state_img/event.png'

