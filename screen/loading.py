from screen.featurebase import FeatureBase

class Loading(FeatureBase):

    # 팀 진급시 무장의 속성과 보유병력이 대쪽으로 중가합니다

    def __init__(self):
        self.name = '로딩중'
        self.feature_texts=['팀']
        self.img_file_path = './rsrc/state_img/loading.png'

