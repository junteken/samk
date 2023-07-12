from screen.featurebase import FeatureBase

class Reward(FeatureBase):
    # 보상 오기 상세내용 수령기한 
    # 지급일로부터수령 모두수령

    def __init__(self):
        self.name = '보상'
        self.feature_texts=['보상', '상세내용', '모두수령']
        self.img_file_path = './rsrc/state_img/reward.png'

