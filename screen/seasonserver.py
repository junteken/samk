from screen.featurebase import FeatureBase

class SeasonServer(FeatureBase):

    def __init__(self):
        self.name = '서버선택'
        self.feature_texts=['시즌서버', 'HB']
        self.img_file_path = './rsrc/state_img/season_server.png'

