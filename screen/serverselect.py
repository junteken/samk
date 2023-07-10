from screen.featurebase import FeatureBase

class ServerSelect(FeatureBase):

    def __init__(self):
        self.name = '서버선택'
        self.feature_texts=['모든신서버']
        self.img_file_path = './rsrc/state_img/serverselection.png'

